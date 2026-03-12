from ...ui.widgets.themed_dialog import ThemedDialog
from UI_Files.ProfileWindow import Ui_Profile
from client.session_manager import session


class ProfileDialog(ThemedDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Profile()
        self.ui.setupUi(self)

        self.ui.label_4.setText(session.username)
        self.ui.label_5.setText(session.email)