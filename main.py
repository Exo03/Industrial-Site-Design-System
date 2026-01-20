from PySide6.QtCore import QPointF, QRectF, Qt, QLocale
from PySide6.QtGui import QBrush, QColor, QFont, QPen, QPainter, QWheelEvent, QTransform, QDoubleValidator
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsItem, QGraphicsObject, QDialog, QColorDialog,
    QVBoxLayout, QLabel, QStatusBar, QMenuBar, QMenu, QToolBar,
    QWidget, QComboBox, QHBoxLayout
)

from UI_Files.EditObjectWindow import Ui_Object_edit
from UI_Files.MainWindow import Ui_MainWindow

PIXELS_PER_METER = 20

class EditObjectWindow(QDialog):
    def __init__(self, parent=None, initial_text="", initial_length=120, initial_width=80, initial_color="#96C8FF"):
        super().__init__(parent)
        self.ui = Ui_Object_edit()
        self.ui.setupUi(self)

        self._initial_text = initial_text
        self._initial_length = initial_length
        self._initial_width = initial_width
        self._initial_color = initial_color

        self.ui.textLineEdit.setText(initial_text)
        self.ui.lengthLineEdit.setText(str(initial_length))
        self.ui.widthLineEdit.setText(str(initial_width))
        self.ui.colorDisplay.setText(initial_color)
        self.update_color_display(initial_color)

        self.ui.colorChooseButton.clicked.connect(self.open_color_dialog)

        double_validator = QDoubleValidator(0.1, 9999.99, 2)  # от 0.1 до 9999.99, 2 знака после запятой
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        double_validator.setLocale(QLocale(QLocale.English)) # Разделитель - точка

        self.ui.lengthLineEdit.setValidator(double_validator)
        self.ui.widthLineEdit.setValidator(double_validator)

    def open_color_dialog(self):
        current_color = QColor(self.ui.colorDisplay.text().strip() or "#96C8FF")
        dialog = QColorDialog(current_color, self)
        dialog.setStyleSheet("""
            QDialog { background-color: #1E1E1E; color: #FFFFFF; }
            QLabel { color: #FFFFFF; }
            QPushButton {
                background-color: #2A2A2A; color: #FFFFFF;
                border: 1px solid #333333; border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover { background-color: #333333; }
            QPushButton:pressed { background-color: #BB86FC; color: black; }
            QLineEdit, QSpinBox { background-color: #2A2A2A; color: #FFFFFF; border: 1px solid #333333; }
        """)
        if dialog.exec() == QDialog.Accepted:
            color = dialog.currentColor()
            if color.isValid():
                hex_color = color.name()
                self.ui.colorDisplay.setText(hex_color)
                self.update_color_display(hex_color)

    def update_color_display(self, hex_color):
        color = QColor(hex_color)
        text_color = "black" if color.lightness() > 128 else "white"
        self.ui.colorDisplay.setStyleSheet(f"""
            background-color: {hex_color};
            color: {text_color};
            border: 1px solid #333333;
            border-radius: 4px;
            padding: 6px 8px;
        """)
    #Функция сгенерирована ии
    def get_data(self):
        data = {}

        text = self.ui.textLineEdit.text().strip()
        if text != self._initial_text:
            data["text"] = text

        try:
            length = float(self.ui.lengthLineEdit.text())
            if length > 0 and abs(length - self._initial_length) > 1e-6:
                data["length"] = length
        except ValueError:
            pass

        try:
            width = float(self.ui.widthLineEdit.text())
            if width > 0 and abs(width - self._initial_width) > 1e-6:
                data["width"] = width
        except ValueError:
            pass

        color_hex = self.ui.colorDisplay.text().strip()
        if color_hex != self._initial_color and QColor(color_hex).isValid():
            data["color"] = color_hex

        return data

#Класс сгенерирован ИИ
class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)  # Управляем вручную
        self._panning = False
        self._last_pan_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._panning = True
            self._last_pan_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning and self._last_pan_pos:
            delta = event.position() - self._last_pan_pos
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - int(delta.x())
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - int(delta.y())
            )
            self._last_pan_pos = event.position()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta != 0:
                zoom_factor = 1.25 if delta > 0 else 1 / 1.25
                self.scale(zoom_factor, zoom_factor)
                event.accept()
        else:
            # Прокрутка колёсиком без Ctrl
            super().wheelEvent(event)


