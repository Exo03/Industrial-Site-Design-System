# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProfileWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Profile(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(589, 344)
        font = QFont()
        font.setBold(True)
        Dialog.setFont(font)

        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(193)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.exitButton = QPushButton(self.frame)
        self.exitButton.setObjectName(u"exitButton")
        icon = QIcon()
        icon.addFile(u"../Icons/arrow_back_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exitButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.exitButton)

        self.titleLabel = QLabel(self.frame)
        self.titleLabel.setObjectName(u"titleLabel")
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.titleLabel.setFont(font1)

        self.horizontalLayout.addWidget(self.titleLabel)

        self.editButton = QPushButton(self.frame)
        self.editButton.setObjectName(u"editButton")
        icon1 = QIcon()
        icon1.addFile(u"../Icons/edit_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.editButton.setIcon(icon1)

        self.horizontalLayout.addWidget(self.editButton)


        self.verticalLayout.addWidget(self.frame)

        self.ProfIcon = QLabel(Dialog)
        self.ProfIcon.setObjectName(u"ProfIcon")
        self.ProfIcon.setStyleSheet(u"qproperty-alignment: AlignCenter;")
        self.ProfIcon.setPixmap(QPixmap(u"../Icons/account_circle_48dp_FFFFFF.svg"))
        self.ProfIcon.setScaledContents(False)

        self.verticalLayout.addWidget(self.ProfIcon)

        self.login_label = QLabel(Dialog)
        self.login_label.setObjectName(u"login_label")
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.login_label.setMargin(10)

        self.verticalLayout.addWidget(self.login_label)

        self.emailLabel = QLabel(Dialog)
        self.emailLabel.setObjectName(u"emailLabel")
        self.emailLabel.setScaledContents(False)
        self.emailLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.emailLabel.setMargin(10)

        self.verticalLayout.addWidget(self.emailLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(21)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.deleteButton = QPushButton(Dialog)
        self.deleteButton.setObjectName(u"deleteButton")
        icon2 = QIcon()
        icon2.addFile(u"../Icons/delete_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteButton.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.deleteButton)

        self.logoutButton = QPushButton(Dialog)
        self.logoutButton.setObjectName(u"logoutButton")
        icon3 = QIcon()
        icon3.addFile(u"../Icons/logout_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.logoutButton.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.logoutButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Profile", None))
        self.exitButton.setText("")
        self.titleLabel.setText(QCoreApplication.translate("Dialog", u"\u041f\u0440\u043e\u0444\u0438\u043b\u044c", None))
        self.editButton.setText("")
        self.ProfIcon.setText("")
        self.login_label.setText(QCoreApplication.translate("Dialog", u"\u041b\u043e\u0433\u0438\u043d", None))
        self.emailLabel.setText(QCoreApplication.translate("Dialog", u"Email", None))
        self.deleteButton.setText(QCoreApplication.translate("Dialog", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0430\u043a\u043a\u0430\u0443\u043d\u0442", None))
        self.logoutButton.setText(QCoreApplication.translate("Dialog", u"\u0412\u044b\u0439\u0442\u0438 \u0438\u0437 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430", None))
    # retranslateUi

