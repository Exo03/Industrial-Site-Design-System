# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddObjectWindow.ui'
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
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_AddObject(object):
    def setupUi(self, AddObject):
        if not AddObject.objectName():
            AddObject.setObjectName(u"AddObject")
        AddObject.resize(638, 433)

        self.verticalLayout = QVBoxLayout(AddObject)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 9, 9, 9)
        self.titleFrame = QFrame(AddObject)
        self.titleFrame.setObjectName(u"titleFrame")

        self.horizontalLayout = QHBoxLayout(self.titleFrame)
        self.horizontalLayout.setSpacing(26)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(1, -1, -1, -1)
        self.backButton = QPushButton(self.titleFrame)
        self.backButton.setObjectName(u"backButton")
        icon = QIcon()
        icon.addFile(u"../Icons/arrow_back_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.backButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.backButton)

        self.titleLabel = QLabel(self.titleFrame)
        self.titleLabel.setObjectName(u"titleLabel")

        self.horizontalLayout.addWidget(self.titleLabel)

        self.addButton = QPushButton(self.titleFrame)
        self.addButton.setObjectName(u"addButton")
        icon1 = QIcon()
        icon1.addFile(u"../Icons/add_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addButton.setIcon(icon1)

        self.horizontalLayout.addWidget(self.addButton)


        self.verticalLayout.addWidget(self.titleFrame)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.addAllButton = QPushButton(AddObject)
        self.addAllButton.setObjectName(u"addAllButton")
        icon2 = QIcon()
        icon2.addFile(u"../Icons/check_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addAllButton.setIcon(icon2)

        self.verticalLayout.addWidget(self.addAllButton)


        self.retranslateUi(AddObject)

        QMetaObject.connectSlotsByName(AddObject)
    # setupUi

    def retranslateUi(self, AddObject):
        AddObject.setWindowTitle(QCoreApplication.translate("AddObject", u"Add Objects", None))
        self.backButton.setText("")
        self.titleLabel.setText(QCoreApplication.translate("AddObject", u"\u0414\u043e\u0431\u0430\u0432\u044c\u0442\u0435 \u043e\u0431\u044a\u0435\u043a\u0442\u044b", None))
        self.addButton.setText("")
        self.addAllButton.setText(QCoreApplication.translate("AddObject", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
    # retranslateUi

