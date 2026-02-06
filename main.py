from PySide6.QtCore import QPointF, QRectF, Qt, QLocale, Signal, QObject, QTimer
from PySide6.QtGui import QBrush, QColor, QFont, QPen, QPainter, QWheelEvent, QTransform, QDoubleValidator
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsItem, QGraphicsObject, QDialog, QColorDialog,
    QVBoxLayout, QLabel, QStatusBar, QMenuBar, QMenu, QToolBar,
    QWidget, QComboBox, QHBoxLayout, QMessageBox
)
from client.api.auth import login, register
from client.api.users import get_current_user

from UI_Files.EditObjectWindow import Ui_Object_edit
from UI_Files.MainWindow import Ui_MainWindow
from UI_Files.SetArea import Ui_SetArea
from UI_Files.AuthorizeWindow import Ui_AuthorizeWindow
from UI_Files.RegisterWindow import Ui_RegisterWindow

import asyncio
from PySide6.QtCore import QRunnable, QThreadPool


#Сгенерировано ИИ
class SessionManager(QObject):
    """Синглтон для хранения сессии пользователя"""
    logged_in = Signal(str)
    logged_out = Signal()

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._token = None
        self._username = None
        self._initialized = True

    @property
    def token(self):
        return self._token

    @property
    def is_authenticated(self):
        return self._token is not None

    def login(self, token, username, user_id=None):
        self._token = token
        self._username = username
        self.logged_in.emit(username)

    def logout(self):
        self._token = None
        self._username = None
        self.logged_out.emit()


session = SessionManager()


#Сгенерировано ИИ
class WorkerSignals(QObject):
    success = Signal(object)
    error = Signal(Exception)
    finished = Signal(object)

#Сгенерировано ИИ
class AsyncWorker(QRunnable):
    """Выполняет async код в фоновом потоке"""

    def __init__(self, coro):
        super().__init__()
        self.coro = coro
        self.signals = WorkerSignals()
        self.setAutoDelete(True)

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.coro)
            self.signals.success.emit(result)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(e)
            self.signals.finished.emit(None)

    @staticmethod
    def run_async(coro):
        worker = AsyncWorker(coro)
        QThreadPool.globalInstance().start(worker)
        return worker

PIXELS_PER_METER = 20

class EditObjectWindow(QDialog):
    def __init__(self, parent=None, initial_text="", initial_length=120, initial_width=80, initial_color="#96C8FF"):
        super().__init__(parent)
        self.ui = Ui_Object_edit()
        self.ui.setupUi(self)

        self._initial_text = initial_text
        self._initial_length = initial_length
        self._initial_width = initial_width
        self._initial_color = initial_color

        self.ui.textLineEdit.setText(initial_text)
        self.ui.lengthLineEdit.setText(str(initial_length))
        self.ui.widthLineEdit.setText(str(initial_width))
        self.ui.colorDisplay.setText(initial_color)
        self.update_color_display(initial_color)

        self.ui.colorChooseButton.clicked.connect(self.open_color_dialog)

        double_validator = QDoubleValidator(0.1, 9999.99, 2)  # от 0.1 до 9999.99, 2 знака после запятой
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        double_validator.setLocale(QLocale(QLocale.English)) # Разделитель - точка

        self.ui.lengthLineEdit.setValidator(double_validator)
        self.ui.widthLineEdit.setValidator(double_validator)

    def open_color_dialog(self):
        current_color = QColor(self.ui.colorDisplay.text().strip() or "#96C8FF")
        dialog = QColorDialog(current_color, self)
        dialog.setStyleSheet("""
            QDialog { background-color: #1E1E1E; color: #FFFFFF; }
            QLabel { color: #FFFFFF; }
            QPushButton {
                background-color: #2A2A2A; color: #FFFFFF;
                border: 1px solid #333333; border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover { background-color: #333333; }
            QPushButton:pressed { background-color: #BB86FC; color: black; }
            QLineEdit, QSpinBox { background-color: #2A2A2A; color: #FFFFFF; border: 1px solid #333333; }
        """)
        if dialog.exec() == QDialog.Accepted:
            color = dialog.currentColor()
            if color.isValid():
                hex_color = color.name()
                self.ui.colorDisplay.setText(hex_color)
                self.update_color_display(hex_color)

    def update_color_display(self, hex_color):
        color = QColor(hex_color)
        text_color = "black" if color.lightness() > 128 else "white"
        self.ui.colorDisplay.setStyleSheet(f"""
            background-color: {hex_color};
            color: {text_color};
            border: 1px solid #333333;
            border-radius: 4px;
            padding: 6px 8px;
        """)
    #Функция сгенерирована ии
    def get_data(self):
        data = {}

        text = self.ui.textLineEdit.text().strip()
        if text != self._initial_text:
            data["text"] = text

        try:
            length = float(self.ui.lengthLineEdit.text())
            if length > 0 and abs(length - self._initial_length) > 1e-6:
                data["length"] = length
        except ValueError:
            pass

        try:
            width = float(self.ui.widthLineEdit.text())
            if width > 0 and abs(width - self._initial_width) > 1e-6:
                data["width"] = width
        except ValueError:
            pass

        color_hex = self.ui.colorDisplay.text().strip()
        if color_hex != self._initial_color and QColor(color_hex).isValid():
            data["color"] = color_hex

        return data

