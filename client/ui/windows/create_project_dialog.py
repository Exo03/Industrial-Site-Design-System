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

        self.created_project_name = None
        self.ui.pushButton.clicked.connect(self.create_new_project)
        self.ui.pushButton_2.clicked.connect(self.reject)

    def create_new_project(self):
        name = self.ui.lineEdit.text()
        description = self.ui.plainTextEdit.toPlainText()
        token = session.token

        AsyncWorker.run_async(create_project(name, description, 0, 0, token))
        self.accept()

    def proj_name(self, result):
        self.created_project_name = result.get("name")
        self.accept()

    def get_project_id(self):
        return self.created_project_name