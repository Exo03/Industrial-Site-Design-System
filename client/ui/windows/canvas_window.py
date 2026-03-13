import json
from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QMessageBox, QFileDialog,
    QStyleOptionGraphicsItem, QStyle, QApplication, QGraphicsView
)
from PySide6.QtCore import Qt, QStandardPaths, QSize
from PySide6.QtGui import QPainter, QImage, QTransform

from UI_Files.MainWindow import Ui_MainWindow
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

class CanvasWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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

        # Подключаем действия
        self.ui.actionAddObject.triggered.connect(self.add_object)
        self.ui.actionEditObject.triggered.connect(self.edit_object)
        self.ui.actionDeleteObject.triggered.connect(self.delete_object)
        self.ui.actionSetArea.triggered.connect(self.set_area)
        self.ui.action_8.triggered.connect(self.open_auth_dialog)
        self.ui.actionSavePNG.triggered.connect(self.save_project_png)
        self.ui.actionSaveJSON.triggered.connect(self.save_project_json)

        # Темы
        self.ui.action_10.triggered.connect(lambda: self.change_theme('light'))
        self.ui.action_11.triggered.connect(lambda: self.change_theme('dark'))
        self.ui.action_12.triggered.connect(lambda: self.change_theme('system'))

        self.statusBar().showMessage("Масштаб: 1 м = 20 пикс. | Сетка: 0.5 м (1 клетка)")
        self.status_label = QLabel("")
        self.statusBar().addPermanentWidget(self.status_label)

        session.logged_in.connect(self._on_logged_in)
        session.logged_out.connect(self._on_logged_out)

    def change_theme(self, theme: str):

        if theme == 'system':
            theme = 'dark'
        theme_manager.apply_theme(theme)
        self.update_icons_for_theme(theme)

    def update_icons_for_theme(self, theme: str):
        from PySide6.QtGui import QIcon
        suffix = "FFFFFF" if theme == "dark" else "000000"
        self.ui.actionAddObject.setIcon(QIcon(f"Icons/add_24dp_{suffix}.svg"))
        self.ui.actionEditObject.setIcon(QIcon(f"Icons/edit_24dp_{suffix}.svg"))
        self.ui.actionDeleteObject.setIcon(QIcon(f"Icons/delete_24dp_{suffix}.svg"))
        self.ui.actionSetArea.setIcon(QIcon(f"Icons/activity_zone_24dp_{suffix}.svg"))

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

    def set_workspace_area(self, width_m, height_m):
        for item in self.scene.items():
            if isinstance(item, WorkspaceArea):
                self.scene.removeItem(item)

        area = WorkspaceArea(width_m, height_m)
        self.scene.addItem(area)

        scene_rect = self.scene.sceneRect()
        center_x = scene_rect.width() / 2 - (width_m * PIXELS_PER_METER) / 2
        center_y = scene_rect.height() / 2 - (height_m * PIXELS_PER_METER) / 2
        area.setPos(center_x, center_y)

    def get_workspace_area(self):
        for item in self.scene.items():
            if isinstance(item, WorkspaceArea):
                return item
        return None

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

    def add_object(self):
        selected_type = self.ui.comboBox.currentText().strip() or "Объект"
        obj = SnappableObject(
            text=selected_type,
            width_m=6.0,
            height_m=4.0,
            color="#96C8FF",
            grid_size_m=0.5,
            pixels_per_meter=PIXELS_PER_METER
        )
        obj.geometryChanged.connect(lambda: self.on_object_moved(obj))
        self.scene.addItem(obj)
        obj.setPos(400, 400)
        self.check_object_bounds(obj)
        self.check_object_collisions()
        self.update_status_bar()

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

        item = selected[0]
        if not isinstance(item, SnappableObject):
            return

        cur_text = item._text
        cur_color = item._color.name()
        cur_w_m = item._width_m
        cur_h_m = item._height_m

        dlg = EditObjectWindow(
            self,
            initial_text=cur_text,
            initial_length=cur_w_m,
            initial_width=cur_h_m,
            initial_color=cur_color
        )
        if dlg.exec() != EditObjectWindow.Accepted:
            return

        changes = dlg.get_data()
        if not changes:
            return

        if "text" in changes:
            item.update_text(changes["text"])
        if "length" in changes:
            item._width_m = changes["length"]
        if "width" in changes:
            item._height_m = changes["width"]
        if "color" in changes:
            item.update_color(changes["color"])

        if "length" in changes or "width" in changes:
            item.prepareGeometryChange()
            item.update()

        if any(k in changes for k in ["length", "width", "text", "color"]):
            self.check_object_bounds(item)
            self.check_object_collisions()
            self.update_status_bar()

    def delete_object(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)