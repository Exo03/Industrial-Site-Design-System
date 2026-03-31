import json
from datetime import datetime
from functools import partial

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QMessageBox, QFileDialog,
    QStyleOptionGraphicsItem, QStyle, QApplication, QGraphicsView, QDialog
)
from PySide6.QtCore import Qt, QStandardPaths, QSize, QTimer
from PySide6.QtGui import QPainter, QImage, QTransform

from UI_Files.MainWindow import Ui_MainWindow
from .add_object_window import AddObjectDialog
from ...api.element_types import get_element_types, upload_element_type
from ...api.elements import get_project_elements, move_element, delete_element, recolor_element, resize_element, \
    add_elements
from ...api.projects import rename_project, resize_project
from ...core import AsyncWorker
from ...ui.widgets.graphics import (
    ZoomableGraphicsView, GridScene, SnappableObject,
    WorkspaceArea, PIXELS_PER_METER
)
from client.session_manager import session
from .edit_object_window import EditObjectWindow
from .set_area_window import SetAreaWindow
from .profile_dialog import ProfileDialog
from .auth_dialog import AuthDialog
from ...core.theme_manager import theme_manager
from ...api.elements import rename_element

import sys
import os

from ...utils.paths import get_resource_path

MOVE_DEBOUNCE_MS = 500