#Класс сгенерирован ИИ
class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)  # Управляем вручную
        self._panning = False
        self._last_pan_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._panning = True
            self._last_pan_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning and self._last_pan_pos:
            delta = event.position() - self._last_pan_pos
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - int(delta.x())
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - int(delta.y())
            )
            self._last_pan_pos = event.position()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta != 0:
                zoom_factor = 1.25 if delta > 0 else 1 / 1.25
                self.scale(zoom_factor, zoom_factor)
                event.accept()
        else:
            # Прокрутка колёсиком без Ctrl
            super().wheelEvent(event)


#Класс сгенерирован ИИ
class GridScene(QGraphicsScene):
    def __init__(self, grid_size=10, parent=None):
        super().__init__(parent)
        self._grid_size = grid_size
        self.setSceneRect(0, 0, 1000, 1000)

    def drawBackground(self, painter, rect):
        # Вызываем родительский метод, если нужно
        super().drawBackground(painter, rect)

        # Настройка пера для сетки
        grid_pen = QPen(QColor(60, 60, 60))  # Тёмно-серый
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)

        # Получаем видимую область
        left = int(rect.left()) - (int(rect.left()) % self._grid_size)
        top = int(rect.top()) - (int(rect.top()) % self._grid_size)

        # Рисуем вертикальные линии
        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += self._grid_size

        # Рисуем горизонтальные линии
        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += self._grid_size


