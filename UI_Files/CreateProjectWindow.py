# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CreateProjectWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_CreateProject(object):
    def setupUi(self, CreateProject):
        if not CreateProject.objectName():
            CreateProject.setObjectName(u"CreateProject")
        CreateProject.resize(500, 315)
        CreateProject.setStyleSheet(u"background-color: #121212;")
        self.verticalLayout_2 = QVBoxLayout(CreateProject)
        self.verticalLayout_2.setSpacing(39)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(15, 15, -1, 15)
        self.label = QLabel(CreateProject)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font-size: 18px;\n"
"font-weight: bold;\n"
"qproperty-alignment: AlignCenter;")

        self.verticalLayout_2.addWidget(self.label)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.proj_name = QVBoxLayout()
        self.proj_name.setSpacing(4)
        self.proj_name.setObjectName(u"proj_name")
        self.label_2 = QLabel(CreateProject)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font-size: 12px;\n"
"font-weight: normal;\n"
"qproperty-alignment: AlignLeft;")

        self.proj_name.addWidget(self.label_2)

        self.lineEdit = QLineEdit(CreateProject)
        self.lineEdit.setObjectName(u"lineEdit")

        self.proj_name.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.proj_name)

        self.discript = QVBoxLayout()
        self.discript.setSpacing(4)
        self.discript.setObjectName(u"discript")
        self.label_3 = QLabel(CreateProject)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font-size: 12px;\n"
"font-weight: normal;\n"
"qproperty-alignment: AlignLeft;")

        self.discript.addWidget(self.label_3)

        self.plainTextEdit = QPlainTextEdit(CreateProject)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.discript.addWidget(self.plainTextEdit)


        self.verticalLayout.addLayout(self.discript)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.buttons = QHBoxLayout()
        self.buttons.setSpacing(4)
        self.buttons.setObjectName(u"buttons")
        self.pushButton = QPushButton(CreateProject)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1E1E1E;\n"
"    color: #FFFFFF;\n"
"    border: 1px solid #333333;\n"
"    border-radius: 4px;\n"
"    font-weight: 500;\n"
"	text-align: center;\n"
"	height: 24px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #333333;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #BB86FC;\n"
"    color: black;\n"
"}")

        self.buttons.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(CreateProject)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"    background-color: #1E1E1E;\n"
"    color: #FFFFFF;\n"
"    border: 1px solid #333333;\n"
"    border-radius: 4px;\n"
"    font-weight: 500;\n"
"	text-align: center;\n"
"	height: 24px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #333333;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #BB86FC;\n"
"    color: black;\n"
"}")

        self.buttons.addWidget(self.pushButton_2)


        self.verticalLayout_2.addLayout(self.buttons)


        self.retranslateUi(CreateProject)

        QMetaObject.connectSlotsByName(CreateProject)
    # setupUi

    def retranslateUi(self, CreateProject):
        CreateProject.setWindowTitle(QCoreApplication.translate("CreateProject", u"Create", None))
        self.label.setText(QCoreApplication.translate("CreateProject", u"<html><head/><body><p>\u0421\u043e\u0437\u0434\u0430\u0439\u0442\u0435 \u043f\u0440\u043e\u0435\u043a\u0442</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("CreateProject", u"\u0418\u043c\u044f \u043f\u0440\u043e\u0435\u043a\u0442\u0430", None))
        self.lineEdit.setText(QCoreApplication.translate("CreateProject", u"New project", None))
        self.label_3.setText(QCoreApplication.translate("CreateProject", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430", None))
        self.pushButton.setText(QCoreApplication.translate("CreateProject", u"OK", None))
        self.pushButton_2.setText(QCoreApplication.translate("CreateProject", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