class CanvasWindow(QMainWindow):
    def __init__(self, project_data=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._element_types = []
        self._load_element_types()

        self._current_project = project_data
        self._elements_map = {}
        self._pending_sync = {}

        self.ui.toolBar.setIconSize(QSize(24, 24))

        self.ui.graphicsView.setParent(None)
        self.ui.graphicsView.deleteLater()

        self.scene = GridScene(grid_size=10)
        self.graphicsView = ZoomableGraphicsView(self.scene, self.ui.centralwidget)

        layout = QVBoxLayout(self.ui.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.graphicsView)

        self.ui.graphicsView = self.graphicsView

        self.ui.graphicsView.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.ui.actionAddObject.triggered.connect(self.add_object)
        self.ui.actionEditObject.triggered.connect(self.edit_object)
        self.ui.actionDeleteObject.triggered.connect(self.delete_object)
        self.ui.actionSetArea.triggered.connect(self.set_area)
        self.ui.actionAddObjectsList.triggered.connect(self.add_objects_list)
        self.ui.action_8.triggered.connect(self.open_auth_dialog)
        self.ui.actionSavePNG.triggered.connect(self.save_project_png)
        self.ui.actionSaveJSON.triggered.connect(self.save_project_json)

        self.ui.actionSaveToServer = self.ui.toolBar.addAction("💾 Сохранить")
        self.ui.actionSaveToServer.triggered.connect(self._save_to_server)

        self.ui.action_10.triggered.connect(lambda: self.change_theme('light'))
        self.ui.action_11.triggered.connect(lambda: self.change_theme('dark'))
        self.ui.action_12.triggered.connect(lambda: self.change_theme('system'))

        self.statusBar().showMessage("Масштаб: 1 м = 20 пикс. | Сетка: 0.5 м (1 клетка)")
        self.status_label = QLabel("")
        self.statusBar().addPermanentWidget(self.status_label)

        self.update_icons_for_theme(theme_manager.current_theme)

        if project_data:
            self._load_project(project_data)

    def _load_element_types(self):
        self.ui.comboBox.clear()
        self._custom_objects = []

        # Асинхронно загружаем все типы оборудования из базы
        worker = AsyncWorker.run_async(get_element_types())

        # Защита от GC
        if not hasattr(self, '_active_workers'):
            self._active_workers = set()
        self._active_workers.add(worker)

        worker.signals.success.connect(self._on_types_loaded)
        worker.signals.error.connect(lambda e: print(f"Ошибка загрузки типов: {e}"))
        worker.signals.finished.connect(partial(self._cleanup_worker, worker=worker))

    def _on_types_loaded(self, types: list):
        self._element_types = types
        self.ui.comboBox.clear()

        for etype in types:
            width = float(etype.get('width', 6.0))
            length = float(etype.get('length', 4.0))
            zone_width = float(etype.get('zone_width', width))

            # Вычисляем обратно margin: (zone_width - width) / 2
            margin = (zone_width - width) / 2 if zone_width > width else 0.0

            template_data = {
                'name': etype.get('title'),
                'width': width,
                'length': length,
                'color': etype.get('color', '#96C8FF'),
                'element_type_id': etype.get('id'),
                'zone_margin': margin  # Восстанавливаем отступ
            }

            self._add_template_to_combobox(template_data)

    def _load_project(self, project_data: dict):
        self._current_project = project_data
        self.setWindowTitle(f"Industrial Designer - {project_data['name']}")

        if self._current_project:
            self._current_project['_area_modified'] = False

        # ⭐ Загружаем площадку из размеров проекта (width/length)
        width = project_data.get('width')
        length = project_data.get('length')

        if width and length:
            self.set_workspace_area(width, length)
            print(f"DEBUG: Загружена площадка {width}x{length} из проекта")
        else:
            # Если размеры не заданы — создаём дефолтную
            self.set_workspace_area(50, 50)
            print("DEBUG: Создана дефолтная площадка 50x50")

        self._load_elements()

    def _load_elements(self):
        if not self._current_project or not session.token:
            return

        worker = AsyncWorker.run_async(
            get_project_elements(self._current_project['id'], session.token)
        )
        worker.signals.success.connect(self._on_elements_loaded)
        worker.signals.error.connect(self._on_elements_error)

    def _on_elements_loaded(self, elements: list):
        # Удаляем только объекты, не площадку!
        for item in list(self.scene.items()):
            if isinstance(item, SnappableObject):
                self.scene.removeItem(item)

        self._elements_map.clear()

        # Создаём объекты
        for elem_data in elements:
            # ⭐ Ищем сохраненную зону в типах оборудования
            type_id = elem_data.get('element_type_id')
            margin = 0.0
            if type_id:
                for etype in self._element_types:
                    if etype.get('id') == type_id:
                        w = float(etype.get('width', 6.0))
                        z_w = float(etype.get('zone_width', w))
                        if z_w > w:
                            margin = (z_w - w) / 2
                        break

            obj = SnappableObject(
                text=elem_data.get('title', 'Объект'),
                width_m=elem_data.get('width', 6.0),
                height_m=elem_data.get('length', 4.0),
                color=elem_data.get('color', '#96C8FF'),
                grid_size_m=0.5,
                pixels_per_meter=PIXELS_PER_METER,
                zone_margin_m=margin  # ⭐ ТЕПЕРЬ ЗОНА НЕ БУДЕТ СБРАСЫВАТЬСЯ В 0
            )

            obj._element_id = elem_data['id']
            obj._element_type_id = elem_data.get('element_type_id')
            obj._is_modified = False

            obj.geometryChanged.connect(lambda o=obj: self._on_object_moved_ui(o))

            self.scene.addItem(obj)
            obj.setPos(
                elem_data.get('x', 0) * PIXELS_PER_METER,
                elem_data.get('y', 0) * PIXELS_PER_METER
            )

            self._elements_map[elem_data['id']] = obj

        # ⭐ Важно: принудительно обновляем сцену перед проверками
        self.scene.update()

        # ⭐ Проверяем границы для каждого объекта явно
        for obj in self._elements_map.values():
            self.check_object_bounds(obj)

        self.check_object_collisions()
        self.update_status_bar()
        self.statusBar().showMessage(f"Загружено элементов: {len(elements)}", 3000)

    def _perform_post_load_checks(self):
        """Выполняет проверки после полной инициализации сцены"""
        self.check_object_collisions()
        self.update_status_bar()

    def _on_elements_error(self, error: Exception):
        QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить элементы:\n{error}")

    def change_theme(self, theme: str):

        if theme == 'system':
            theme = 'dark'
        theme_manager.apply_theme(theme)
        self.update_icons_for_theme(theme)

    def update_icons_for_theme(self, theme: str):
        from PySide6.QtGui import QIcon

        suffix = "FFFFFF" if theme == "dark" else "000000"

        # Используем get_resource_path вместо прямых путей
        self.ui.actionAddObject.setIcon(
            QIcon(
                get_resource_path(f"Icons/add_24dp_{suffix}.svg"))
        )
        self.ui.actionEditObject.setIcon(
            QIcon(get_resource_path(f"Icons/edit_24dp_{suffix}.svg"))
        )
        self.ui.actionDeleteObject.setIcon(
            QIcon(get_resource_path(f"Icons/delete_24dp_{suffix}.svg"))
        )
        self.ui.actionSetArea.setIcon(
            QIcon(get_resource_path(f"Icons/activity_zone_24dp_{suffix}.svg"))
        )

    def save_project_png(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить в PNG",
            QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation) + "/project.png",
            "PNG Images (*.png);;JPEG Images (*.jpg *.jpeg);;BMP Images (*.bmp);;All Files (*)"
        )

        if not file_path:
            return

        if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            file_path += '.png'

        self._do_save_png(file_path)

    def _do_save_png(self, file_path: str):
        try:
            scene_rect = self.scene.itemsBoundingRect()
            margin = 50
            render_rect = scene_rect.adjusted(-margin, -margin, margin, margin)

            width = int(render_rect.width())
            height = int(render_rect.height())

            image = QImage(width, height, QImage.Format_ARGB32)
            image.fill(Qt.transparent)

            painter = QPainter(image)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.translate(-render_rect.x(), -render_rect.y())

            self.scene.drawBackground(painter, render_rect)

            items = sorted(self.scene.items(), key=lambda item: item.zValue())

            for item in items:
                if not item.isVisible():
                    continue

                painter.save()
                painter.setTransform(item.sceneTransform(), True)

                option = QStyleOptionGraphicsItem()
                option.rect = item.boundingRect().toRect()
                option.state = QStyle.State_None

                item.paint(painter, option, None)
                painter.restore()

            painter.end()

            if image.save(file_path):
                self.statusBar().showMessage(f"✓ Сохранено: {file_path}", 5000)
                QMessageBox.information(self, "Успех", f"Изображение сохранено:\n{file_path}")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось сохранить изображение")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения:\n{e}")

    def save_project_json(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить в JSON",
            QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation) + "/project.json",
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            return

        if not file_path.lower().endswith('.json'):
            file_path += '.json'

        self._do_save_json(file_path)

    def _do_save_json(self, file_path: str):
        """Сохраняет проект в JSON согласно структуре БД"""
        try:
            # Данные о площадке (если есть)
            area = self.get_workspace_area()
            area_data = None
            if area:
                area_data = {
                    "width": int(area._width_m),
                    "length": int(area._length_m),
                    "x": int(area.pos().x() / PIXELS_PER_METER),
                    "y": int(area.pos().y() / PIXELS_PER_METER)
                }

            # Данные об элементах - только поля из БД
            elements_data = []
            for element_id, obj in self._elements_map.items():
                # Цвет в формате #RRGGBB (убираем альфа-канал если есть)
                color = obj._color
                if hasattr(color, 'name'):
                    color_str = color.name()[:7]  # Берем только #RRGGBB
                else:
                    color_str = str(color)[:7]

                element_data = {
                    "id": element_id,  # Серверный ID или локальный
                    "element_type_id": getattr(obj, '_element_type_id', None),
                    "title": obj._text[:64] if obj._text else "Объект",  # Ограничение varchar(64)
                    "x": int(obj.pos().x() / PIXELS_PER_METER),
                    "y": int(obj.pos().y() / PIXELS_PER_METER),
                    "width": int(obj._width_m),
                    "length": int(obj._height_m),
                    "color": color_str
                }
                elements_data.append(element_data)

            # Состояние камеры
            viewport_center = self.graphicsView.mapToScene(
                self.graphicsView.viewport().rect().center()
            )

            project_data = {
                "version": "2.0-db",
                "created_at": datetime.now().isoformat(),
                "project": {
                    "id": self._current_project.get('id') if self._current_project else None,
                    "name": self._current_project.get('name',
                                                      'New Project') if self._current_project else 'New Project',
                    "description": self._current_project.get('description', '') if self._current_project else '',
                    "area": area_data
                },
                "settings": {
                    "pixels_per_meter": PIXELS_PER_METER,
                    "grid_size": getattr(self.scene, '_grid_size', 10)
                },
                "elements": elements_data,
                "view": {
                    "center_x": int(viewport_center.x()),
                    "center_y": int(viewport_center.y()),
                    "zoom": self.graphicsView.transform().m11()
                }
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)

            self.current_project_path = file_path
            self.statusBar().showMessage(f"✓ Сохранено: {len(elements_data)} объектов", 5000)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить:\n{e}")
            import traceback
            traceback.print_exc()

    def load_project_json(self):
        """Загружает проект из JSON"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть проект",
            QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            return

        self._do_load_json(file_path)

    def _do_load_json(self, file_path: str):
        """Загружает проект с учетом структуры БД"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Очищаем сцену
            for item in list(self.scene.items()):
                if isinstance(item, (SnappableObject, WorkspaceArea)):
                    self.scene.removeItem(item)
            self._elements_map.clear()

            # Загружаем метаданные
            project_info = data.get('project', {})
            old_project_id = project_info.get('id')

            # Создаем новый локальный проект (ID будет назначен при сохранении на сервере)
            self._current_project = {
                'id': None,  # Новый проект - новый ID
                'name': project_info.get('name', 'Imported Project'),
                'description': project_info.get('description', ''),
                'width': None,
                'length': None,
                '_needs_sync': True  # Флаг, что проект нужно создать на сервере
            }

            # Загружаем площадку
            area_data = project_info.get('area')
            if area_data:
                width = int(area_data.get('width', 50))
                length = int(area_data.get('length', 50))
                self._current_project['width'] = width
                self._current_project['length'] = length

                area = WorkspaceArea(width, length)
                self.scene.addItem(area)

                if 'x' in area_data and 'y' in area_data:
                    area.setPos(
                        int(area_data['x']) * PIXELS_PER_METER,
                        int(area_data['y']) * PIXELS_PER_METER
                    )
                else:
                    # ⭐ Размещаем в центре сцены (5000, 5000)
                    width_px = width * PIXELS_PER_METER
                    height_px = length * PIXELS_PER_METER

                    scene_center_x = self.scene.width() / 2
                    scene_center_y = self.scene.height() / 2

                    area.setPos(
                        scene_center_x - width_px / 2,
                        scene_center_y - height_px / 2
                    )

                    # Центрируем вид на центр сцены
                QTimer.singleShot(0, lambda: self.graphicsView.centerOn(
                    self.scene.width() / 2, self.scene.height() / 2
                ))

            # Загружаем элементы - создаем как новые (без привязки к старым ID)
            elements = data.get('elements', [])
            for elem_data in elements:
                # Валидация обязательных полей
                x = int(elem_data.get('x', 0))
                y = int(elem_data.get('y', 0))
                width = int(elem_data.get('width', 6))
                length = int(elem_data.get('length', 4))

                # Обрезаем title до 64 символов
                title = elem_data.get('title', 'Объект')[:64]

                # Нормализуем цвет
                color = elem_data.get('color', '#96C8FF')
                if not color.startswith('#') or len(color) != 7:
                    color = '#96C8FF'

                obj = SnappableObject(
                    text=title,
                    width_m=width,
                    height_m=length,
                    color=color,
                    grid_size_m=0.5,
                    pixels_per_meter=PIXELS_PER_METER
                )

                # Сбрасываем ID - объект будет создан как новый на сервере
                # Сохраняем старый ID только для информации
                obj._original_id = elem_data.get('id')
                obj._element_id = None  # Новый объект
                obj._element_type_id = elem_data.get('element_type_id')
                obj._is_modified = True  # Помечаем для синхронизации

                obj.setPos(x * PIXELS_PER_METER, y * PIXELS_PER_METER)
                obj.geometryChanged.connect(lambda o=obj: self._on_object_moved_ui(o))

                self.scene.addItem(obj)
                # Временный ID для локальной карты
                temp_id = f"temp_{len(self._elements_map)}"
                self._elements_map[temp_id] = obj

            # Восстанавливаем вид
            view_data = data.get('view', {})
            if view_data:
                if 'center_x' in view_data and 'center_y' in view_data:
                    self.graphicsView.centerOn(view_data['center_x'], view_data['center_y'])
                if 'zoom' in view_data:
                    self.graphicsView.setTransform(QTransform().scale(view_data['zoom'], view_data['zoom']))

            self.check_object_collisions()
            self.update_status_bar()
            self.setWindowTitle(f"Industrial Designer - {self._current_project['name']} [Импорт]")

            QMessageBox.information(
                self,
                "Проект загружен",
                f"Загружено объектов: {len(elements)}\n"
                f"Сохраните проект на сервере (💾), чтобы создать копию с новыми ID."
            )

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить:\n{e}")
            import traceback
            traceback.print_exc()

    def import_json_as_new_project(self):
        """Импорт JSON как нового проекта с сохранением на сервер"""
        # Сначала загружаем JSON локально
        self.load_project_json()

        # Затем предлагаем сохранить как новый проект на сервере
        if self._current_project and self._current_project.get('_needs_sync'):
            reply = QMessageBox.question(
                self,
                "Синхронизация",
                "Сохранить импортированный проект на сервере как новый?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self._save_imported_project_to_server()

    def _on_logged_in(self, username):
        self.statusBar().showMessage(f"Пользователь: {username}")

    def _on_logged_out(self):
        self.statusBar().showMessage("Не авторизован")
        self.scene.clear()

    def open_auth_dialog(self):
        if session.is_authenticated:
            dialog = ProfileDialog(self)
            dialog.exec()
        else:
            dialog = AuthDialog(self)
            dialog.exec()

    def set_area(self):
        dialog = SetAreaWindow(self)
        if dialog.exec() == SetAreaWindow.Accepted:
            width, height = dialog.get_values()
            if width and height:
                self.set_workspace_area(width, height)
                if self._current_project:
                    self._current_project['width'] = width
                    self._current_project['length'] = height
                    self._current_project['_area_modified'] = True
                    self.statusBar().showMessage(f"Площадка изменена: {width}×{height} м (нажмите 💾 для сохранения)",
                                                 5000)

    def set_workspace_area(self, width_m, height_m):
        # Удаляем старую площадку
        for item in self.scene.items():
            if isinstance(item, WorkspaceArea):
                self.scene.removeItem(item)

        area = WorkspaceArea(width_m, height_m)
        self.scene.addItem(area)

        # ⭐ Размещаем площадку в центре сцены (5000, 5000)
        area_width_px = width_m * PIXELS_PER_METER
        area_height_px = height_m * PIXELS_PER_METER

        # Центр сцены
        scene_center_x = self.scene.width() / 2  # 5000
        scene_center_y = self.scene.height() / 2  # 5000

        area.setPos(
            scene_center_x - area_width_px / 2,
            scene_center_y - area_height_px / 2
        )

        # Центрируем вид на центр сцены (5000, 5000), если нужно
        QTimer.singleShot(0, lambda: self.graphicsView.centerOn(scene_center_x, scene_center_y))

    def get_workspace_area(self):
        for item in self.scene.items():
            if isinstance(item, WorkspaceArea):
                return item
        return None

    def get_viewport_center_scene_pos(self):
        """Возвращает координаты центра видимой области в системе координат сцены"""
        # Получаем размер viewport в пикселях
        viewport_rect = self.graphicsView.viewport().rect()
        viewport_center = viewport_rect.center()

        # Преобразуем координаты viewport в координаты сцены
        scene_pos = self.graphicsView.mapToScene(viewport_center)
        return scene_pos

    def check_object_bounds(self, obj: SnappableObject):
        area = self.get_workspace_area()
        if not area:
            obj.set_outside_area(False)
            obj.set_zone_outside_area(False)
            return False

        area_rect = area.mapToScene(area.boundingRect()).boundingRect()

        # Проверяем сам объект (body)
        obj_body_rect = obj.mapToScene(obj.bodyRect()).boundingRect()
        is_obj_outside = not area_rect.contains(obj_body_rect)
        obj.set_outside_area(is_obj_outside)

        # Проверяем зону обслуживания
        if obj._zone_margin_m > 0:
            obj_zone_rect = obj.mapToScene(obj.zoneRect()).boundingRect()
            is_zone_outside = not area_rect.contains(obj_zone_rect)
            obj.set_zone_outside_area(is_zone_outside)
        else:
            obj.set_zone_outside_area(is_obj_outside)

        return is_obj_outside

    def check_object_collisions(self):
        objects = [item for item in self.scene.items() if isinstance(item, SnappableObject)]

        # Сначала сбрасываем флаги для всех
        for obj in objects:
            obj.set_overlapping(False)
            obj.set_zone_overlapping(False)

        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects):
                if i >= j:
                    continue

                # 1. Проверяем столкновение самих объектов
                body1_rect = obj1.mapToScene(obj1.bodyRect()).boundingRect()
                body2_rect = obj2.mapToScene(obj2.bodyRect()).boundingRect()

                if body1_rect.intersects(body2_rect):
                    obj1.set_overlapping(True)
                    obj2.set_overlapping(True)

                # 2. Проверяем пересечение зон обслуживания
                zone1_rect = obj1.mapToScene(obj1.zoneRect()).boundingRect()
                zone2_rect = obj2.mapToScene(obj2.zoneRect()).boundingRect()

                if zone1_rect.intersects(zone2_rect):
                    # Отмечаем ошибку зоны, только если хотя бы у одного объекта есть зона
                    if obj1._zone_margin_m > 0 or obj2._zone_margin_m > 0:
                        obj1.set_zone_overlapping(True)
                        obj2.set_zone_overlapping(True)

    def update_status_bar(self):
        area = self.get_workspace_area()
        outside_names = []
        overlapping_names = []
        zone_outside_names = []
        zone_overlapping_names = []

        for item in self.scene.items():
            if isinstance(item, SnappableObject):
                if item._is_outside_area:
                    outside_names.append(item._text)
                elif item._is_zone_outside_area:
                    zone_outside_names.append(item._text)

                if item._is_overlapping:
                    overlapping_names.append(item._text)
                elif item._is_zone_overlapping:
                    zone_overlapping_names.append(item._text)

        messages = []
        if outside_names:
            messages.append("⚠️ Вне площадки: " + ", ".join(outside_names))
        if zone_outside_names:
            messages.append("🟥 Зона обслуживания вне площадки: " + ", ".join(zone_outside_names))
        if overlapping_names:
            messages.append("🔴 Объекты пересекаются: " + ", ".join(overlapping_names))
        if zone_overlapping_names:
            messages.append("🟡 Зоны обслуживания пересекаются: " + ", ".join(zone_overlapping_names))

        self.status_label.setText(" | ".join(messages) if messages else "")

    def _on_object_moved_ui(self, obj: SnappableObject):
        """Только UI обновления при перемещении, без отправки на сервер"""
        obj._is_modified = True  # Помечаем как изменённый
        self.check_object_bounds(obj)
        self.check_object_collisions()
        self.update_status_bar()

    def add_object(self):
        """Добавляет выбранный из combobox объект на сцену"""
        if not self._current_project or not session.token:
            QMessageBox.warning(self, "Ошибка", "Нет активного проекта")
            return

        index = self.ui.comboBox.currentIndex()
        if index < 0:
            QMessageBox.warning(self, "Ошибка", "Сначала добавьте объекты через диалог (+)")
            return

        # Получаем данные из combobox (сохраненные как userData)
        obj_data = self.ui.comboBox.currentData()
        if not obj_data:
            QMessageBox.warning(self, "Ошибка", "Нет данных об объекте")
            return

        self.statusBar().showMessage("Создание объекта...", 3000)

        # Центр видимой области
        center_pos = self.get_viewport_center_scene_pos()
        x_pos = int(center_pos.x() / PIXELS_PER_METER)
        y_pos = int(center_pos.y() / PIXELS_PER_METER)

        worker = AsyncWorker.run_async(add_elements(
            project_id=self._current_project['id'],
            element_type_id=1,  # Дефолтный тип или None, если API позволяет
            x=x_pos,
            y=y_pos,
            width=int(obj_data['width']),
            length=int(obj_data['length']),
            title=obj_data['name'],
            color=obj_data['color'],
            token=session.token
        ))

        zone = float(obj_data.get('zone_margin', 0.0))
        worker.signals.success.connect(
            partial(self._on_object_created, zone_margin=zone)
        )
        worker.signals.error.connect(self._on_object_create_error)

    def add_objects_list(self):
        """Открывает диалог добавления нескольких объектов"""
        if not self._current_project or not session.token:
            QMessageBox.warning(self, "Ошибка", "Нет активного проекта")
            return

        dialog = AddObjectDialog(self)
        if dialog.exec() != QDialog.Accepted:
            return

        objects = dialog.get_objects()
        if not objects:
            self.statusBar().showMessage("Нет объектов для добавления", 3000)
            return

        self.statusBar().showMessage(f"Создание {len(objects)} типов и объектов...", 5000)

        # Создаем типы и объекты последовательно
        for obj_data in objects:
            self._create_object_with_type(obj_data)

    def _create_object_with_type(self, obj_data):
        """Создает ElementType, затем Element"""

        width = float(obj_data['width'])
        length = float(obj_data['length'])
        # Достаем margin (по умолчанию 0)
        margin = float(obj_data.get('zone_margin', 0.0))

        # 1. Создаем тип элемента на сервере
        type_data = {
            'title': obj_data['name'][:64],
            'length': length,
            'width': width,
            # Общие габариты зоны = размер объекта + отступ с двух сторон
            'zone_length': length + 2 * margin,
            'zone_width': width + 2 * margin,
            'description': obj_data.get('description', f"Custom {obj_data['name']}")
        }

        # Асинхронное создание типа
        worker = AsyncWorker.run_async(upload_element_type(
            title=type_data['title'],
            length=type_data['length'],
            width=type_data['width'],
            zone_length=type_data['zone_length'],
            zone_width=type_data['zone_width'],
            description=type_data['description'],
            token=session.token
        ))

        # ЗАЩИТА ОТ GC
        if not hasattr(self, '_active_workers'):
            self._active_workers = set()
        self._active_workers.add(worker)

        worker.signals.success.connect(
            partial(self._on_type_created, obj_data=obj_data)
        )
        worker.signals.error.connect(
            partial(self._on_type_create_error, obj_name=obj_data['name'])
        )
        worker.signals.finished.connect(
            partial(self._cleanup_worker, worker=worker)
        )

    def _cleanup_worker(self, result_or_none, worker=None):
        """Удаляет отработавший воркер из списка активных"""
        if hasattr(self, '_active_workers') and worker in self._active_workers:
            self._active_workers.remove(worker)

    def _on_type_created(self, type_result, obj_data):
        print(f"DEBUG: Ответ сервера: {type_result}")
        element_type_id = type_result.get('id')

        if not element_type_id:
            return

        margin = float(obj_data.get('zone_margin', 0.0))

        # Добавляем в combobox шаблон с реальным type_id и зоной
        template_data = {
            'name': obj_data['name'],
            'width': obj_data['width'],
            'length': obj_data['length'],
            'color': obj_data['color'],
            'zone_margin': margin, # ⭐ Сохраняем зону для будущих добавлений
            'element_type_id': element_type_id
        }
        self._add_template_to_combobox(template_data)

        # Передаем margin локально
        self._create_single_object(
            element_type_id=element_type_id,
            title=obj_data['name'],
            width=obj_data['width'],
            length=obj_data['length'],
            color=obj_data['color'],
            zone_margin=margin
        )

    def _on_type_create_error(self, error, obj_name):
        """Обработка ошибки создания типа"""
        print(f"DEBUG ERROR: Не удалось создать тип для {obj_name}: {error}")
        QMessageBox.warning(self, "Ошибка",
                            f"Не удалось создать тип '{obj_name}':\n{error}")

    def _add_template_to_combobox(self, obj_data):
        """Добавляет объект в combobox как шаблон, если такого еще нет"""
        name = obj_data.get('name', 'Объект')
        # Проверяем, есть ли уже такой шаблон
        for i in range(self.ui.comboBox.count()):
            existing_data = self.ui.comboBox.itemData(i)
            if existing_data and existing_data.get('name') == name:
                return  # Уже есть

        # Добавляем новый шаблон
        self.ui.comboBox.addItem(name, obj_data)

    def _create_single_object(self, element_type_id, title, width, length, color, zone_margin=0.0):
        center_pos = self.get_viewport_center_scene_pos()
        import random
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)

        x_pos = int(center_pos.x() / PIXELS_PER_METER) + offset_x
        y_pos = int(center_pos.y() / PIXELS_PER_METER) + offset_y

        worker = AsyncWorker.run_async(add_elements(
            project_id=self._current_project['id'],
            element_type_id=element_type_id,
            x=x_pos,
            y=y_pos,
            width=int(width),
            length=int(length),
            title=title,
            color=color,
            token=session.token
        ))

        # ⭐ Используем partial, чтобы передать zone_margin в success callback
        worker.signals.success.connect(
            partial(self._on_object_created, zone_margin=zone_margin)
        )
        worker.signals.error.connect(self._on_object_create_error)

    # ⭐ Добавили zone_margin с дефолтным значением
    def _on_object_created(self, element_data: dict, zone_margin=0.0):
        if not element_data or 'id' not in element_data:
            QMessageBox.critical(self, "Ошибка", "Сервер вернул некорректные данные")
            return

        obj = SnappableObject(
            text=element_data.get('title', 'Объект'),
            width_m=float(element_data.get('width', 6.0)),
            height_m=float(element_data.get('length', 4.0)),
            color=element_data.get('color', '#96C8FF'),
            grid_size_m=0.5,
            pixels_per_meter=PIXELS_PER_METER,
            zone_margin_m=zone_margin # ⭐ ПРИМЕНЯЕМ ЗОНУ!
        )

        obj._element_id = element_data['id']
        obj._element_type_id = element_data.get('element_type_id')
        obj._is_modified = False

        obj.geometryChanged.connect(lambda: self._on_object_moved_ui(obj))

        center_pos = self.get_viewport_center_scene_pos()
        obj_width_px = obj._width_m * PIXELS_PER_METER
        obj_height_px = obj._height_m * PIXELS_PER_METER

        x_px = center_pos.x() - obj_width_px / 2
        y_px = center_pos.y() - obj_height_px / 2

        obj.setPos(x_px, y_px)
        self.scene.addItem(obj)
        self._elements_map[element_data['id']] = obj

        self.check_object_bounds(obj)
        self.check_object_collisions()
        self.update_status_bar()
        self.scene.update()

        self.statusBar().showMessage(f"Добавлен объект: {obj._text}", 3000)
        self._save_object_position(obj)

    def _on_object_create_error(self, error: Exception):
        """Обработка ошибки создания"""
        error_msg = str(error)
        print(f"DEBUG ERROR: _on_object_create_error: {error_msg}")
        QMessageBox.critical(self, "Ошибка", f"Не удалось создать объект:\n{error_msg}")

    def on_object_moved(self, obj):
        self.check_object_bounds(obj)
        self.check_object_collisions()
        self.update_status_bar()

    def edit_object(self):
        selected = self.scene.selectedItems()
        if not selected:
            return

        first_item = selected[0]
        if not isinstance(first_item, SnappableObject):
            return

        # ⭐ Добавляем передачу initial_zone
        dlg = EditObjectWindow(
            self,
            initial_text=first_item._text,
            initial_length=first_item._width_m,
            initial_width=first_item._height_m,
            initial_color=first_item._color.name(),
            initial_zone=getattr(first_item, '_zone_margin_m', 0.0)
        )

        if dlg.exec() != EditObjectWindow.Accepted:
            return

        changes = dlg.get_data()
        if not changes:
            return

        save_queue = []

        modified_count = 0
        for item in selected:
            if not isinstance(item, SnappableObject):
                continue

            element_id = getattr(item, '_element_id', None)

            # --- ВАШ ТЕКУЩИЙ КОД ---
            if "text" in changes:
                item.update_text(changes["text"])
                item._is_modified = True
                save_queue.append(('rename', element_id, changes["text"]))

            if "length" in changes:
                item._width_m = changes["length"]
                item._is_modified = True

            if "width" in changes:
                item._height_m = changes["width"]
                item._is_modified = True

            if "color" in changes:
                item.update_color(changes["color"])  # Обновляем цвет локально
                item._is_modified = True
                save_queue.append(('recolor', element_id, changes["color"]))

            # ⭐ Добавляем обработку изменения зоны
            if "zone_margin" in changes:
                item.update_zone_margin(changes["zone_margin"])
                item._is_modified = True

            if "length" in changes or "width" in changes:
                item.prepareGeometryChange()
                item.update()
                save_queue.append(('resize', element_id, int(item._width_m), int(item._height_m)))

            self.check_object_bounds(item)
            modified_count += 1

        self.check_object_collisions()
        self.update_status_bar()

        # ⭐ Запускаем сохранения последовательно через очередь
        if save_queue:
            self._pending_save_queue = save_queue
            self._process_save_queue()

        self.statusBar().showMessage(
            f"Изменения применены к {modified_count} объектов. Сохранение...", 3000
        )

    def _process_save_queue(self):
        """Обрабатывает очередь сохранений последовательно"""
        if not hasattr(self, '_pending_save_queue') or not self._pending_save_queue:
            self.statusBar().showMessage("Все изменения сохранены", 3000)
            return

        # Берём первое задание
        save_task = self._pending_save_queue.pop(0)
        save_type, element_id, *args = save_task

        print(f"DEBUG: Processing {save_type} for element {element_id}")

        # Создаём worker
        if save_type == 'rename':
            text = args[0]
            worker = AsyncWorker.run_async(
                rename_element(element_id, text, session.token)
            )
        elif save_type == 'recolor':
            color = args[0]
            worker = AsyncWorker.run_async(
                recolor_element(element_id, color, session.token)
            )
        elif save_type == 'resize':
            width, length = args
            worker = AsyncWorker.run_async(
                resize_element(element_id, width, length, session.token)
            )
        else:
            # Неизвестный тип — пропускаем
            self._process_save_queue()
            return

        # Подключаем callback'и с явным захватом
        # ⭐ Используем functools.partial вместо lambda для надёжности
        from functools import partial

        worker.signals.success.connect(
            partial(self._on_save_success, save_type, element_id)
        )
        worker.signals.error.connect(
            partial(self._on_save_error, save_type, element_id)
        )

    def _on_save_success(self, save_type, element_id, result=None):
        """Callback успешного сохранения"""
        print(f"DEBUG: {save_type} success for element {element_id}")
        # Продолжаем со следующим
        self._process_save_queue()

    def _on_save_error(self, save_type, element_id, error):
        """Callback ошибки сохранения"""
        print(f"DEBUG: {save_type} error for element {element_id}: {error}")
        # Продолжаем со следующим, даже при ошибке
        self._process_save_queue()

    def delete_object(self):
        selected = list(self.scene.selectedItems())

        for item in selected:
            if isinstance(item, SnappableObject):
                element_id = getattr(item, '_element_id', None)

                self._remove_from_scene(item)

                if element_id and session.token:
                    worker = AsyncWorker.run_async(
                        delete_element(element_id, session.token)
                    )
                    worker.signals.error.connect(self._on_delete_error)

    def _remove_from_scene(self, item):
        self.scene.removeItem(item)
        if hasattr(item, '_element_id') and item._element_id in self._elements_map:
            del self._elements_map[item._element_id]
        self.update_status_bar()

    def _on_delete_error(self, error: Exception):
        QMessageBox.critical(self, "Ошибка", f"Не удалось удалить объект:\n{error}")

    def _save_to_server(self):
        """Сохраняет позиции объектов и размеры площадки на сервер"""
        if not self._current_project or not session.token:
            QMessageBox.warning(self, "Ошибка", "Нет активного проекта")
            return

        # Проверяем, нужно ли сохранять площадку
        area_needs_save = self._current_project.get('_area_modified', False)

        # Проверяем, есть ли изменённые объекты
        modified_objects = [
            obj for obj in self._elements_map.values()
            if getattr(obj, '_is_modified', False)
        ]

        if not area_needs_save and not modified_objects:
            self.statusBar().showMessage("Нет изменений для сохранения", 3000)
            return

        self.statusBar().showMessage("Сохранение...", 5000)

        success_messages = []
        error_messages = []

        # 1. Сохраняем площадку если изменена
        if area_needs_save:
            area_success, area_error = self._save_area_to_server()
            if area_success:
                success_messages.append("площадка")
            if area_error:
                error_messages.append("площадка")

        # 2. Сохраняем позиции объектов
        if modified_objects:
            obj_success, obj_errors = self._save_objects_to_server(modified_objects)
            if obj_success > 0:
                success_messages.append(f"{obj_success} объектов")
            if obj_errors > 0:
                error_messages.append(f"{obj_errors} объектов")

        # Итоговое сообщение
        if error_messages:
            self.statusBar().showMessage(f"Ошибки при сохранении: {', '.join(error_messages)}", 5000)
            QMessageBox.warning(self, "Частичное сохранение",
                                f"Успешно сохранено: {', '.join(success_messages) if success_messages else 'ничего'}\n"
                                f"Ошибки: {', '.join(error_messages)}")
        else:
            self.statusBar().showMessage(f"✓ Сохранено: {', '.join(success_messages)}", 5000)
            QMessageBox.information(self, "Успех", f"Сохранено: {', '.join(success_messages)}")

    def _save_area_to_server(self) -> tuple:
        """Сохраняет размеры площадки через resize_project. Возвращает (success: bool, error: bool)"""
        try:
            area = self.get_workspace_area()
            if not area:
                return (False, False)

            width_m = int(area._width_m)
            height_m = int(area._height_m)

            # Используем resize_project вместо rename_project
            worker = AsyncWorker.run_async(
                resize_project(
                    project_id=self._current_project['id'],
                    width=width_m,
                    length=height_m,
                    token=session.token
                )
            )

            # Синхронное ожидание для совместимости с текущей логикой
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                resize_project(
                    project_id=self._current_project['id'],
                    width=width_m,
                    length=height_m,
                    token=session.token
                )
            )
            loop.close()

            # Обновляем локальные данные
            self._current_project['width'] = width_m
            self._current_project['length'] = height_m
            self._current_project['_area_modified'] = False

            print(f"DEBUG: Площадка сохранена: {width_m}x{height_m}")
            return (True, False)

        except Exception as e:
            print(f"DEBUG ERROR: Не удалось сохранить площадку: {e}")
            return (False, True)

    def _save_objects_to_server(self, objects: list) -> tuple:
        """Сохраняет позиции объектов. Возвращает (success_count, error_count)"""
        success_count = 0
        error_count = 0

        for obj in objects:
            if not (hasattr(obj, '_element_id') and obj._element_id):
                continue

            x_m = int(obj.pos().x() / PIXELS_PER_METER)
            y_m = int(obj.pos().y() / PIXELS_PER_METER)

            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                result = loop.run_until_complete(
                    move_element(obj._element_id, x_m, y_m, session.token)
                )
                loop.close()

                obj._is_modified = False
                success_count += 1
                print(f"DEBUG: Сохранена позиция {obj._element_id}: ({x_m}, {y_m})")

            except Exception as e:
                error_count += 1
                print(f"DEBUG ERROR: Не удалось сохранить {obj._element_id}: {e}")

        return (success_count, error_count)

    def _save_text_to_server(self, element_id: int, text: str):
        """Сохраняет название элемента на сервере"""


        worker = AsyncWorker.run_async(
            rename_element(element_id, text, session.token)
        )
        worker.signals.success.connect(
            lambda: print(f"Название сохранено для элемента {element_id}")
        )
        worker.signals.error.connect(
            lambda e: print(f"Ошибка сохранения названия: {e}")
        )

    def _save_color_to_server(self, element_id: int, color: str):
        """Сохраняет цвет элемента на сервере"""

        worker = AsyncWorker.run_async(
            recolor_element(element_id, color, session.token)
        )
        worker.signals.success.connect(
            lambda: print(f"Цвет сохранён для элемента {element_id}")
        )
        worker.signals.error.connect(
            lambda e: print(f"Ошибка сохранения цвета: {e}")
        )

    def _save_size_to_server(self, element_id: int, width: int, length: int):
        """Сохраняет размеры элемента на сервере"""


        worker = AsyncWorker.run_async(
            resize_element(element_id, width, length, session.token)
        )
        worker.signals.success.connect(
            lambda: print(f"Размеры сохранены для элемента {element_id}")
        )
        worker.signals.error.connect(
            lambda e: print(f"Ошибка сохранения размеров: {e}")
        )

    def _save_object_position(self, obj: SnappableObject):
        """Сохраняет позицию объекта на сервере"""
        if not (hasattr(obj, '_element_id') and obj._element_id and session.token):
            return

        x_m = int(obj.pos().x() / PIXELS_PER_METER)
        y_m = int(obj.pos().y() / PIXELS_PER_METER)

        worker = AsyncWorker.run_async(
            move_element(obj._element_id, x_m, y_m, session.token)
        )
        worker.signals.error.connect(lambda e: print(f"Ошибка сохранения позиции: {e}"))