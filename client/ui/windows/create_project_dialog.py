from PySide6.QtWidgets import QMessageBox

from ...ui.widgets.themed_dialog import ThemedDialog
from UI_Files.CreateProjectWindow import Ui_CreateProject
from client.api.projects import create_project
from client.session_manager import session
from ...core.async_worker import AsyncWorker


class CreateProjectDialog(ThemedDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_CreateProject()
        self.ui.setupUi(self)

        self.created_project = None

        self.ui.pushButton.clicked.connect(self._create_new_project)
        self.ui.pushButton_2.clicked.connect(self.reject)

    def _create_new_project(self):
        name = self.ui.lineEdit.text().strip()
        description = self.ui.plainTextEdit.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название проекта")
            return

        token = session.token
        if not token:
            QMessageBox.critical(self, "Ошибка", "Не авторизован")
            return

        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton.setText("Создание...")

        worker = AsyncWorker.run_async(
            create_project(name, description, 0, 0, token)
        )
        worker.signals.success.connect(self._on_created)
        worker.signals.error.connect(self._on_error)

    def _on_created(self, result: dict):
        self.created_project = result
        self.accept()

    def _on_error(self, error: Exception):
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton.setText("Создать")
        QMessageBox.critical(self, "Ошибка", f"Не удалось создать проект:\n{error}")

    def get_project(self):
        return self.created_project