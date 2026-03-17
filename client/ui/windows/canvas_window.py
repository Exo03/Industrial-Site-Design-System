import json
from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QMessageBox, QFileDialog,
    QStyleOptionGraphicsItem, QStyle, QApplication, QGraphicsView
)
from PySide6.QtCore import Qt, QStandardPaths, QSize, QTimer
from PySide6.QtGui import QPainter, QImage, QTransform
from PySide6.scripts.project_lib import project_data

from UI_Files.MainWindow import Ui_MainWindow
from ...api.element_types import get_element_types
from ...api.elements import get_project_elements, move_element, delete_element, recolor_element, resize_element, \
    add_elements
from ...api.projects import rename_project
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

        self.graphicsView.centerOn(500, 500)
        self.ui.graphicsView = self.graphicsView

        self.ui.graphicsView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.ui.graphicsView.centerOn(500, 500)

        self.ui.actionAddObject.triggered.connect(self.add_object)
        self.ui.actionEditObject.triggered.connect(self.edit_object)
        self.ui.actionDeleteObject.triggered.connect(self.delete_object)
        self.ui.actionSetArea.triggered.connect(self.set_area)
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

        if project_data:
            self._load_project(project_data)

    def _load_element_types(self):
        if not session.token:
            return

        worker = AsyncWorker.run_async(get_element_types())
        worker.signals.success.connect(self._on_types_loaded)
        worker.signals.error.connect(lambda e: print(f"Ошибка загрузки типов: {e}"))

    def _on_types_loaded(self, types: list):
        self._element_types = types
        self.ui.comboBox.clear()

        for etype in types:
            self.ui.comboBox.addItem(etype['title'], etype['id'])  # Сохраняем ID в data

    def _load_project(self, project_data: dict):
        self._current_project = project_data
        self.setWindowTitle(f"Industrial Designer - {project_data['name']}")

        if self._current_project:
            self._current_project['_area_modified'] = False

        if project_data.get('width') and project_data.get('length'):
            self.set_workspace_area(project_data['width'], project_data['length'])

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
        for item in list(self.scene.items()):  # list() для безопасного удаления
            if isinstance(item, SnappableObject):
                self.scene.removeItem(item)

        self._elements_map.clear()

        # Площадку НЕ трогаем, она уже создана в _load_project
        # Но если вдруг нет — создаём
        if not self.get_workspace_area() and self._current_project:
            width = self._current_project.get('width', 50)
            length = self._current_project.get('length', 50)
            if width and length:
                self.set_workspace_area(width, length)

        # Создаём объекты
        for elem_data in elements:
            obj = SnappableObject(
                text=elem_data.get('title', 'Объект'),
                width_m=elem_data.get('width', 6.0),
                height_m=elem_data.get('length', 4.0),
                color=elem_data.get('color', '#96C8FF'),
                grid_size_m=0.5,
                pixels_per_meter=PIXELS_PER_METER
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

        self.check_object_collisions()
        self.update_status_bar()
        self.statusBar().showMessage(f"Загружено элементов: {len(elements)}", 3000)

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
        try:
            project_data = {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "project_name": "New Project",
                "settings": {
                    "pixels_per_meter": PIXELS_PER_METER,
                    "grid_size": self.scene._grid_size
                }
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)

            self.current_project_path = file_path
            self.statusBar().showMessage(f"✓ Сохранено: {file_path}", 5000)
            QMessageBox.information(self, "Успех", f"Проект сохранён:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить JSON:\n{e}")

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

        # Центр видимой области
        center_pos = self.get_viewport_center_scene_pos()

        # Центрируем площадку относительно видимой области
        area_width_px = width_m * PIXELS_PER_METER
        area_height_px = height_m * PIXELS_PER_METER

        area.setPos(
            center_pos.x() - area_width_px / 2,
            center_pos.y() - area_height_px / 2
        )

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
            return False

        obj_rect = obj.mapToScene(obj.boundingRect()).boundingRect()
        area_rect = area.mapToScene(area.boundingRect()).boundingRect()

        is_outside = not area_rect.contains(obj_rect)
        obj.set_outside_area(is_outside)
        return is_outside

    def check_object_collisions(self):
        objects = [item for item in self.scene.items() if isinstance(item, SnappableObject)]

        for obj in objects:
            obj.set_overlapping(False)

        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects):
                if i >= j:
                    continue
                obj1_rect = obj1.mapToScene(obj1.boundingRect()).boundingRect()
                obj2_rect = obj2.mapToScene(obj2.boundingRect()).boundingRect()

                if obj1_rect.intersects(obj2_rect):
                    obj1.set_overlapping(True)
                    obj2.set_overlapping(True)

    def _on_object_moved_ui(self, obj: SnappableObject):
        """Только UI обновления при перемещении, без отправки на сервер"""
        obj._is_modified = True  # Помечаем как изменённый
        self.check_object_bounds(obj)
        self.check_object_collisions()
        self.update_status_bar()

    def add_object(self):
        """Добавляет объект на сервер и на сцену"""
        if not self._current_project or not session.token:
            QMessageBox.warning(self, "Ошибка", "Нет активного проекта")
            return

        index = self.ui.comboBox.currentIndex()
        if index < 0 or not self._element_types:
            QMessageBox.warning(self, "Ошибка", "Выберите тип оборудования")
            return

        element_type_id = self.ui.comboBox.currentData()
        selected_type = self.ui.comboBox.currentText()

        # Центр видимой области в координатах сцены (в метрах)
        center_pos = self.get_viewport_center_scene_pos()
        x_pos = center_pos.x() / PIXELS_PER_METER
        y_pos = center_pos.y() / PIXELS_PER_METER

        self.statusBar().showMessage("Создание объекта...", 3000)

        worker = AsyncWorker.run_async(add_elements(
            project_id=self._current_project['id'],
            element_type_id=element_type_id,
            x=int(x_pos), y=int(y_pos),
            width=6, length=4,
            title=selected_type,
            color="#96C8FF",
            token=session.token
        ))

        worker.signals.success.connect(self._on_object_created)
        worker.signals.error.connect(self._on_object_create_error)

    def _on_object_created(self, element_data: dict):
        """Добавляет созданный объект на сцену по центру видимой области"""
        if not element_data or 'id' not in element_data:
            QMessageBox.critical(self, "Ошибка", "Сервер вернул некорректные данные")
            return

        obj = SnappableObject(
            text=element_data.get('title', 'Объект'),
            width_m=float(element_data.get('width', 6.0)),
            height_m=float(element_data.get('length', 4.0)),
            color=element_data.get('color', '#96C8FF'),
            grid_size_m=0.5,
            pixels_per_meter=PIXELS_PER_METER
        )

        obj._element_id = element_data['id']
        obj._element_type_id = element_data.get('element_type_id')
        obj._is_modified = False

        # Только UI обновления при перемещении
        obj.geometryChanged.connect(lambda: self._on_object_moved_ui(obj))

        # Центр видимой области (там, где пользователь смотрит)
        center_pos = self.get_viewport_center_scene_pos()

        # Центрируем объект (учитываем его размер)
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

        self.statusBar().showMessage(f"Добавлен объект: {obj._text} (ID: {obj._element_id})", 3000)

        # Сразу сохраняем позицию на сервере
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

    def update_status_bar(self):
        area = self.get_workspace_area()
        outside_names = []
        overlapping_names = []

        for item in self.scene.items():
            if isinstance(item, SnappableObject):
                if item._is_outside_area:
                    outside_names.append(item._text)
                if item._is_overlapping:
                    overlapping_names.append(item._text)

        messages = []
        if outside_names:
            messages.append("⚠️ Вне площадки: " + ", ".join(outside_names))
        if overlapping_names:
            messages.append("🟡 Пересекаются: " + ", ".join(overlapping_names))

        self.status_label.setText(" | ".join(messages) if messages else "")

    def edit_object(self):
        selected = self.scene.selectedItems()
        if not selected:
            return

        # Берем первый выделенный объект для получения начальных значений
        first_item = selected[0]
        if not isinstance(first_item, SnappableObject):
            return

        # Открываем диалог с параметрами первого объекта
        dlg = EditObjectWindow(
            self,
            initial_text=first_item._text,
            initial_length=first_item._width_m,
            initial_width=first_item._height_m,
            initial_color=first_item._color.name()
        )

        if dlg.exec() != EditObjectWindow.Accepted:
            return

        changes = dlg.get_data()
        if not changes:
            return

        # Применяем изменения ко ВСЕМ выделенным объектам и сохраняем на сервере
        modified_count = 0
        for item in selected:
            if not isinstance(item, SnappableObject):
                continue

            element_id = getattr(item, '_element_id', None)
            if not element_id:
                continue

            # Применяем изменения локально
            if "text" in changes:
                item.update_text(changes["text"])
                item._is_modified = True
                # Сохраняем на сервере
                self._save_text_to_server(element_id, changes["text"])

            if "length" in changes:
                item._width_m = changes["length"]
                item._is_modified = True

            if "width" in changes:
                item._height_m = changes["width"]
                item._is_modified = True

            # Сохраняем размеры, если изменились
            if "length" in changes or "width" in changes:
                item.prepareGeometryChange()
                item.update()
                self._save_size_to_server(
                    element_id,
                    int(item._width_m),
                    int(item._height_m)
                )

            if "color" in changes:
                item.update_color(changes["color"])
                item._is_modified = True
                # Сохраняем на сервере
                self._save_color_to_server(element_id, changes["color"])

            self.check_object_bounds(item)
            modified_count += 1

        # Проверяем коллизии для всех объектов после изменения всех размеров
        self.check_object_collisions()
        self.update_status_bar()

        self.statusBar().showMessage(
            f"Изменения применены и сохранены для {modified_count} объектов.",
            3000
        )

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
        """Сохраняет размеры площадки. Возвращает (success: bool, error: bool)"""
        try:
            area = self.get_workspace_area()
            if not area:
                return (False, False)  # Нет площадки для сохранения

            width_m = int(area._width_m)
            height_m = int(area._height_m)

            # Используем AsyncWorker вместо синхронного вызова
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            result = loop.run_until_complete(rename_project(
                project_id=self._current_project['id'],
                name=self._current_project.get('name', 'Без названия'),
                description=self._current_project.get('description', ''),
                width=width_m,
                length=height_m,
                token=session.token
            ))
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