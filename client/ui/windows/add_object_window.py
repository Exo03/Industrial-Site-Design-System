from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QScrollArea, QMessageBox
from PySide6.QtCore import QTimer
from UI_Files.AddObjectWindow import Ui_AddObject
from UI_Files.ObjectRow import Ui_ObjectRow
from client.core import theme_manager
from client.ui.windows import EditObjectWindow
from client.utils.paths import get_resource_path


class ObjectRowWidget(QWidget):
    """Одна строка объекта с полными данными"""

    def __init__(self, name="Объект", width=6.0, length=4.0, color="#96C8FF", zone_margin=0.0, parent=None):
        super().__init__(parent)
        self.ui = Ui_ObjectRow()
        self.ui.setupUi(self)

        self._width = width
        self._length = length
        self._color = color
        self._zone_margin = zone_margin # ⭐ Храним зону

        self.set_name(name)
        self.ui.deleteButton.clicked.connect(self.delete_row)
        self.ui.editButton.clicked.connect(self.edit_object)
        self.update_icons_for_theme(theme_manager.current_theme)

    def update_icons_for_theme(self, theme: str):
        from PySide6.QtGui import QIcon

        suffix = "FFFFFF" if theme == "dark" else "000000"

        self.ui.editButton.setIcon(
            QIcon(get_resource_path(f"Icons/edit_24dp_{suffix}.svg"))
        )
        self.ui.deleteButton.setIcon(
            QIcon(get_resource_path(f"Icons/delete_24dp_{suffix}.svg"))
        )

    def set_name(self, name):
        self.ui.objectNameLabel.setText(name)

    def get_name(self):
        return self.ui.objectNameLabel.text()

    def delete_row(self):
        """Удаляет сам себя"""
        self.deleteLater()

    def edit_object(self):
        """Открывает диалог редактирования с текущими данными объекта"""
        dialog = EditObjectWindow(
            self,
            initial_text=self.get_name(),
            initial_length=self._length,
            initial_width=self._width,
            initial_color=self._color,
            initial_zone=self._zone_margin, # ⭐ Передаем текущую зону
            is_creation=True # ⭐ Разрешаем редактировать зону!
        )

        if dialog.exec() == QDialog.Accepted:
            changes = dialog.get_data()

            if "text" in changes:
                self.set_name(changes["text"])
            if "length" in changes:
                self._length = changes["length"]
            if "width" in changes:
                self._width = changes["width"]
            if "color" in changes:
                self._color = changes["color"]
            if "zone_margin" in changes: # ⭐ Сохраняем новую зону
                self._zone_margin = changes["zone_margin"]


class AddObjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AddObject()
        self.ui.setupUi(self)

        self.object_count = 0

        # Настраиваем контейнер для строк (вместо спейсеров)
        self._setup_rows_container()

        # Подключаем кнопки
        self.ui.addButton.clicked.connect(self.add_row)
        self.ui.backButton.clicked.connect(self.close)
        self.ui.addAllButton.clicked.connect(self.on_add_all)

        # Добавляем первую строку по умолчанию
        self.add_row()

        self.update_icons_for_theme(theme_manager.current_theme)

    def update_icons_for_theme(self, theme: str):
        from PySide6.QtGui import QIcon

        suffix = "FFFFFF" if theme == "dark" else "000000"

        self.ui.backButton.setIcon(
            QIcon(get_resource_path(f"Icons/arrow_back_24dp_{suffix}.svg"))
        )
        self.ui.addButton.setIcon(
            QIcon(get_resource_path(f"Icons/add_24dp_{suffix}.svg"))
        )
        self.ui.addAllButton.setIcon(
            QIcon(get_resource_path(f"Icons/check_24dp_{suffix}.svg"))
        )

    def _setup_rows_container(self):
        """Заменяет спейсеры на ScrollArea с контейнером для строк"""
        # Удаляем спейсеры из layout
        self.ui.verticalLayout.removeItem(self.ui.verticalSpacer)
        self.ui.verticalLayout.removeItem(self.ui.verticalSpacer_2)

        # Удаляем кнопку "Добавить" временно, чтобы потом вернуть её в конец
        self.ui.verticalLayout.removeWidget(self.ui.addAllButton)

        # Создаем ScrollArea (чтобы строки прокручивались если их много)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # Контейнер для строк
        self.rows_container = QWidget()
        self.rows_layout = QVBoxLayout(self.rows_container)
        self.rows_layout.setSpacing(8)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.addStretch()  # Прижимаем строки к верху

        self.scroll_area.setWidget(self.rows_container)

        # Добавляем scroll_area (растягивается на всё доступное пространство)
        self.ui.verticalLayout.addWidget(self.scroll_area, 1)

        # Возвращаем кнопку "Добавить" в самый низ
        self.ui.verticalLayout.addWidget(self.ui.addAllButton)

    def add_row(self):
        """Добавляет новую строку при нажатии на '+' """
        self.object_count += 1
        row = ObjectRowWidget(f"Объект {self.object_count}")

        # Вставляем перед stretch (в конец списка, но перед растяжкой)
        insert_index = self.rows_layout.count() - 1
        self.rows_layout.insertWidget(insert_index, row)

        # Прокручиваем к новой строке
        QTimer.singleShot(10, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        """Прокрутка к последней строке"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def get_objects(self):
        """Возвращает список всех объектов с полными данными"""
        objects = []
        for i in range(self.rows_layout.count()):
            item = self.rows_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, ObjectRowWidget):
                    obj_data = {
                        "name": widget.get_name(),
                        "width": widget._width,
                        "length": widget._length,
                        "color": widget._color,
                        "zone_margin": widget._zone_margin # ⭐ ПЕРЕДАЕМ ЗОНУ!
                    }
                    objects.append(obj_data)
        return objects

    def on_add_all(self):
        """Обработчик кнопки 'Добавить' """
        objects = self.get_objects()
        if not objects:
            QMessageBox.warning(self, "Внимание", "Добавьте хотя бы один объект")
            return

        print(f"Добавляем объекты: {objects}")
        # Здесь можно вызвать API для сохранения
        self.accept()