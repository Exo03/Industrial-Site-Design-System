from PySide6.QtWidgets import QMessageBox, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Signal

from ...api.projects import get_project, get_user_projects
from ...core import AsyncWorker
from ...session_manager import session
from ...ui.widgets.themed_dialog import ThemedDialog
from UI_Files.ProjectMenu import Ui_ProjectMenuWindow
from .create_project_dialog import CreateProjectDialog


class ProjectMenuDialog(ThemedDialog):
    """Меню выбора проекта после авторизации"""

    project_selected = Signal(dict)  # Передаем данные проекта
    project_created = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProjectMenuWindow()
        self.ui.setupUi(self)
        self._projects = []
        self._setup_ui()
        self._connect_signals()
        self._load_projects()

    def _setup_ui(self):
        """Добавляем область для списка проектов"""
        # Создаем контейнер для списка проектов
        self.projects_container = QWidget()
        self.projects_layout = QVBoxLayout(self.projects_container)
        self.projects_layout.setSpacing(8)

        # Добавляем в существующий layout
        self.ui.verticalLayout.insertWidget(1, self.projects_container)

    def _connect_signals(self):
        self.ui.pushButton.clicked.connect(self._create_new_project)
        self.ui.pushButton_2.clicked.connect(self._open_selected_project)

    def _load_projects(self):
        """Загружает список проектов с сервера"""
        if not session.token:
            return

        worker = AsyncWorker.run_async(get_user_projects(session.token))
        worker.signals.success.connect(self._on_projects_loaded)
        worker.signals.error.connect(self._on_projects_error)

    def _on_projects_loaded(self, projects: list):
        """Отображает загруженные проекты"""
        self._projects = projects

        # Очищаем старые кнопки
        while self.projects_layout.count():
            item = self.projects_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not projects:
            from PySide6.QtWidgets import QLabel
            label = QLabel("У вас пока нет проектов. Создайте новый!")
            label.setStyleSheet("color: gray; padding: 20px;")
            self.projects_layout.addWidget(label)
            return

        # Создаем кнопки для каждого проекта
        for project in projects:
            btn = QPushButton(f"{project['name']}\n{project.get('description', '')[:50]}...")
            btn.setProperty("project_id", project["id"])
            btn.setProperty("project_data", project)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 12px;
                    border: 1px solid #333;
                    border-radius: 4px;
                }
                QPushButton:checked {
                    border: 2px solid #BB86FC;
                    background-color: rgba(187, 134, 252, 0.1);
                }
            """)
            btn.clicked.connect(self._on_project_selected)
            self.projects_layout.addWidget(btn)

    def _on_projects_error(self, error: Exception):
        QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить проекты:\n{error}")

    def _on_project_selected(self):
        """Сохраняет выбранный проект"""
        sender = self.sender()
        self._selected_project_id = sender.property("project_id")
        self._selected_project_data = sender.property("project_data")

    def _create_new_project(self):
        dialog = CreateProjectDialog(self)
        if dialog.exec() == CreateProjectDialog.Accepted:
            self.project_created.emit()
            # Перезагружаем список
            self._load_projects()

    def _open_selected_project(self):
        """Открывает выбранный проект"""
        if not hasattr(self, '_selected_project_id') or self._selected_project_id is None:
            QMessageBox.warning(self, "Внимание", "Выберите проект из списка")
            return

        # Загружаем полные данные проекта
        worker = AsyncWorker.run_async(
            get_project(self._selected_project_id, session.token)
        )
        worker.signals.success.connect(self._on_project_opened)
        worker.signals.error.connect(self._on_project_error)

    def _on_project_opened(self, project_data: dict):
        self.project_selected.emit(project_data)
        self.accept()

    def _on_project_error(self, error: Exception):
        QMessageBox.critical(self, "Ошибка", f"Не удалось открыть проект:\n{error}")