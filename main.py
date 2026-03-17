import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

from client.core.theme_manager import theme_manager
from client.session_manager import session
from client.ui.windows import AuthDialog, ProjectMenuDialog, CanvasWindow
from client.ui.windows.canvas_window import get_resource_path


# ваша функция для путей


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

    if not session.is_authenticated:
        auth_dialog = AuthDialog()
        if auth_dialog.exec() != AuthDialog.Accepted:
            sys.exit(0)

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