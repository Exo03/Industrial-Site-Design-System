from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, \
    QGraphicsItem, QDialog, QColorDialog, QVBoxLayout, QLabel, QGraphicsItemGroup
from PySide6.QtGui import QBrush, QColor, QFont, QPen, QFontMetrics, Qt

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

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1000, 1000)
        self.ui.graphicsView.setScene(self.scene)

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
        group.setPos(200, 200)

    # Метод сгенерирован ИИ
    def edit_object(self):
        print("🔧 edit_object: started")
        selected = self.scene.selectedItems()
        print(f"🔧 Selected items: {len(selected)}")
        for i, item in enumerate(selected):
            print(f"  [{i}] Type: {type(item).__name__}")

        if not selected:
            print("⚠️ No items selected")
            return

        rect_item = None
        text_item = None
        group_item = None

        for item in selected:
            if isinstance(item, QGraphicsRectItem):
                rect_item = item
            elif isinstance(item, QGraphicsTextItem):
                text_item = item
            elif isinstance(item, QGraphicsItemGroup):
                # Ищем rect и text внутри группы
                for child in item.childItems():
                    if isinstance(child, QGraphicsRectItem):
                        rect_item = child
                    elif isinstance(child, QGraphicsTextItem):
                        text_item = child
                group_item = item

        if not rect_item:
            print("⚠️ No rect item found")
            return

        # ——— ПРАВИЛЬНОЕ ПОЛУЧЕНИЕ ГЛОБАЛЬНОЙ ПОЗИЦИИ ———
        if group_item:
            # Получаем глобальную позицию левого верхнего угла прямоугольника
            top_left = rect_item.mapToScene(0, 0)
            scene_x, scene_y = top_left.x(), top_left.y()
        else:
            scene_x, scene_y = rect_item.pos().x(), rect_item.pos().y()

        # ——— ПОЛУЧАЕМ ТЕКУЩИЕ ПАРАМЕТРЫ ———
        rect = rect_item.rect()
        current_length = int(rect.width())
        current_width = int(rect.height())
        current_color = rect_item.brush().color().name()
        current_text = text_item.toPlainText() if text_item else ""

        # Открываем диалог
        dialog = EditObjectWindow(
            self,
            initial_text=current_text,
            initial_length=current_length,
            initial_width=current_width,
            initial_color=current_color
        )

        if dialog.exec() != QDialog.Accepted:
            print("Dialog cancelled")
            return

        changes = dialog.get_data()
        print(f"Changes: {changes}")
        if not changes:
            print("No changes to apply")
            return

        # ——— ПРИМЕНЯЕМ ИЗМЕНЕНИЯ ———
        new_rect = rect_item.rect()
        if "length" in changes:
            new_rect.setWidth(changes["length"])
        if "width" in changes:
            new_rect.setHeight(changes["width"])
        rect_item.setRect(new_rect)

        if group_item:
            # 1. запоминаем позицию и состав
            old_pos = group_item.pos()
            items = group_item.childItems()  # прямоугольник + текст
            # 2. удаляем старую группу
            self.scene.destroyItemGroup(group_item)
            # 3. создаём новую с тем же составом
            group_item = self.scene.createItemGroup(items)
            group_item.setPos(old_pos)
            group_item.setFlags(QGraphicsItem.ItemIsMovable |
                                QGraphicsItem.ItemIsSelectable)

        # Цвет
        if "color" in changes:
            color = QColor(changes["color"])
            rect_item.setBrush(QBrush(color))
            rect_item.setPen(QPen(QColor(0, 0, 0, 150)))

        # Текст
        if "text" in changes:
            new_text = changes["text"]

            # 1. создаём текст, если его нет
            if not text_item and new_text.strip():
                text_item = QGraphicsTextItem()
                font = QFont()
                font.setPointSize(9)
                text_item.setFont(font)
                text_item.setDefaultTextColor(QColor(0, 0, 0))
                group_item.addToGroup(text_item)

            if text_item:
                text_item.setPlainText(new_text)
                br = text_item.boundingRect()

                top_left_rect = rect_item.pos()
                dx = top_left_rect.x() + (new_rect.width() - br.width()) / 2
                dy = top_left_rect.y() + (new_rect.height() - br.height()) / 2
                text_item.setPos(dx, dy)

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