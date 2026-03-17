from PySide6.QtCore import QObject, Signal


class SessionManager(QObject):
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
        self._username = "Test username"
        self._email = "Test email"
        self._initialized = True

    @property
    def token(self):
        return self._token

    @property
    def email(self):
        return self._email

    @property
    def username(self):
        return self._username

    @property
    def is_authenticated(self):
        return self._token is not None


    def login(self, token, username, email=None, user_id=None):
        self._token = token
        self._username = username
        self._email = email
        self.logged_in.emit(username)

    def logout(self):
        self._token = None
        self._username = None
        self.logged_out.emit()


# Глобальный экземпляр
session = SessionManager()