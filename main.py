from PyQt6.QtCore import QPointF
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, \
    QGraphicsItem, QDialog, QColorDialog, QVBoxLayout, QLabel, QGraphicsItemGroup, QGraphicsView
from PySide6.QtGui import QBrush, QColor, QFont, QPen, QFontMetrics, Qt, QTransform, QPainter

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

class CanvasWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.graphicsView.setParent(None)
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self.ui.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ui.graphicsView)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1000, 1000)
        self.ui.graphicsView.setScene(self.scene)

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

        rect_w, rect_h = 120, 80
        rect_color = QColor(150, 200, 255)

        # 1. создаём элементы, но НЕ добавляем в сцену
        rect_item = QGraphicsRectItem(0, 0, rect_w, rect_h)
        rect_item.setBrush(QBrush(rect_color))
        rect_item.setPen(QPen(QColor(0, 0, 0, 150)))

        text_item = QGraphicsTextItem()
        text_item.setPlainText(selected_type)
        font = QFont()
        font.setPointSize(9)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(0, 0, 0))

        br = text_item.boundingRect()
        text_item.setPos((rect_w - br.width()) / 2,
                         (rect_h - br.height()) / 2)

        # 2. СНАЧАЛА добавляем в сцену группу, а потом уже в неё элементы
        group = self.scene.createItemGroup([])
        group.addToGroup(rect_item)
        group.addToGroup(text_item)
        group.setFlags(QGraphicsItem.ItemIsMovable |
                       QGraphicsItem.ItemIsSelectable)
        group.setPos(400, 400)

    # Метод сгенерирован ИИ
    # ---------- edit_object ----------
    def edit_object(self):
        print("🔧 edit_object: started")
        selected = self.scene.selectedItems()
        if not selected:
            print("⚠️ No items selected")
            return

        # 1. находим rect и text (внутри группы или снаружи)
        rect_item = text_item = group_item = None
        for item in selected:
            if isinstance(item, QGraphicsItemGroup):
                group_item = item
                for ch in item.childItems():
                    if isinstance(ch, QGraphicsRectItem):
                        rect_item = ch
                    elif isinstance(ch, QGraphicsTextItem):
                        text_item = ch
            elif isinstance(item, QGraphicsRectItem):
                rect_item = item
            elif isinstance(item, QGraphicsTextItem):
                text_item = item

        if not rect_item:  # главное – прямоугольник
            print("⚠️ No rect item found")
            return

        # 2. запоминаем ГЛОБАЛЬНУЮ позицию левого-верхнего угла прямоугольника
        old_top_left = rect_item.mapToScene(0, 0)

        # 3. текущие параметры
        rect = rect_item.rect()
        cur_w, cur_h = int(rect.width()), int(rect.height())
        cur_color = rect_item.brush().color().name()
        cur_text = text_item.toPlainText() if text_item else ""

        # 4. диалог
        dlg = EditObjectWindow(self,
                               initial_text=cur_text,
                               initial_length=cur_w,
                               initial_width=cur_h,
                               initial_color=cur_color)
        if dlg.exec() != QDialog.Accepted:
            return

        changes = dlg.get_data()
        print("Changes:", changes)
        if not changes:
            return

        # 5. новый размер
        new_rect = rect_item.rect()
        if "length" in changes:
            new_rect.setWidth(changes["length"])
        if "width" in changes:
            new_rect.setHeight(changes["width"])
        rect_item.setRect(new_rect)

        # 6. цвет
        if "color" in changes:
            c = QColor(changes["color"])
            rect_item.setBrush(QBrush(c))
            rect_item.setPen(QPen(QColor(0, 0, 0, 150)))

        # 7. текст
        if "text" in changes:
            new_txt = changes["text"]
            if not text_item and new_txt.strip():  # создаём, если не было
                text_item = QGraphicsTextItem()
                font = QFont()
                font.setPointSize(9)
                text_item.setFont(font)
                text_item.setDefaultTextColor(QColor(0, 0, 0))
                (group_item.addToGroup(text_item) if group_item
                 else self.scene.addItem(text_item))

            if text_item:
                text_item.setPlainText(new_txt)
                br = text_item.boundingRect()
                # центруем в локальных координатах прямоугольника
                text_item.setPos((new_rect.width() - br.width()) / 2,
                                 (new_rect.height() - br.height()) / 2)

        # 8. ВОССТАНАВЛИВАЕМ глобальное положение левого-верхнего угла
        new_top_left = rect_item.mapToScene(0, 0)
        delta = old_top_left - new_top_left

        if group_item:
            group_item.setPos(group_item.pos() + delta)

            # сохраняем локальную позицию текста
            text_local_pos = text_item.pos() if text_item else QPointF()

            group_item.removeFromGroup(rect_item)
            group_item.addToGroup(rect_item)

            # возвращаем текст на место и поднимаем выше
            if text_item:
                text_item.setPos(text_local_pos)
                text_item.setZValue(1)
        else:
            rect_item.setPos(rect_item.pos() + delta)
            if text_item:
                text_item.setPos(text_item.pos() + delta)

        self.scene.update()
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