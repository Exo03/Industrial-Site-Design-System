# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EditObjectWindow.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Object_edit(object):
    def setupUi(self, Object_edit):
        if not Object_edit.objectName():
            Object_edit.setObjectName(u"Object_edit")
        Object_edit.resize(240, 309)

        self.verticalLayout_2 = QVBoxLayout(Object_edit)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TextLabel = QLabel(Object_edit)
        self.TextLabel.setObjectName(u"TextLabel")

        self.verticalLayout.addWidget(self.TextLabel)

        self.textLineEdit = QLineEdit(Object_edit)
        self.textLineEdit.setObjectName(u"textLineEdit")

        self.verticalLayout.addWidget(self.textLineEdit)

        self.LengthLabel = QLabel(Object_edit)
        self.LengthLabel.setObjectName(u"LengthLabel")

        self.verticalLayout.addWidget(self.LengthLabel)

        self.lengthLineEdit = QLineEdit(Object_edit)
        self.lengthLineEdit.setObjectName(u"lengthLineEdit")

        self.verticalLayout.addWidget(self.lengthLineEdit)

        self.WidthLabel = QLabel(Object_edit)
        self.WidthLabel.setObjectName(u"WidthLabel")

        self.verticalLayout.addWidget(self.WidthLabel)

        self.widthLineEdit = QLineEdit(Object_edit)
        self.widthLineEdit.setObjectName(u"widthLineEdit")

        self.verticalLayout.addWidget(self.widthLineEdit)

        self.ColorLabel = QLabel(Object_edit)
        self.ColorLabel.setObjectName(u"ColorLabel")

        self.verticalLayout.addWidget(self.ColorLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.colorDisplay = QLineEdit(Object_edit)
        self.colorDisplay.setObjectName(u"colorDisplay")

        self.horizontalLayout.addWidget(self.colorDisplay)

        self.colorChooseButton = QPushButton(Object_edit)
        self.colorChooseButton.setObjectName(u"colorChooseButton")

        self.horizontalLayout.addWidget(self.colorChooseButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Object_edit)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Object_edit)
        self.buttonBox.accepted.connect(Object_edit.accept)
        self.buttonBox.rejected.connect(Object_edit.reject)

        QMetaObject.connectSlotsByName(Object_edit)
    # setupUi

    def retranslateUi(self, Object_edit):
        Object_edit.setWindowTitle(QCoreApplication.translate("Object_edit", u"Dialog", None))
        self.TextLabel.setText(QCoreApplication.translate("Object_edit", u"\u0422\u0435\u043a\u0441\u0442:  ", None))
        self.LengthLabel.setText(QCoreApplication.translate("Object_edit", u"\u0414\u043b\u0438\u043d\u0430:", None))
        self.WidthLabel.setText(QCoreApplication.translate("Object_edit", u"\u0428\u0438\u0440\u0438\u043d\u0430:", None))
        self.ColorLabel.setText(QCoreApplication.translate("Object_edit", u"\u0426\u0432\u0435\u0442:", None))
        self.colorChooseButton.setText(QCoreApplication.translate("Object_edit", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0446\u0432\u0435\u0442", None))
    # retranslateUi

