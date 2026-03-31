from PySide6.QtWidgets import QDialog, QColorDialog
from PySide6.QtGui import QColor, QDoubleValidator
from PySide6.QtCore import QLocale

from ...ui.widgets.themed_dialog import ThemedDialog
from UI_Files.EditObjectWindow import Ui_Object_edit
from ...core.theme_manager import theme_manager

class EditObjectWindow(ThemedDialog):
    def __init__(self, parent=None, initial_text="", initial_length=120,
                 initial_width=80, initial_color="#96C8FF", initial_zone=0.0):
        super().__init__(parent)
        self.ui = Ui_Object_edit()
        self.ui.setupUi(self)

        self._initial_text = initial_text
        self._initial_length = initial_length
        self._initial_width = initial_width
        self._initial_color = initial_color
        self._initial_zone = initial_zone

        self.ui.textLineEdit.setText(initial_text)
        self.ui.lengthLineEdit.setText(str(initial_length))
        self.ui.widthLineEdit.setText(str(initial_width))
        self.ui.zoneLineEdit.setText(str(initial_zone))  # Заполняем поле из UI
        self.ui.colorDisplay.setText(initial_color)
        self.update_color_display(initial_color)

        self.ui.colorChooseButton.clicked.connect(self.open_color_dialog)

        # Валидатор для чисел с плавающей точкой
        double_validator = QDoubleValidator(0.0, 9999.99, 2)
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        double_validator.setLocale(QLocale(QLocale.English))

        self.ui.lengthLineEdit.setValidator(double_validator)
        self.ui.widthLineEdit.setValidator(double_validator)
        self.ui.zoneLineEdit.setValidator(double_validator)  # Применяем валидатор к зоне

    def open_color_dialog(self):
        current_color = QColor(self.ui.colorDisplay.text().strip() or "#96C8FF")
        dialog = QColorDialog(current_color, self)

        is_dark = theme_manager.is_dark()
        bg = "#1E1E1E" if is_dark else "#F5F5F5"
        fg = "#FFFFFF" if is_dark else "#212121"
        surface = "#2A2A2A" if is_dark else "#FFFFFF"

        dialog.setStyleSheet(f"""
            QDialog {{ background-color: {bg}; color: {fg}; }}
            QLabel {{ color: {fg}; }}
            QPushButton {{
                background-color: {surface}; color: {fg};
                border: 1px solid {'#333333' if is_dark else '#E0E0E0'};
                border-radius: 4px; padding: 6px 12px;
            }}
            QLineEdit, QSpinBox {{ 
                background-color: {surface}; color: {fg}; 
                border: 1px solid {'#333333' if is_dark else '#E0E0E0'}; 
            }}
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
            border: 1px solid {'#333333'};
            border-radius: 4px;
            padding: 6px 8px;
        """)

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

        # Собираем данные из поля зоны
        try:
            zone = float(self.ui.zoneLineEdit.text())
            if zone >= 0 and abs(zone - self._initial_zone) > 1e-6:
                data["zone_margin"] = zone
        except ValueError:
            pass

        color_hex = self.ui.colorDisplay.text().strip()
        if color_hex != self._initial_color and QColor(color_hex).isValid():
            data["color"] = color_hex

        return data