#Класс сгенерирован ИИ
class GridScene(QGraphicsScene):
    def __init__(self, grid_size=10, parent=None):
        super().__init__(parent)
        self._grid_size = grid_size
        self.setSceneRect(0, 0, 1000, 1000)

    def drawBackground(self, painter, rect):
        # Вызываем родительский метод, если нужно
        super().drawBackground(painter, rect)

        # Настройка пера для сетки
        grid_pen = QPen(QColor(60, 60, 60))  # Тёмно-серый
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)

        # Получаем видимую область
        left = int(rect.left()) - (int(rect.left()) % self._grid_size)
        top = int(rect.top()) - (int(rect.top()) % self._grid_size)

        # Рисуем вертикальные линии
        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += self._grid_size

        # Рисуем горизонтальные линии
        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += self._grid_size


#Класс сгенерирован ИИ
class SnappableObject(QGraphicsObject):
    def __init__(self, text="Объект", width_m=6.0, height_m=4.0, color="#96C8FF", grid_size_m=0.5, pixels_per_meter=PIXELS_PER_METER, parent=None):
        super().__init__(parent)
        self._pixels_per_meter = pixels_per_meter
        self._grid_size_m = grid_size_m
        self._width_m = width_m
        self._height_m = height_m
        self._text = text
        self._color = QColor(color)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def _px(self, meters):
        return meters * self._pixels_per_meter

    def boundingRect(self):
        return QRectF(0, 0, self._px(self._width_m), self._px(self._height_m))

    def paint(self, painter, option, widget=None):
        w_px = self._px(self._width_m)
        h_px = self._px(self._height_m)

        painter.setBrush(QBrush(self._color))
        painter.setPen(QPen(QColor(0, 0, 0, 150)))
        painter.drawRect(0, 0, w_px, h_px)

        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))
        text_rect = QRectF(0, 0, w_px, h_px)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self._text)

        if self.isSelected():
            pen = QPen(Qt.white)
            pen.setWidth(1)
            pen.setStyle(Qt.DashLine)  # Пунктир — стандарт для выделения
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)  # Не закрашиваем внутри
            painter.drawRect(0, 0, w_px, h_px)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            grid_px = self._px(self._grid_size_m)
            x = round(value.x() / grid_px) * grid_px
            y = round(value.y() / grid_px) * grid_px
            return QPointF(x, y)
        return super().itemChange(change, value)

    def update_text(self, text):
        self._text = text
        self.update()

    def update_size(self, width_m, height_m):
        self._width_m = width_m
        self._height_m = height_m
        self.prepareGeometryChange()
        self.update()

    def update_color(self, color):
        self._color = QColor(color)
        self.update()

class CanvasWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
        self.ui.graphicsView.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.ui.graphicsView.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.ui.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ui.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.ui.graphicsView.setTransform(QTransform())

        self.ui.graphicsView.centerOn(500, 500)

        self.ui.actionAddObject.triggered.connect(self.add_object)
        self.ui.actionEditObject.triggered.connect(self.edit_object)
        self.ui.actionDeleteObject.triggered.connect(self.delete_object)

        self.statusBar().showMessage("Масштаб: 1 м = 20 пикс. | Сетка: 0.5 м (1 клетка)")

    #Метод сгенерирован ИИ
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
        self.scene.addItem(obj)
        obj.setPos(400, 400)

    # Метод сгенерирован ИИ
    def edit_object(self):
        print("🔧 edit_object: started")
        selected = self.scene.selectedItems()
        if not selected:
            print("⚠️ No items selected")
            return

        item = selected[0]
        if not isinstance(item, SnappableObject):
            print("⚠️ Selected item is not editable")
            return

        # Текущие параметры
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
        if dlg.exec() != QDialog.Accepted:
            return

        changes = dlg.get_data()
        if not changes:
            return

        # Применяем изменения
        if "text" in changes:
            item.update_text(changes["text"])
        if "length" in changes:
            item._width_m = changes["length"]
        if "width" in changes:
            item._height_m = changes["width"]
        if "color" in changes:
            item.update_color(changes["color"])

        # Обновляем геометрию
        if "length" in changes or "width" in changes:
            item.prepareGeometryChange()
            item.update()

        print("✅ edit_object: completed")

    def delete_object(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CanvasWindow()
    window.show()
    sys.exit(app.exec())