#Класс сгенерирован ИИ
class SnappableObject(QGraphicsObject):
    def __init__(self, text="Объект", width_m=6.0, height_m=4.0, color="#96C8FF", grid_size_m=0.5, pixels_per_meter=PIXELS_PER_METER, parent=None):
        super().__init__(parent)
        self._pixels_per_meter = pixels_per_meter
        self._grid_size_m = grid_size_m
        self._width_m = width_m
        self._height_m = height_m
        self._text = text
        self._color = QColor(color)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self._is_outside_area = False
        self._is_overlapping = False  # Новое поле

    def _px(self, meters):
        return meters * self._pixels_per_meter

    def boundingRect(self):
        return QRectF(0, 0, self._px(self._width_m), self._px(self._height_m))

    def set_outside_area(self, is_outside: bool):
        if self._is_outside_area != is_outside:
            self._is_outside_area = is_outside
            self.update()  # Перерисовать

    def set_overlapping(self, is_overlapping: bool):
        if self._is_overlapping != is_overlapping:
            self._is_overlapping = is_overlapping
            self.update()  # Перерисовать

    def paint(self, painter, option, widget=None):
        w_px = self._px(self._width_m)
        h_px = self._px(self._height_m)

        painter.setBrush(QBrush(self._color))
        base_pen = QPen(QColor(0, 0, 0, 150))
        base_pen.setWidth(1)
        painter.setPen(base_pen)
        painter.drawRect(0, 0, w_px, h_px)

        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))
        text_rect = QRectF(0, 0, w_px, h_px)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self._text)

        # Рисуем выделение (если выбран)
        if self.isSelected():
            pen = QPen(Qt.white)
            pen.setWidth(1)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(0, 0, w_px, h_px)

        # Рисуем жёлтую рамку, если пересекается с другим объектом
        if self._is_overlapping:
            yellow_pen = QPen(QColor(255, 255, 0))
            yellow_pen.setWidth(2)
            yellow_pen.setStyle(Qt.SolidLine)
            painter.setPen(yellow_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(0, 0, w_px, h_px)

        # Рисуем красную рамку, если вне площадки
        if self._is_outside_area:
            red_pen = QPen(QColor(255, 0, 0))
            red_pen.setWidth(2)
            red_pen.setStyle(Qt.SolidLine)
            painter.setPen(red_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(0, 0, w_px, h_px)

    geometryChanged = Signal()  # Новый сигнал

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            grid_px = self._px(self._grid_size_m)
            x = round(value.x() / grid_px) * grid_px
            y = round(value.y() / grid_px) * grid_px
            new_value = QPointF(x, y)
            # После изменения позиции — уведомляем
            result = super().itemChange(change, new_value)
            self.geometryChanged.emit()
            return result
        elif change == QGraphicsItem.ItemTransformHasChanged:
            self.geometryChanged.emit()
        return super().itemChange(change, value)

    def update_text(self, text):
        self._text = text
        self.update()

    def update_size(self, width_m, height_m):
        self._width_m = width_m
        self._height_m = height_m
        self.prepareGeometryChange()
        self.update()

    def update_color(self, color):
        self._color = QColor(color)
        self.update()

class SetAreaWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SetArea()
        self.ui.setupUi(self)

        # Установим валидаторы для полей
        double_validator = QDoubleValidator(0.1, 9999.99, 2)
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        double_validator.setLocale(QLocale(QLocale.English))

        self.ui.widthLineEdit.setValidator(double_validator)
        self.ui.heightLineEdit.setValidator(double_validator)

    def get_values(self):
        try:
            width = float(self.ui.widthLineEdit.text())
            height = float(self.ui.heightLineEdit.text())
            return width, height
        except ValueError:
            return None, None

class WorkspaceArea(QGraphicsObject):
    def __init__(self, width_m, height_m, pixels_per_meter=PIXELS_PER_METER):
        super().__init__()
        self._width_m = width_m
        self._height_m = height_m
        self._pixels_per_meter = pixels_per_meter

        # Запрещаем выделение и перемещение
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsFocusable, False)

    def boundingRect(self):
        w_px = self._width_m * self._pixels_per_meter
        h_px = self._height_m * self._pixels_per_meter
        return QRectF(0, 0, w_px, h_px)

    def paint(self, painter, option, widget=None):
        w_px = self._width_m * self._pixels_per_meter
        h_px = self._height_m * self._pixels_per_meter

        # Жирная рамка
        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)  # Без заливки
        painter.drawRect(0, 0, w_px, h_px)

