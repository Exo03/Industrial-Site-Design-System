# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AuthorizeWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_AuthorizeWindow(object):
    def setupUi(self, AuthorizeWindow):
        if not AuthorizeWindow.objectName():
            AuthorizeWindow.setObjectName(u"AuthorizeWindow")
        AuthorizeWindow.resize(507, 345)
        AuthorizeWindow.setStyleSheet(u"/* \u041e\u0431\u0449\u0438\u0439 \u0444\u043e\u043d \u043e\u043a\u043d\u0430 \u0430\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u0438 */\n"
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
"\n"
"/* \u0413\u0438\u043f\u0435\u0440\u0441\u0441\u044b\u043b\u043a\u0438: \"\u0417\u0430\u0431\u044b\u043b\u0438 \u043f\u0430\u0440\u043e\u043b\u044c?\", \"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f\" */\n"
"QLabel#forgotPasswordLink,\n"
"QLabel#registerLink {\n"
"    color: #BB86FC;\n"
"    text-decoration: underline;\n"
"    cursor: pointer;\n"
"    padding: 4px 0px;\n"
"    qproperty-alignment: AlignRight;\n"
"}\n"
"\n"
"QLabel#reg"
                        "isterLink {\n"
"    qproperty-alignment: AlignCenter;\n"
"    margin-top: 10px;\n"
"}\n"
"\n"
"QLabel#forgotPasswordLink:hover,\n"
"QLabel#registerLink:hover {\n"
"    color: #FFFFFF;\n"
"}")
        self.verticalLayout = QVBoxLayout(AuthorizeWindow)
        self.verticalLayout.setSpacing(24)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.authLabel = QLabel(AuthorizeWindow)
        self.authLabel.setObjectName(u"authLabel")
        self.authLabel.setStyleSheet(u"font-size: 20px;")
        self.authLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.authLabel)

        self.paslogLayout = QVBoxLayout()
        self.paslogLayout.setSpacing(18)
        self.paslogLayout.setObjectName(u"paslogLayout")
        self.logLayout = QVBoxLayout()
        self.logLayout.setSpacing(0)
        self.logLayout.setObjectName(u"logLayout")
        self.loginLabel = QLabel(AuthorizeWindow)
        self.loginLabel.setObjectName(u"loginLabel")
        self.loginLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.loginLabel.setLineWidth(0)
        self.loginLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.logLayout.addWidget(self.loginLabel)

        self.loginLineEdit = QLineEdit(AuthorizeWindow)
        self.loginLineEdit.setObjectName(u"loginLineEdit")
        self.loginLineEdit.setStyleSheet(u"")

        self.logLayout.addWidget(self.loginLineEdit)


        self.paslogLayout.addLayout(self.logLayout)

        self.pasLayout = QFormLayout()
        self.pasLayout.setObjectName(u"pasLayout")
        self.pasLayout.setHorizontalSpacing(0)
        self.pasLayout.setVerticalSpacing(0)
        self.passwordLabel = QLabel(AuthorizeWindow)
        self.passwordLabel.setObjectName(u"passwordLabel")
        self.passwordLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.pasLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.passwordLabel)

        self.passwordLineEdit = QLineEdit(AuthorizeWindow)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setStyleSheet(u"")

        self.pasLayout.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.passwordLineEdit)

        self.forgotPasswordLink = QLabel(AuthorizeWindow)
        self.forgotPasswordLink.setObjectName(u"forgotPasswordLink")
        self.forgotPasswordLink.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.pasLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.forgotPasswordLink)


        self.paslogLayout.addLayout(self.pasLayout)


        self.verticalLayout.addLayout(self.paslogLayout)

        self.enterLayout = QVBoxLayout()
        self.enterLayout.setSpacing(0)
        self.enterLayout.setObjectName(u"enterLayout")
        self.pushButton = QPushButton(AuthorizeWindow)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"font-size: 11pt;")

        self.enterLayout.addWidget(self.pushButton)

        self.registerLink = QLabel(AuthorizeWindow)
        self.registerLink.setObjectName(u"registerLink")
        self.registerLink.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.enterLayout.addWidget(self.registerLink)


        self.verticalLayout.addLayout(self.enterLayout)


        self.retranslateUi(AuthorizeWindow)

        QMetaObject.connectSlotsByName(AuthorizeWindow)
    # setupUi

    def retranslateUi(self, AuthorizeWindow):
        AuthorizeWindow.setWindowTitle(QCoreApplication.translate("AuthorizeWindow", u"Authorize", None))
        self.authLabel.setText(QCoreApplication.translate("AuthorizeWindow", u"<b>\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f</b>", None))
        self.loginLabel.setText(QCoreApplication.translate("AuthorizeWindow", u"\u041b\u043e\u0433\u0438\u043d", None))
        self.passwordLabel.setText(QCoreApplication.translate("AuthorizeWindow", u"\u041f\u0430\u0440\u043e\u043b\u044c", None))
        self.forgotPasswordLink.setText(QCoreApplication.translate("AuthorizeWindow", u"\u0417\u0430\u0431\u044b\u043b\u0438 \u043f\u0430\u0440\u043e\u043b\u044c?", None))
        self.pushButton.setText(QCoreApplication.translate("AuthorizeWindow", u"\u0412\u043e\u0439\u0442\u0438", None))
        self.registerLink.setText(QCoreApplication.translate("AuthorizeWindow", u"<html><head/><body><p align=\"center\"><a href=\"#\">\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f</a></p></body></html>", None))
    # retranslateUi

