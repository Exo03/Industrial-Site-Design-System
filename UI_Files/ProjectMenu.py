# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProjectMenu.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ProjectMenuWindow(object):
    def setupUi(self, ProjectMenuWindow):
        if not ProjectMenuWindow.objectName():
            ProjectMenuWindow.setObjectName(u"ProjectMenuWindow")
        ProjectMenuWindow.resize(703, 499)

        self.verticalLayout_2 = QVBoxLayout(ProjectMenuWindow)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(150, 0, 150, 150)
        self.label = QLabel(ProjectMenuWindow)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.label)

        self.pushButton = QPushButton(ProjectMenuWindow)
        self.pushButton.setObjectName(u"pushButton")
        icon = QIcon()
        icon.addFile("Icons/add_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(ProjectMenuWindow)
        self.pushButton_2.setObjectName(u"pushButton_2")
        icon1 = QIcon()
        icon1.addFile("Icons/folder_open_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon1)

        self.verticalLayout.addWidget(self.pushButton_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(ProjectMenuWindow)

        QMetaObject.connectSlotsByName(ProjectMenuWindow)
    # setupUi

    def retranslateUi(self, ProjectMenuWindow):
        ProjectMenuWindow.setWindowTitle(QCoreApplication.translate("ProjectMenuWindow", u"Menu", None))
        self.label.setText(QCoreApplication.translate("ProjectMenuWindow", u"\u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c", None))
        self.pushButton.setText(QCoreApplication.translate("ProjectMenuWindow", u"\u041d\u043e\u0432\u044b\u0439 \u043f\u0440\u043e\u0435\u043a\u0442", None))
        self.pushButton_2.setText(QCoreApplication.translate("ProjectMenuWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043f\u0440\u043e\u0435\u043a\u0442", None))
    # retranslateUi

