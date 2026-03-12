from PySide6.QtWidgets import QDialog, QMainWindow
from PySide6.QtCore import Qt

class ThemedDialog(QDialog):
    """Базовый диалог с поддержкой тем"""

    def __init__(self, parent=None):
        super().__init__(parent)



class ThemedMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)