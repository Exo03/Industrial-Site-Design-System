from PySide6.QtWidgets import QMessageBox

from ...ui.widgets.themed_dialog import ThemedDialog
from UI_Files.AuthorizeWindow import Ui_AuthorizeWindow
from client.api.auth import login
from client.api.users import get_current_user
from client.session_manager import session
from ...core.async_worker import AsyncWorker


class AuthDialog(ThemedDialog):
    """Диалог авторизации с интеграцией API"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AuthorizeWindow()
        self.ui.setupUi(self)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.ui.pushButton.setText("Войти")
        self.ui.pushButton.setDefault(True)

    def _connect_signals(self):
        self.ui.pushButton.clicked.connect(self._handle_login)
        self.ui.passwordLineEdit.returnPressed.connect(self._handle_login)
        self.ui.registerLink.linkActivated.connect(self._open_register)

    def _handle_login(self):
        username = self.ui.loginLineEdit.text().strip()
        password = self.ui.passwordLineEdit.text()

        if not self._validate_input(username, password):
            return

        self._set_loading(True)

        worker = AsyncWorker.run_async(self._do_login(username, password))
        worker.signals.success.connect(self._on_login_success)
        worker.signals.error.connect(self._on_login_error)

    def _validate_input(self, username: str, password: str) -> bool:
        if not username:
            QMessageBox.warning(self, "Ошибка", "Введите логин")
            return False
        if not password:
            QMessageBox.warning(self, "Ошибка", "Введите пароль")
            return False
        return True

    async def _do_login(self, username: str, password: str):
        token_data = await login(username, password)
        token = token_data["access_token"]
        user_data = await get_current_user(token)

        return {
            "token": token,
            "username": user_data.get("username", username),
            "user_id": user_data.get("id")
        }

    def _on_login_success(self, data: dict):
        session.login(
            token=data["token"],
            username=data["username"],
            user_id=data.get("user_id")
        )
        self.accept()

    def _on_login_error(self, error: Exception):
        self._set_loading(False)

        error_str = str(error).lower()

        if "401" in error_str or "403" in error_str:
            QMessageBox.warning(self, "Ошибка входа", "Неверный логин или пароль")
        elif "connection" in error_str:
            QMessageBox.critical(self, "Ошибка подключения", "Сервер недоступен")
        else:
            QMessageBox.critical(self, "Ошибка", f"Не удалось войти: {error}")

    def _set_loading(self, loading: bool):
        self.ui.pushButton.setEnabled(not loading)
        self.ui.pushButton.setText("Вход..." if loading else "Войти")
        self.ui.loginLineEdit.setEnabled(not loading)
        self.ui.passwordLineEdit.setEnabled(not loading)

    def _open_register(self):
        from .register_dialog import RegisterDialog

        self.hide()
        reg_dialog = RegisterDialog(self.parent())

        if reg_dialog.exec() == RegisterDialog.Accepted:
            pass

        self.show()
        self.raise_()
        self.activateWindow()