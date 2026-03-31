# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ObjectRow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_ObjectRow(object):
    def setupUi(self, ObjectRow):
        if not ObjectRow.objectName():
            ObjectRow.setObjectName(u"ObjectRow")
        ObjectRow.resize(636, 128)
        self.horizontalLayout = QHBoxLayout(ObjectRow)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.objectRow = QFrame(ObjectRow)
        self.objectRow.setObjectName(u"objectRow")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.objectRow.sizePolicy().hasHeightForWidth())
        self.objectRow.setSizePolicy(sizePolicy)

        self.object = QHBoxLayout(self.objectRow)
        self.object.setObjectName(u"object")
        self.objectNameLabel = QLabel(self.objectRow)
        self.objectNameLabel.setObjectName(u"objectNameLabel")

        self.object.addWidget(self.objectNameLabel)

        self.horizontalSpacer = QSpacerItem(208, 23, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.object.addItem(self.horizontalSpacer)

        self.editButton = QPushButton(self.objectRow)
        self.editButton.setObjectName(u"editButton")
        icon = QIcon()
        icon.addFile(u"../Icons/edit_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.editButton.setIcon(icon)

        self.object.addWidget(self.editButton)

        self.deleteButton = QPushButton(self.objectRow)
        self.deleteButton.setObjectName(u"deleteButton")
        icon1 = QIcon()
        icon1.addFile(u"../Icons/delete_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteButton.setIcon(icon1)

        self.object.addWidget(self.deleteButton)


        self.horizontalLayout.addWidget(self.objectRow)


        self.retranslateUi(ObjectRow)

        QMetaObject.connectSlotsByName(ObjectRow)
    # setupUi

    def retranslateUi(self, ObjectRow):
        ObjectRow.setWindowTitle(QCoreApplication.translate("ObjectRow", u"objectRow", None))
        self.objectNameLabel.setText(QCoreApplication.translate("ObjectRow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:400;\">\u041e\u0431\u044a\u0435\u043a\u0442 1</span></p></body></html>", None))
        self.editButton.setText("")
        self.deleteButton.setText("")
    # retranslateUi

