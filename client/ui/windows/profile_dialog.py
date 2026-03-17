from PyQt6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt

from ...api.users import get_current_user
from ...core import AsyncWorker
from ...ui.widgets.themed_dialog import ThemedDialog
from UI_Files.ProfileWindow import Ui_Profile
from client.session_manager import session


class ProfileDialog(ThemedDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Profile()
        self.ui.setupUi(self)

        self.ui.label_3.setAlignment(Qt.AlignCenter)
        # Загружаем актуальные данные
        self._load_user_data()

        self.ui.pushButton.clicked.connect(self._logout)
        self.ui.pushButton_2.clicked.connect(self._delete_account)

    def _load_user_data(self):
        """Загружает актуальные данные пользователя с сервера"""
        if not session.token:
            self.ui.label_4.setText(session.username)
            self.ui.label_5.setText(session.email)
            return

        worker = AsyncWorker.run_async(get_current_user(session.token))
        worker.signals.success.connect(self._on_user_loaded)
        worker.signals.error.connect(self._on_user_error)

    def _on_user_loaded(self, user_data: dict):
        """Обновляет UI при получении данных"""
        self.ui.label_4.setText(user_data.get("username", session.username))
        self.ui.label_5.setText(user_data.get("email", session.email))

    def _on_user_error(self, error: Exception):
        """При ошибке показываем сохраненные данные"""
        self.ui.label_4.setText(session.username)
        self.ui.label_5.setText(session.email)

    def _logout(self):
        session.logout()
        self.accept()

    def _delete_account(self):
        from PySide6.QtWidgets import QMessageBox, QInputDialog
        from client.api.users import delete_user

        # Подтверждение
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите удалить аккаунт?\nЭто действие необратимо!",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # Запрос пароля
        password, ok = QInputDialog.getText(
            self, "Подтверждение пароля",
            "Введите пароль для удаления аккаунта:",
            QLineEdit.Password
        )

        if not ok or not password:
            return


        worker = AsyncWorker.run_async(delete_user(password, session.token))
        worker.signals.success.connect(self._on_delete_success)
        worker.signals.error.connect(self._on_delete_error)

    def _on_delete_success(self, result):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Успех", "Аккаунт удален")
        session.logout()
        self.accept()

    def _on_delete_error(self, error: Exception):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Ошибка", f"Не удалось удалить аккаунт:\n{error}")