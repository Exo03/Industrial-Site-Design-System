# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RegisterWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        if not RegisterWindow.objectName():
            RegisterWindow.setObjectName(u"RegisterWindow")
        RegisterWindow.resize(486, 406)

        self.verticalLayout_6 = QVBoxLayout(RegisterWindow)
        self.verticalLayout_6.setSpacing(27)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label = QLabel(RegisterWindow)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font-size: 16pt;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_6.addWidget(self.label)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(16)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.loginLabel = QLabel(RegisterWindow)
        self.loginLabel.setObjectName(u"loginLabel")

        self.verticalLayout_3.addWidget(self.loginLabel)

        self.loginLineEdit = QLineEdit(RegisterWindow)
        self.loginLineEdit.setObjectName(u"loginLineEdit")

        self.verticalLayout_3.addWidget(self.loginLineEdit)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.emailLabel = QLabel(RegisterWindow)
        self.emailLabel.setObjectName(u"emailLabel")

        self.verticalLayout_2.addWidget(self.emailLabel)

        self.emailLineEdit = QLineEdit(RegisterWindow)
        self.emailLineEdit.setObjectName(u"emailLineEdit")

        self.verticalLayout_2.addWidget(self.emailLineEdit)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.passwordLabel = QLabel(RegisterWindow)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.verticalLayout.addWidget(self.passwordLabel)

        self.passwordLineEdit = QLineEdit(RegisterWindow)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")

        self.verticalLayout.addWidget(self.passwordLineEdit)


        self.verticalLayout_4.addLayout(self.verticalLayout)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.pushButton = QPushButton(RegisterWindow)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_5.addWidget(self.pushButton)

        self.ifExist = QLabel(RegisterWindow)
        self.ifExist.setObjectName(u"ifExist")

        self.verticalLayout_5.addWidget(self.ifExist)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)


        self.retranslateUi(RegisterWindow)

        QMetaObject.connectSlotsByName(RegisterWindow)
    # setupUi

    def retranslateUi(self, RegisterWindow):
        RegisterWindow.setWindowTitle(QCoreApplication.translate("RegisterWindow", u"Register", None))
        self.label.setText(QCoreApplication.translate("RegisterWindow", u"<b>\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f</b>", None))
        self.loginLabel.setText(QCoreApplication.translate("RegisterWindow", u"\u041b\u043e\u0433\u0438\u043d", None))
        self.emailLabel.setText(QCoreApplication.translate("RegisterWindow", u"Email", None))
        self.passwordLabel.setText(QCoreApplication.translate("RegisterWindow", u"\u041f\u0430\u0440\u043e\u043b\u044c", None))
        self.pushButton.setText(QCoreApplication.translate("RegisterWindow", u"\u0417\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c\u0441\u044f", None))
        self.ifExist.setText(QCoreApplication.translate("RegisterWindow", u"<html><head/><body><p align=\"center\"><a href=\"#\">\u0423\u0436\u0435 \u0435\u0441\u0442\u044c \u0430\u043a\u043a\u0430\u0443\u043d\u0442?</a></p></body></html>", None))
    # retranslateUi

