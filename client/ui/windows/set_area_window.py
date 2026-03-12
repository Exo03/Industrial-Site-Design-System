from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import QLocale

from ...ui.widgets.themed_dialog import ThemedDialog
from UI_Files.SetArea import Ui_SetArea


class SetAreaWindow(ThemedDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SetArea()
        self.ui.setupUi(self)

        double_validator = QDoubleValidator(0.1, 9999.99, 2)
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        double_validator.setLocale(QLocale(QLocale.English))

        self.ui.widthLineEdit.setValidator(double_validator)
        self.ui.heightLineEdit.setValidator(double_validator)

    def get_values(self):
        try:
            width = float(self.ui.widthLineEdit.text())
            height = float(self.ui.heightLineEdit.text())
            return width, height
        except ValueError:
            return None, None