#Сгенерировано ИИ
class RegisterDialog(QDialog):
    """Диалог регистрации"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)

        self._connect_signals()

    def _connect_signals(self):
        self.ui.pushButton.clicked.connect(self._handle_register)
        self.ui.passwordLineEdit.returnPressed.connect(self._handle_register)
        self.ui.ifExist.linkActivated.connect(self._back_to_login)

    def _handle_register(self):
        """Обработка регистрации"""
        login_text = self.ui.loginLineEdit.text().strip()
        email = self.ui.emailLineEdit.text().strip()
        password = self.ui.passwordLineEdit.text()

        if not self._validate(login_text, email, password):
            return

        self._set_loading(True)

        worker = AsyncWorker.run_async(register(email, login_text, password))
        worker.signals.success.connect(self._on_success)
        worker.signals.error.connect(self._on_error)

    def _validate(self, login: str, email: str, password: str) -> bool:
        """Валидация данных"""
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

    def _on_success(self, data: dict):
        """Успешная регистрация"""
        QMessageBox.information(
            self,
            "Успешно",
            "Регистрация завершена! Теперь вы можете войти."
        )
        self.accept()

    def _on_error(self, error: Exception):
        """Ошибка регистрации"""
        self._set_loading(False)

        error_str = str(error).lower()

        if "already exists" in error_str or "409" in error_str:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Пользователь с таким логином или email уже существует"
            )
        else:
            QMessageBox.critical(self, "Ошибка", f"Ошибка регистрации: {error}")

    def _set_loading(self, loading: bool):
        self.ui.pushButton.setEnabled(not loading)
        self.ui.pushButton.setText("Регистрация..." if loading else "Зарегистрироваться")

    def _back_to_login(self):
        """Вернуться к авторизации"""
        self.reject()

#Сгенерировано ИИ
class AuthDialog(QDialog):
    """Диалог авторизации с интеграцией API"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.ui = Ui_AuthorizeWindow()
        self.ui.setupUi(self)

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.ui.pushButton.setText("Войти")
        self.ui.pushButton.setDefault(True)

        # Проверка доступности сервера
        self._check_server()

    def _connect_signals(self):
        """Подключение сигналов"""
        self.ui.pushButton.clicked.connect(self._handle_login)
        self.ui.passwordLineEdit.returnPressed.connect(self._handle_login)
        self.ui.registerLink.linkActivated.connect(self._open_register)

    def _check_server(self):
        """Проверка доступности сервера"""
        import httpx
        from client.config.settings import API_BASE_URL

        try:
            response = httpx.get(f"{API_BASE_URL}/health", timeout=2.0)
            if response.status_code == 200:
                self.setWindowTitle("Авторизация")
                return
        except:
            pass

        self.setWindowTitle("Авторизация ⚠️ (сервер недоступен)")

    def _handle_login(self):
        """Обработка входа"""
        username = self.ui.loginLineEdit.text().strip()
        password = self.ui.passwordLineEdit.text()

        if not self._validate_input(username, password):
            return

        self._set_loading(True)

        # Запускаем асинхронную авторизацию
        worker = AsyncWorker.run_async(self._do_login(username, password))
        worker.signals.success.connect(self._on_login_success)
        worker.signals.error.connect(self._on_login_error)

    def _validate_input(self, username: str, password: str) -> bool:
        """Валидация входных данных"""
        if not username:
            QMessageBox.warning(self, "Ошибка", "Введите логин")
            return False
        if not password:
            QMessageBox.warning(self, "Ошибка", "Введите пароль")
            return False
        return True

    async def _do_login(self, username: str, password: str):
        """Асинхронная авторизация"""
        # Получаем токен
        token_data = await login(username, password)
        token = token_data["access_token"]

        # Получаем данные пользователя
        user_data = await get_current_user(token)

        return {
            "token": token,
            "username": user_data.get("username", username),
            "user_id": user_data.get("id")
        }

    def _on_login_success(self, data: dict):
        """Успешная авторизация"""
        session.login(
            token=data["token"],
            username=data["username"],
            user_id=data.get("user_id")
        )
        self.accept()

    def _on_login_error(self, error: Exception):
        """Ошибка авторизации"""
        self._set_loading(False)

        error_str = str(error).lower()

        if "401" in error_str or "403" in error_str:
            QMessageBox.warning(
                self,
                "Ошибка входа",
                "Неверный логин или пароль"
            )
        elif "connection" in error_str:
            QMessageBox.critical(
                self,
                "Ошибка подключения",
                "Сервер недоступен. Проверьте подключение к интернету."
            )
        else:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось войти: {error}"
            )

    def _set_loading(self, loading: bool):
        """Переключение состояния загрузки"""
        self.ui.pushButton.setEnabled(not loading)
        self.ui.pushButton.setText("Вход..." if loading else "Войти")
        self.ui.loginLineEdit.setEnabled(not loading)
        self.ui.passwordLineEdit.setEnabled(not loading)

    def _open_register(self):
        """Открытие окна регистрации"""
        self.hide()
        reg_dialog = RegisterDialog(self.parent())

        if reg_dialog.exec() == QDialog.Accepted:
            # Регистрация успешна, можно подставить данные
            pass

        self.show()
        self.raise_()
        self.activateWindow()

class CanvasWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.graphicsView.setParent(None)
        self.ui.graphicsView.deleteLater()

        self.scene = GridScene(grid_size=10)

        self.graphicsView = ZoomableGraphicsView(self.scene, self.ui.centralwidget)

        layout = QVBoxLayout(self.ui.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.graphicsView)

        self.graphicsView.centerOn(500, 500)

        self.ui.graphicsView = self.graphicsView

        self.ui.graphicsView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.ui.graphicsView.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.ui.graphicsView.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.ui.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ui.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.ui.graphicsView.setTransform(QTransform())

        self.ui.graphicsView.centerOn(500, 500)

        self.ui.actionAddObject.triggered.connect(self.add_object)
        self.ui.actionEditObject.triggered.connect(self.edit_object)
        self.ui.actionDeleteObject.triggered.connect(self.delete_object)
        self.ui.actionSetArea.triggered.connect(self.set_area)
        self.ui.action_8.triggered.connect(self.open_auth_dialog)

        self.statusBar().showMessage("Масштаб: 1 м = 20 пикс. | Сетка: 0.5 м (1 клетка)")
        self.status_label = QLabel("")
        self.statusBar().addPermanentWidget(self.status_label)

        session.logged_in.connect(self._on_logged_in)
        session.logged_out.connect(self._on_logged_out)

        QTimer.singleShot(0, self._check_auth)

    # Сгенерировано ИИ
    def _check_auth(self):
        """Показываем окно входа при старте"""
        if not session.is_authenticated:
            dialog = AuthDialog(self)
            if dialog.exec() != QDialog.Accepted:
                self.close()  # Закрываем если не вошли

    # Сгенерировано ИИ
    def _on_logged_in(self, username):
        """Когда вошли"""
        self.statusBar().showMessage(f"Пользователь: {username}")
        # Здесь можно загрузить проекты пользователя

    # Сгенерировано ИИ
    def _on_logged_out(self):
        """Когда вышли"""
        self.statusBar().showMessage("Не авторизован")
        self.scene.clear()  # Очищаем сцену

    # Сгенерировано ИИ
    def open_auth_dialog(self):
        """Ручной вход через меню"""
        dialog = AuthDialog(self)
        dialog.exec()

    #Функция сгенерирована ИИ
    def set_area(self):
        dialog = SetAreaWindow(self)
        if dialog.exec() == QDialog.Accepted:
            width, height = dialog.get_values()
            if width and height:
                self.set_workspace_area(width, height)

    # Сгенерировано ИИ
    def set_workspace_area(self, width_m, height_m):
        # Удаляем старую площадку, если была
        for item in self.scene.items():
            if isinstance(item, WorkspaceArea):
                self.scene.removeItem(item)

        # Добавляем новую
        area = WorkspaceArea(width_m, height_m)
        self.scene.addItem(area)

        # Центрируем площадку в сцене
        scene_rect = self.scene.sceneRect()
        center_x = scene_rect.width() / 2 - (width_m * PIXELS_PER_METER) / 2
        center_y = scene_rect.height() / 2 - (height_m * PIXELS_PER_METER) / 2
        area.setPos(center_x, center_y)

    def get_workspace_area(self):
          for item in self.scene.items():
              if isinstance(item, WorkspaceArea):
                 return item
          return None

    def check_object_bounds(self, obj: SnappableObject):
        area = self.get_workspace_area()
        if not area:
            obj.set_outside_area(False)
            return False

        obj_rect = obj.mapToScene(obj.boundingRect()).boundingRect()
        area_rect = area.mapToScene(area.boundingRect()).boundingRect()

        is_outside = not area_rect.contains(obj_rect)

        obj.set_outside_area(is_outside)
        return is_outside

    def check_object_collisions(self):
        objects = [item for item in self.scene.items() if isinstance(item, SnappableObject)]

        for obj in objects:
            obj.set_overlapping(False)

        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects):
                if i >= j:
                    continue
                obj1_rect = obj1.mapToScene(obj1.boundingRect()).boundingRect()
                obj2_rect = obj2.mapToScene(obj2.boundingRect()).boundingRect()

                if obj1_rect.intersects(obj2_rect):
                    obj1.set_overlapping(True)
                    obj2.set_overlapping(True)

    #Метод сгенерирован ИИ
    def add_object(self):
        selected_type = self.ui.comboBox.currentText().strip() or "Объект"
        obj = SnappableObject(
            text=selected_type,
            width_m=6.0,
            height_m=4.0,
            color="#96C8FF",
            grid_size_m=0.5,
            pixels_per_meter=PIXELS_PER_METER
        )
        obj.geometryChanged.connect(lambda: self.on_object_moved(obj))
        self.scene.addItem(obj)
        obj.setPos(400, 400)
        self.check_object_bounds(obj)
        self.check_object_collisions()
        self.update_status_bar()

    def on_object_moved(self, obj):
        self.check_object_bounds(obj)
        self.check_object_collisions()
        self.update_status_bar()

    #Сгенерировано ИИ
    def update_status_bar(self):
        area = self.get_workspace_area()
        outside_names = []
        overlapping_names = []

        for item in self.scene.items():
            if isinstance(item, SnappableObject):
                if item._is_outside_area:
                    outside_names.append(item._text)
                if item._is_overlapping:
                    overlapping_names.append(item._text)

        messages = []
        if outside_names:
            messages.append("⚠️ Вне площадки: " + ", ".join(outside_names))
        if overlapping_names:
            messages.append("🟡 Пересекаются: " + ", ".join(overlapping_names))

        if messages:
            self.status_label.setText(" | ".join(messages))
        else:
            self.status_label.setText("")

    # Метод сгенерирован ИИ
    def edit_object(self):
        print("🔧 edit_object: started")
        selected = self.scene.selectedItems()
        if not selected:
            print("⚠️ No items selected")
            return

        item = selected[0]
        if not isinstance(item, SnappableObject):
            print("⚠️ Selected item is not editable")
            return

        # Текущие параметры
        cur_text = item._text
        cur_color = item._color.name()
        cur_w_m = item._width_m
        cur_h_m = item._height_m

        dlg = EditObjectWindow(
            self,
            initial_text=cur_text,
            initial_length=cur_w_m,
            initial_width=cur_h_m,
            initial_color=cur_color
        )
        if dlg.exec() != QDialog.Accepted:
            return

        changes = dlg.get_data()
        if not changes:
            return

        # Применяем изменения
        if "text" in changes:
            item.update_text(changes["text"])
        if "length" in changes:
            item._width_m = changes["length"]
        if "width" in changes:
            item._height_m = changes["width"]
        if "color" in changes:
            item.update_color(changes["color"])

        # Обновляем геометрию
        if "length" in changes or "width" in changes:
            item.prepareGeometryChange()
            item.update()

        if "length" in changes or "width" in changes or "text" in changes or "color" in changes:
            self.check_object_bounds(item)
            self.check_object_collisions()
            self.update_status_bar()

        print("✅ edit_object: completed")

    def delete_object(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CanvasWindow()
    window.show()
    sys.exit(app.exec())