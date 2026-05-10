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
from ..widgets.graphics.zoomable_view import ZoomableGraphicsView

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
        self.graphicsView.polygonDrawn.connect(self._on_custom_polygon_drawn)

        self._drawing_mode = "object"

        self.ui.actionAddObject.triggered.connect(self.add_object_entry)
        self.ui.actionEditObject.triggered.connect(self.edit_object)
        self.ui.actionDeleteObject.triggered.connect(self.delete_object)
        self.ui.actionSetArea.triggered.connect(self.set_area)
        self.ui.actionAddObjectsList.triggered.connect(self.add_objects_list)
        self.ui.action_8.triggered.connect(self.open_auth_dialog)
        self.ui.actionSavePNG.triggered.connect(self.save_project_png)
        self.ui.actionSaveJSON.triggered.connect(self.save_project_json)
        self.ui.deleteTemplateButton.clicked.connect(self.delete_template_from_list)

        self.ui.action_10.triggered.connect(lambda: self.change_theme('light'))
        self.ui.action_11.triggered.connect(lambda: self.change_theme('dark'))
        self.ui.action_12.triggered.connect(lambda: self.change_theme('system'))

        self.statusBar().showMessage("Масштаб: 1 м = 20 пикс. | Сетка: 0.5 м (1 клетка)")
        self.status_label = QLabel("")
        self.statusBar().addPermanentWidget(self.status_label)

        self.update_icons_for_theme(theme_manager.current_theme)

        if project_data:
            self._load_project(project_data)

    def delete_template_from_list(self):
        """Удаляет выбранный шаблон (тип объекта) из выпадающего списка"""
        index = self.ui.comboBox.currentIndex()
        if index < 0:
            QMessageBox.warning(self, "Внимание", "Нет объектов для удаления")
            return

        # Получаем данные выбранного шаблона
        obj_data = self.ui.comboBox.currentData()
        if not obj_data:
            return

        template_name = obj_data.get('name', 'Неизвестный объект')
        type_id = obj_data.get('element_type_id')

        # Спрашиваем подтверждение
        reply = QMessageBox.question(
            self,
            "Удаление объекта",
            f"Удалить '{template_name}' из выпадающего списка?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # 1. Удаляем локально из UI
            self.ui.comboBox.removeItem(index)
            self.statusBar().showMessage(f"Объект '{template_name}' удален из списка", 3000)

            # 2. Если у вас уже есть эндпоинт на сервере для удаления типов — вызываем его
            if type_id and session.token:
                try:
                    from ...api.element_types import delete_element_type
                    worker = AsyncWorker.run_async(delete_element_type(type_id, session.token))

                    if not hasattr(self, '_active_workers'):
                        self._active_workers = set()
                    self._active_workers.add(worker)

                    worker.signals.error.connect(
                        lambda e: QMessageBox.warning(self, "Ошибка API", f"Не удалось удалить шаблон на сервере:\n{e}")
                    )
                    from functools import partial
                    worker.signals.finished.connect(partial(self._cleanup_worker, worker=worker))
                except ImportError:
                    print("API для удаления типа (delete_element_type) еще не реализовано напарником.")

    def add_object_entry(self):
        """Выбор способа добавления объекта: рисование или список"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Добавление объекта")
        msg.setText("Как вы хотите добавить объект на площадку?")

        # Создаем кастомные кнопки
        btn_draw = msg.addButton("Нарисовать полигон", QMessageBox.ButtonRole.ActionRole)
        btn_list = msg.addButton("Добавить из списка", QMessageBox.ButtonRole.ActionRole)
        msg.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        if msg.clickedButton() == btn_draw:
            # Включаем режим рисования объекта (используем твою обертку)
            self._start_drawing_object()

        elif msg.clickedButton() == btn_list:
            # Открываем твой существующий диалог со списком
            self.add_object()

    def _start_drawing_object(self):
        self._drawing_mode = "object"
        self.graphicsView.start_drawing()

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

            # ⭐ ВОССТАНАВЛИВАЕМ ШАБЛОН В COMBOBOX (возвращает цвета и размеры!)
            template_data = {
                'name': elem_data.get('title', 'Объект'),
                'width': float(elem_data.get('width', 6.0)),
                'length': float(elem_data.get('length', 4.0)),
                'color': elem_data.get('color', '#96C8FF'),
                'zone_margin': margin,
                'element_type_id': type_id
            }
            self._add_template_to_combobox(template_data)

            obj = SnappableObject(
                text=elem_data.get('title', 'Объект'),
                width_m=float(elem_data.get('width', 6.0)), # Обязательно float!
                height_m=float(elem_data.get('length', 4.0)),
                color=elem_data.get('color', '#96C8FF'),
                grid_size_m=0.5,
                pixels_per_meter=PIXELS_PER_METER,
                zone_margin_m=margin
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
        self.ui.actionAddObjectsList.setIcon(
            QIcon(get_resource_path(f"Icons/library_add_24dp_{suffix}.svg"))
        )
        self.ui.deleteTemplateButton.setIcon(
            QIcon(get_resource_path(f"Icons/delete_24dp_{suffix}.svg"))
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
                    "length": int(area._height_m),
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
        # Создаем окно с выбором действия
        msg = QMessageBox(self)
        msg.setWindowTitle("Настройка площадки")
        msg.setText("Как вы хотите задать границы площадки?")

        btn_draw = msg.addButton("Нарисовать полигон", QMessageBox.ButtonRole.ActionRole)
        btn_manual = msg.addButton("Ввести размеры", QMessageBox.ButtonRole.ActionRole)
        msg.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        if msg.clickedButton() == btn_draw:
            # Включаем режим рисования площадки
            self._drawing_mode = "area"
            self.graphicsView.start_drawing()

        elif msg.clickedButton() == btn_manual:
            # Старая логика с текстовыми полями
            dialog = SetAreaWindow(self)
            if dialog.exec() == SetAreaWindow.Accepted:
                width, height = dialog.get_values()
                if width and height:
                    self.set_workspace_area(width, height)
                    if self._current_project:
                        self._current_project['width'] = width
                        self._current_project['length'] = height
                        self._current_project['_area_modified'] = True
                        self.statusBar().showMessage(
                            f"Площадка изменена: {width}×{height} м (нажмите 💾 для сохранения)",
                            5000
                        )

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

        # Получаем контур площадки в координатах сцены
        area_path = area.mapToScene(area.shape())

        # Проверяем сам объект
        obj_body_path = obj.mapToScene(obj.bodyPath())
        # Если площадка не содержит полностью контур объекта
        is_obj_outside = not area_path.contains(obj_body_path)
        obj.set_outside_area(is_obj_outside)

        # Проверяем зону обслуживания
        if obj._zone_margin_m > 0:
            obj_zone_path = obj.mapToScene(obj.zonePath())
            is_zone_outside = not area_path.contains(obj_zone_path)
            obj.set_zone_outside_area(is_zone_outside)
        else:
            obj.set_zone_outside_area(is_obj_outside)

        return is_obj_outside

    def check_object_collisions(self):
        objects = [item for item in self.scene.items() if isinstance(item, SnappableObject)]

        for obj in objects:
            obj.set_overlapping(False)
            obj.set_zone_overlapping(False)

        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects):
                if i >= j:
                    continue

                body1_path = obj1.mapToScene(obj1.bodyPath())
                body2_path = obj2.mapToScene(obj2.bodyPath())

                # Пересекаются ли пути (контуры)
                if body1_path.intersects(body2_path):
                    obj1.set_overlapping(True)
                    obj2.set_overlapping(True)

                zone1_path = obj1.mapToScene(obj1.zonePath())
                zone2_path = obj2.mapToScene(obj2.zonePath())

                if zone1_path.intersects(zone2_path):
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
        """Обновления UI при перемещении и отложенное сохранение (Debounce)"""
        obj._is_modified = True  # Помечаем как изменённый
        self.check_object_bounds(obj)
        self.check_object_collisions()
        self.update_status_bar()

        # Если у объекта еще нет ID (он не сохранен на сервере), пропускаем
        if not hasattr(obj, '_element_id') or not obj._element_id:
            return

        element_id = obj._element_id

        # Создаем словарь таймеров, если его еще нет
        if not hasattr(self, '_save_timers'):
            self._save_timers = {}

        # Если таймер для этого объекта уже запущен — останавливаем его
        if element_id in self._save_timers:
            self._save_timers[element_id].stop()
        else:
            # Если таймера нет, создаем новый
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(partial(self._execute_save_position, obj, element_id))
            self._save_timers[element_id] = timer

        # Запускаем таймер заново. Если вы будете непрерывно двигать мышь,
        # таймер будет постоянно сбрасываться и запрос не уйдет.
        # Как только вы остановитесь на 500 мс, таймер сработает и сохранит позицию.
        self._save_timers[element_id].start(MOVE_DEBOUNCE_MS)

    def _execute_save_position(self, obj, element_id):
        """Вызывается по истечении таймера Debounce для сохранения"""
        # Удаляем отработавший таймер
        if element_id in self._save_timers:
            del self._save_timers[element_id]

        # Запускаем ваш готовый метод сохранения на сервер!
        self._save_object_position(obj)

    def add_object(self):
        """Добавляет выбранный из combobox объект на сцену"""
        if not self._current_project or not session.token:
            QMessageBox.warning(self, "Ошибка", "Нет активного проекта")
            return

        index = self.ui.comboBox.currentIndex()
        if index < 0:
            QMessageBox.warning(self, "Ошибка", "Сначала добавьте объекты через диалог (+)")
            return

        obj_data = self.ui.comboBox.currentData()
        if not obj_data:
            return

        self.statusBar().showMessage("Создание объекта...", 3000)

        center_pos = self.get_viewport_center_scene_pos()
        x_pos = int(center_pos.x() / PIXELS_PER_METER)
        y_pos = int(center_pos.y() / PIXELS_PER_METER)

        # ⭐ Используем ID типа из данных объекта, а не жесткую единицу
        type_id = obj_data.get('element_type_id', 1)

        worker = AsyncWorker.run_async(add_elements(
            project_id=self._current_project['id'],
            element_type_id=type_id,
            x=x_pos,
            y=y_pos,
            width=float(obj_data['width']), # Используем float для точности
            length=float(obj_data['length']),
            title=obj_data['name'],
            color=obj_data['color'],
            token=session.token
        ))

        # ⭐ ЗАЩИТА ОТ GC: Обязательно добавляем в активные воркеры
        if not hasattr(self, '_active_workers'):
            self._active_workers = set()
        self._active_workers.add(worker)

        zone = float(obj_data.get('zone_margin', 0.0))
        worker.signals.success.connect(
            partial(self._on_object_created, zone_margin=zone)
        )
        worker.signals.error.connect(self._on_object_create_error)
        worker.signals.finished.connect(partial(self._cleanup_worker, worker=worker))

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
        """Добавляет объект в combobox или обновляет существующий шаблон"""
        name = obj_data.get('name', 'Объект')

        # Проверяем, есть ли уже такой шаблон
        for i in range(self.ui.comboBox.count()):
            if self.ui.comboBox.itemText(i) == name:
                # ⭐ Если имя совпало, обновляем данные (включая зону) и выходим
                self.ui.comboBox.setItemData(i, obj_data)
                return

                # Если шаблона нет, добавляем новый
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
                # Берем новые значения или оставляем старые, если они не менялись
                new_length = changes.get("length", item._width_m)
                new_width = changes.get("width", item._height_m)

                # Вызываем наш новый умный метод масштабирования
                item.update_size(new_length, new_width)

                item._is_modified = True
                save_queue.append(('resize', element_id, float(item._width_m), float(item._height_m)))

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

    def _on_custom_polygon_drawn(self, points_scene_m: list):
        """Диспетчер: решает, что создавать по завершении рисования"""
        if getattr(self, '_drawing_mode', 'object') == 'area':
            self._create_custom_area(points_scene_m)
        else:
            self._create_custom_object(points_scene_m)

        # Возвращаем режим по умолчанию
        self._drawing_mode = "object"

    def _create_custom_object(self, points_scene_m: list):
        """Создает SnappableObject на основе нарисованного полигона"""
        # 1. Вычисляем исходные габариты нарисованного полигона
        min_x = min(pt[0] for pt in points_scene_m)
        min_y = min(pt[1] for pt in points_scene_m)
        max_x = max(pt[0] for pt in points_scene_m)
        max_y = max(pt[1] for pt in points_scene_m)

        width_m = max_x - min_x
        height_m = max_y - min_y
        local_polygon_m = [(pt[0] - min_x, pt[1] - min_y) for pt in points_scene_m]

        default_name = f"Полигон {len(self._elements_map) + 1}"

        # 2. ВЫЗЫВАЕМ ДИАЛОГ СОЗДАНИЯ (сразу после рисования)
        dialog = EditObjectWindow(
            self,
            initial_text=default_name,
            initial_length=width_m,
            initial_width=height_m,
            initial_color="#BB86FC",
            initial_zone=0.0,
            is_creation=True  # ⭐ ГЛАВНЫЙ ФЛАГ: Разрешает задать зону!
        )

        # Если пользователь нажал "Отмена" - прерываем создание
        if dialog.exec() != QDialog.Accepted:
            self.statusBar().showMessage("Создание объекта отменено", 3000)
            return

        # 3. Получаем данные, которые ввел пользователь
        changes = dialog.get_data()
        name = changes.get("text", default_name)
        color = changes.get("color", "#BB86FC")
        zone_margin = changes.get("zone_margin", 0.0)  # ⭐ Считываем зону

        # 4. Создаем объект
        obj = SnappableObject(
            text=name,
            width_m=width_m,
            height_m=height_m,
            polygon_m=local_polygon_m,
            color=color,
            grid_size_m=0.5,
            pixels_per_meter=PIXELS_PER_METER,
            zone_margin_m=zone_margin  # ⭐ Применяем зону к полигону
        )

        # 5. Умное масштабирование (если пользователь вдруг изменил ширину/длину в диалоге)
        if "length" in changes or "width" in changes:
            new_length = changes.get("length", width_m)
            new_width = changes.get("width", height_m)
            obj.update_size(new_length, new_width)

        # 6. Регистрируем и размещаем на сцене
        obj._element_id = f"custom_temp_{len(self._elements_map)}"
        obj._element_type_id = None
        obj._is_modified = True

        x_px = min_x * PIXELS_PER_METER
        y_px = min_y * PIXELS_PER_METER
        obj.setPos(x_px, y_px)

        self.scene.addItem(obj)
        self._elements_map[obj._element_id] = obj

        obj.geometryChanged.connect(lambda: self._on_object_moved_ui(obj))

        self.check_object_bounds(obj)
        self.check_object_collisions()
        self.update_status_bar()
        self.scene.update()

        self.statusBar().showMessage(f"Объект '{name}' успешно создан!", 3000)

    def _create_custom_area(self, points_scene_m: list):
        """Создает полигональную площадку WorkspaceArea"""
        min_x = min(pt[0] for pt in points_scene_m)
        min_y = min(pt[1] for pt in points_scene_m)
        max_x = max(pt[0] for pt in points_scene_m)
        max_y = max(pt[1] for pt in points_scene_m)

        width_m = max_x - min_x
        height_m = max_y - min_y

        # Нормализуем координаты площадки
        local_polygon_m = [(pt[0] - min_x, pt[1] - min_y) for pt in points_scene_m]

        # Удаляем старую площадку со сцены
        for item in self.scene.items():
            if isinstance(item, WorkspaceArea):
                self.scene.removeItem(item)

        # Создаем новую полигональную площадку
        area = WorkspaceArea(polygon_m=local_polygon_m)
        self.scene.addItem(area)

        # Размещаем ее точно там, где кликал пользователь
        area.setPos(min_x * PIXELS_PER_METER, min_y * PIXELS_PER_METER)

        # Обновляем данные проекта
        if self._current_project:
            self._current_project['width'] = width_m
            self._current_project['length'] = height_m
            self._current_project['vertices'] = local_polygon_m  # Сохраняем вершины для JSON/БД
            self._current_project['_area_modified'] = True

        # После изменения площадки, нужно ПЕРЕПРОВЕРИТЬ все объекты на сцене!
        # Вдруг площадка сузилась, и объекты оказались за бортом
        for obj in self._elements_map.values():
            self.check_object_bounds(obj)

        self.check_object_collisions()
        self.update_status_bar()
        self.scene.update()

        self.statusBar().showMessage("Полигональная площадка успешно создана! (нажмите 💾 для сохранения)", 5000)

    def _process_save_queue(self):
        """Обрабатывает очередь сохранений последовательно"""
        if not hasattr(self, '_pending_save_queue') or not self._pending_save_queue:
            self.statusBar().showMessage("Все изменения сохранены", 3000)
            return

        save_task = self._pending_save_queue.pop(0)
        save_type, element_id, *args = save_task

        print(f"DEBUG: Processing {save_type} for element {element_id}")

        if save_type == 'rename':
            worker = AsyncWorker.run_async(rename_element(element_id, args[0], session.token))
        elif save_type == 'recolor':
            worker = AsyncWorker.run_async(recolor_element(element_id, args[0], session.token))
        elif save_type == 'resize':
            worker = AsyncWorker.run_async(resize_element(element_id, args[0], args[1], session.token))
        else:
            self._process_save_queue()
            return

        # ⭐ ЗАЩИТА ОТ GC (Сборщика мусора)
        if not hasattr(self, '_active_workers'):
            self._active_workers = set()
        self._active_workers.add(worker)

        from functools import partial
        worker.signals.success.connect(partial(self._on_save_success, save_type, element_id))
        worker.signals.error.connect(partial(self._on_save_error, save_type, element_id))

        # Обязательно удаляем воркер после завершения
        worker.signals.finished.connect(partial(self._cleanup_worker, worker=worker))

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
                    worker = AsyncWorker.run_async(delete_element(element_id, session.token))

                    # ⭐ ЗАЩИТА ОТ GC
                    if not hasattr(self, '_active_workers'):
                        self._active_workers = set()
                    self._active_workers.add(worker)

                    worker.signals.error.connect(self._on_delete_error)

                    from functools import partial
                    worker.signals.finished.connect(partial(self._cleanup_worker, worker=worker))

    def _remove_from_scene(self, item):
        self.scene.removeItem(item)
        if hasattr(item, '_element_id'):
            element_id = item._element_id
            if element_id in self._elements_map:
                del self._elements_map[element_id]

            # ⭐ Отменяем автосохранение, если объект был удален
            if hasattr(self, '_save_timers') and element_id in self._save_timers:
                self._save_timers[element_id].stop()
                del self._save_timers[element_id]

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

        worker = AsyncWorker.run_async(move_element(obj._element_id, x_m, y_m, session.token))

        # ⭐ ЗАЩИТА ОТ GC
        if not hasattr(self, '_active_workers'):
            self._active_workers = set()
        self._active_workers.add(worker)

        worker.signals.error.connect(lambda e: print(f"Ошибка сохранения позиции: {e}"))

        from functools import partial
        worker.signals.finished.connect(partial(self._cleanup_worker, worker=worker))