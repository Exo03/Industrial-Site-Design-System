from PySide6.QtWidgets import QMessageBox

from ...ui.widgets.themed_dialog import ThemedDialog
from UI_Files.RegisterWindow import Ui_RegisterWindow
from client.api.auth import register
from ...core.async_worker import AsyncWorker


class RegisterDialog(ThemedDialog):
    """Диалог регистрации"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)
        self._registered_username = None  # Для передачи в AuthDialog
        self._connect_signals()

    def _connect_signals(self):
        self.ui.pushButton.clicked.connect(self._handle_register)
        self.ui.passwordLineEdit.returnPressed.connect(self._handle_register)
        self.ui.ifExist.linkActivated.connect(self._back_to_login)

    def _handle_register(self):
        login_text = self.ui.loginLineEdit.text().strip()
        email = self.ui.emailLineEdit.text().strip()
        password = self.ui.passwordLineEdit.text()

        if not self._validate(login_text, email, password):
            return

        self._set_loading(True)

        worker = AsyncWorker.run_async(register(email, login_text, password))
        worker.signals.success.connect(lambda: self._on_success(login_text))  # Передаём логин
        worker.signals.error.connect(self._on_error)

    def _validate(self, login: str, email: str, password: str) -> bool:
        if not all([login, email, password]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return False

        if "@" not in email or "." not in email.split("@")[-1]:
            QMessageBox.warning(self, "Ошибка", "Введите корректный email")
            return False

        if len(password) < 5:
            QMessageBox.warning(self, "Ошибка", "Пароль должен быть минимум 5 символов")
            return False

        return True

    def _on_success(self, username: str):
        self._registered_username = username  # Сохраняем для возврата
        QMessageBox.information(self, "Успешно", "Регистрация завершена!")
        self.accept()

    def _on_error(self, error: Exception):
        self._set_loading(False)

        error_str = str(error).lower()

        if "already exists" in error_str or "409" in error_str:
            QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")
        else:
            QMessageBox.critical(self, "Ошибка", f"Ошибка регистрации: {error}")

    def _set_loading(self, loading: bool):
        self.ui.pushButton.setEnabled(not loading)
        self.ui.pushButton.setText("Регистрация..." if loading else "Зарегистрироваться")

    def _back_to_login(self):
        self.reject()