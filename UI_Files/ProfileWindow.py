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
        Dialog.resize(589, 316)
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
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setPixmap(QPixmap("Icons/arrow_back_24dp_FFFFFF.svg"))

        self.horizontalLayout.addWidget(self.label_3)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.label.setFont(font1)

        self.horizontalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setPixmap(QPixmap("Icons/edit_24dp_FFFFFF.svg"))

        self.horizontalLayout.addWidget(self.label_2)


        self.verticalLayout.addWidget(self.frame)

        self.ProfIcon = QLabel(Dialog)
        self.ProfIcon.setObjectName(u"ProfIcon")
        self.ProfIcon.setPixmap(QPixmap("Icons/account_circle_48dp_FFFFFF.svg"))
        self.ProfIcon.setScaledContents(False)

        self.verticalLayout.addWidget(self.ProfIcon)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.label_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setMargin(10)

        self.verticalLayout.addWidget(self.label_4)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setMargin(10)

        self.verticalLayout.addWidget(self.label_5)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(21)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(False)
        self.pushButton.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile("Icons/profile_delete_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile("Icons/logout_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Profile", None))
        self.label_3.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"\u041f\u0440\u043e\u0444\u0438\u043b\u044c", None))
        self.label_2.setText("")
        self.ProfIcon.setText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u041b\u043e\u0433\u0438\u043d", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Email", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0430\u043a\u043a\u0430\u0443\u043d\u0442", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"\u0412\u044b\u0439\u0442\u0438 \u0438\u0437 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430", None))
    # retranslateUi

