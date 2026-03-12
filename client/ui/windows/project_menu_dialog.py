from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal

from ...ui.widgets.themed_dialog import ThemedDialog
from UI_Files.ProjectMenu import Ui_ProjectMenuWindow
from .create_project_dialog import CreateProjectDialog


class ProjectMenuDialog(ThemedDialog):
    """Меню выбора проекта после авторизации"""

    project_created = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProjectMenuWindow()
        self.ui.setupUi(self)
        self._connect_signals()

    def _connect_signals(self):
        self.ui.pushButton.clicked.connect(self._create_new_project)
        self.ui.pushButton_2.clicked.connect(self._open_project)

    def _create_new_project(self):
        dialog = CreateProjectDialog(self)
        if dialog.exec() == CreateProjectDialog.Accepted:
            self.project_created.emit()
            self.accept()

    def _open_project(self):
        QMessageBox.information(self, "Информация", "Функция в разработке")
        self.project_created.emit()
        self.accept()