from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QLineEdit)
from PySide6.QtCore import Qt

from ...api.users import get_current_user
from ...core import AsyncWorker, theme_manager
from ...ui.widgets.themed_dialog import ThemedDialog
from UI_Files.ProfileWindow import Ui_Profile
from client.session_manager import session
from ...utils.paths import get_resource_path


class ProfileDialog(ThemedDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Profile()
        self.ui.setupUi(self)

        self.ui.ProfIcon.setAlignment(Qt.AlignCenter)
        # Загружаем актуальные данные
        self._load_user_data()

        self.ui.logoutButton.clicked.connect(self._logout)
        self.ui.deleteButton.clicked.connect(self._delete_account)

        self.update_icons_for_theme(theme_manager.current_theme)


    def update_icons_for_theme(self, theme: str):
        from PySide6.QtGui import QIcon

        suffix = "FFFFFF" if theme == "dark" else "000000"

        self.ui.exitButton.setIcon(
            QIcon(
                get_resource_path(f"Icons/arrow_back_24dp_{suffix}.svg"))
        )
        self.ui.editButton.setIcon(
            QIcon(get_resource_path(f"Icons/edit_24dp_{suffix}.svg"))
        )
        self.ui.ProfIcon.setPixmap(
            QPixmap(get_resource_path(f"Icons/account_circle_48dp_{suffix}.svg"))
        )
        self.ui.deleteButton.setIcon(
            QIcon(get_resource_path(f"Icons/delete_24dp_{suffix}.svg"))
        )
        self.ui.logoutButton.setIcon(
            QIcon(get_resource_path(f"Icons/logout_24dp_{suffix}.svg"))
        )

    def _load_user_data(self):
        if not session.token:
            self.ui.login_label.setText(session.username)
            self.ui.emailLabel.setText(session.email)
            return

        worker = AsyncWorker.run_async(get_current_user(session.token))
        worker.signals.success.connect(self._on_user_loaded)
        worker.signals.error.connect(self._on_user_error)

    def _on_user_loaded(self, user_data: dict):
        """Обновляет UI при получении данных"""
        self.ui.login_label.setText(user_data.get("username", session.username))
        self.ui.emailLabel.setText(user_data.get("email", session.email))

    def _on_user_error(self, error: Exception):
        """При ошибке показываем сохраненные данные"""
        self.ui.login_label.setText(session.username)
        self.ui.emailLabel.setText(session.email)

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