import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from client.core.theme_manager import theme_manager
from client.session_manager import session
from client.ui.windows import AuthDialog, ProjectMenuDialog, CanvasWindow


def main():
    # Высокий DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Industrial Designer")
    app.setFont(QFont("Segoe UI", 10))

    # Применяем тему
    theme_manager.initialize(app, 'dark')

    # Авторизация
    if not session.is_authenticated:
        auth_dialog = AuthDialog()
        if auth_dialog.exec() != AuthDialog.Accepted:
            sys.exit(0)

    # Меню проектов
    menu_dialog = ProjectMenuDialog()

    result = menu_dialog.exec()

    # ← ИСПРАВЛЕНО: Проверяем результат
    if result == ProjectMenuDialog.Rejected:
        # Пользователь нажал "Отмена" или закрыл окно
        sys.exit(0)

    # ← ИСПРАВЛЕНО: Если Accepted — показываем Canvas
    canvas = CanvasWindow()
    canvas.show()

    # Запускаем главный цикл
    sys.exit(app.exec())


if __name__ == "__main__":
    main()