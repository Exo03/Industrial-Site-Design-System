from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPen, QPainter, QWheelEvent, QTransform
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsItem, QGraphicsObject, QDialog, QColorDialog,
    QVBoxLayout, QLabel, QStatusBar, QMenuBar, QMenu, QToolBar,
    QWidget, QComboBox, QHBoxLayout
)

from UI_Files.EditObjectWindow import Ui_Object_edit
from UI_Files.MainWindow import Ui_MainWindow

class EditObjectWindow(QDialog):
    def __init__(self, parent=None, initial_text="", initial_length=120, initial_width=80, initial_color="#96C8FF"):
        super().__init__(parent)
        self.ui = Ui_Object_edit()
        self.ui.setupUi(self)

        # Сохраняем начальные значения для сравнения
        self._initial_text = initial_text
        self._initial_length = initial_length
        self._initial_width = initial_width
        self._initial_color = initial_color

        # Заполняем поля — через self.ui.*
        self.ui.textLineEdit.setText(initial_text)
        self.ui.lengthLineEdit.setText(str(initial_length))
        self.ui.widthLineEdit.setText(str(initial_width))
        self.ui.colorDisplay.setText(initial_color)
        self.update_color_display(initial_color)

        # Подключаем кнопку выбора цвета
        self.ui.colorChooseButton.clicked.connect(self.open_color_dialog)

    def open_color_dialog(self):
        current_color = QColor(self.ui.colorDisplay.text().strip() or "#96C8FF")
        dialog = QColorDialog(current_color, self)
        # Стилизуем под твою тему:
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

    def get_data(self):
        """Возвращает ТОЛЬКО изменённые поля."""
        data = {}

        text = self.ui.textLineEdit.text().strip()
        if text != self._initial_text:
            data["text"] = text

        try:
            length = int(self.ui.lengthLineEdit.text())
            if length > 0 and length != self._initial_length:
                data["length"] = length
        except ValueError:
            pass

        try:
            width = int(self.ui.widthLineEdit.text())
            if width > 0 and width != self._initial_width:
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



class GridScene(QGraphicsScene):
    def __init__(self, grid_size=20, parent=None):
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



class SnappableObject(QGraphicsObject):
    def __init__(self, text="Объект", width=120, height=80, color="#96C8FF", grid_size=20, parent=None):
        super().__init__(parent)
        self._grid_size = grid_size
        self._width = width
        self._height = height
        self._text = text
        self._color = QColor(color)

        # Флаги
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # Отключаем кэширование, чтобы boundingRect обновлялся
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

    def boundingRect(self):
        return QRectF(0, 0, self._width, self._height)

    def paint(self, painter, option, widget=None):
        # Рисуем прямоугольник
        painter.setBrush(QBrush(self._color))
        painter.setPen(QPen(QColor(0, 0, 0, 150)))
        painter.drawRect(0, 0, self._width, self._height)

        # Рисуем текст
        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))
        text_rect = QRectF(0, 0, self._width, self._height)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self._text)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            x = round(value.x() / self._grid_size) * self._grid_size
            y = round(value.y() / self._grid_size) * self._grid_size
            return QPointF(x, y)
        return super().itemChange(change, value)

    # Методы для редактирования
    def update_text(self, text):
        self._text = text
        self.update()

    def update_size(self, width, height):
        self._width = width
        self._height = height
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

        # Удаляем старый graphicsView
        self.ui.graphicsView.setParent(None)
        self.ui.graphicsView.deleteLater()

        # Создаём новую сцену
        self.scene = GridScene(grid_size=20)

        # Создаём масштабируемый view
        self.graphicsView = ZoomableGraphicsView(self.scene, self.ui.centralwidget)

        # Добавляем в layout
        layout = QVBoxLayout(self.ui.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.graphicsView)

        # Центрируем
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

    #Метод сгенерирован ИИ
    def add_object(self):
        selected_type = self.ui.comboBox.currentText().strip() or "Объект"
        obj = SnappableObject(
            text=selected_type,
            width=120,
            height=80,
            color="#96C8FF",
            grid_size=20
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
        cur_w = item._width
        cur_h = item._height
        cur_color = item._color.name()

        # Диалог
        dlg = EditObjectWindow(self,
                               initial_text=cur_text,
                               initial_length=cur_w,
                               initial_width=cur_h,
                               initial_color=cur_color)
        if dlg.exec() != QDialog.Accepted:
            return

        changes = dlg.get_data()
        if not changes:
            return

        # Применяем изменения
        if "text" in changes:
            item.update_text(changes["text"])
        if "length" in changes:
            item._width = changes["length"]
        if "width" in changes:
            item._height = changes["width"]
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