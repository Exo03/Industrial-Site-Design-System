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
        RegisterWindow.setStyleSheet(u"/* \u041e\u0431\u0449\u0438\u0439 \u0444\u043e\u043d \u043e\u043a\u043d\u0430 \u0430\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u0438 */\n"
"QWidget {\n"
"    background-color: #121212;\n"
"    color: #FFFFFF;\n"
"    font-family: \"Segoe UI\", Arial, sans-serif;\n"
"}\n"
"\n"
"/* \u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f\" */\n"
"QLabel#titleLabel {\n"
"    font-size: 20pt;\n"
"    font-weight: bold;\n"
"    color: #FFFFFF;\n"
"    qproperty-alignment: AlignCenter;\n"
"    margin-bottom: 20px;\n"
"}\n"
"\n"
"/* \u041c\u0435\u0442\u043a\u0438 \"\u041b\u043e\u0433\u0438\u043d\", \"\u041f\u0430\u0440\u043e\u043b\u044c\" */\n"
"QLabel {\n"
"    color: #FFFFFF;\n"
"    font-size: 11pt;\n"
"    padding: 4px 0px;\n"
"}\n"
"\n"
"/* \u041f\u043e\u043b\u044f \u0432\u0432\u043e\u0434\u0430 */\n"
"QLineEdit {\n"
"    background-color: #1E1E1E;\n"
"    color: #FFFFFF;\n"
"    border: 1px solid #333333;\n"
"    padding: 6px 10px;\n"
""
                        "    border-radius: 4px;\n"
"    selection-background-color: #BB86FC;\n"
"    selection-color: black;\n"
"}\n"
"\n"
"/* \u041a\u043d\u043e\u043f\u043a\u0430 \"\u0412\u043e\u0439\u0442\u0438\" */\n"
"QPushButton {\n"
"    background-color: #1E1E1E;\n"
"    color: #FFFFFF;\n"
"    border: 1px solid #333333;\n"
"    padding: 8px 20px;\n"
"    border-radius: 4px;\n"
"    font-weight: 500;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #333333;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #BB86FC;\n"
"    color: black;\n"
"}\n"
"QLabel#ifExist {\n"
"    color: #BB86FC;\n"
"    text-decoration: underline;\n"
"    cursor: pointer;\n"
"    padding: 4px 0px;\n"
"    qproperty-alignment: AlignRight;\n"
"}")
        self.label = QLabel(RegisterWindow)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(160, 20, 138, 36))
        self.label.setStyleSheet(u"font-size: 16pt;")
        self.layoutWidget = QWidget(RegisterWindow)
        self.layoutWidget.setObjectName(u"layoutWidget1")
        self.layoutWidget.setGeometry(QRect(80, 60, 311, 226))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.loginLabel = QLabel(self.layoutWidget)
        self.loginLabel.setObjectName(u"loginLabel")

        self.verticalLayout_3.addWidget(self.loginLabel)

        self.loginLineEdit = QLineEdit(self.layoutWidget)
        self.loginLineEdit.setObjectName(u"loginLineEdit")

        self.verticalLayout_3.addWidget(self.loginLineEdit)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.emailLabel = QLabel(self.layoutWidget)
        self.emailLabel.setObjectName(u"emailLabel")

        self.verticalLayout_2.addWidget(self.emailLabel)

        self.emailLineEdit = QLineEdit(self.layoutWidget)
        self.emailLineEdit.setObjectName(u"emailLineEdit")

        self.verticalLayout_2.addWidget(self.emailLineEdit)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.passwordLabel = QLabel(self.layoutWidget)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.verticalLayout.addWidget(self.passwordLabel)

        self.passwordLineEdit = QLineEdit(self.layoutWidget)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")

        self.verticalLayout.addWidget(self.passwordLineEdit)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.layoutWidget1 = QWidget(RegisterWindow)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(150, 310, 183, 74))
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.layoutWidget1)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"font-size: 11pt;\n"
"")

        self.verticalLayout_5.addWidget(self.pushButton)

        self.ifExist = QLabel(self.layoutWidget1)
        self.ifExist.setObjectName(u"ifExist")

        self.verticalLayout_5.addWidget(self.ifExist)


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

