import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

from client.core.theme_manager import theme_manager
from client.session_manager import session
from client.ui.windows import AuthDialog, ProjectMenuDialog, CanvasWindow
from client.utils.paths import get_resource_path


def main():
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            'company.industrialdesigner.v1'
        )

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Industrial Designer")
    app.setApplicationDisplayName("Industrial Designer")
    app.setFont(QFont("Segoe UI", 10))

    app.setWindowIcon(QIcon(get_resource_path("Icons/logotip.ico")))

    theme_manager.initialize(app, 'dark')

    # Цикл авторизации: показываем AuthDialog пока не будет успешного входа или закрытия
    while not session.is_authenticated:
        auth_dialog = AuthDialog()
        result = auth_dialog.exec()

        # Цикл авторизации: показываем AuthDialog пока не будет успешного входа или закрытия
        while not session.is_authenticated:
            auth_dialog = AuthDialog()
            auth_dialog.exec()
            # После exec() проверяем, авторизовался ли пользователь
            # Если нет — значит диалог был закрыт (X или "назад"), выходим
            if not session.is_authenticated:
                sys.exit(0)

    # Успешная авторизация — продолжаем
    menu_dialog = ProjectMenuDialog()
    result = menu_dialog.exec()

    if result == ProjectMenuDialog.Rejected:
        sys.exit(0)

    selected_project = getattr(menu_dialog, '_selected_project_data', None)
    canvas = CanvasWindow(project_data=selected_project)
    canvas.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()