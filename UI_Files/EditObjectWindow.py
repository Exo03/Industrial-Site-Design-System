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
        Object_edit.setStyleSheet(u"QDialog {\n"
"        background-color: #1E1E1E;\n"
"        color: #FFFFFF;\n"
"        border: 1px solid #333333;\n"
"        border-radius: 8px;\n"
"        padding: 16px;\n"
"    }\n"
"\n"
"    QLabel {\n"
"        font-weight: bold;\n"
"        color: #FFFFFF;\n"
"        margin-bottom: 4px;\n"
"    }\n"
"\n"
"    QLineEdit {\n"
"        background-color: #2A2A2A;\n"
"        color: #FFFFFF;\n"
"        border: 1px solid #333333;\n"
"        border-radius: 4px;\n"
"        padding: 6px 8px;\n"
"    }\n"
"\n"
"    QLineEdit:focus {\n"
"        border: 1px solid #BB86FC;\n"
"        outline: none;\n"
"    }\n"
"\n"
"    /* \u041f\u043e\u043b\u0435 \u0434\u043b\u044f \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f \u0446\u0432\u0435\u0442\u0430 \u2014 \u0441 \u0437\u0430\u043b\u0438\u0432\u043a\u043e\u0439 */\n"
"    QLineEdit#colorDisplay {\n"
"        background-color: #121212;  /* \u0444\u043e\u043d \u2014 \u043a\u0430\u043a \u0443 \u0433\u043b\u0430\u0432\u043d\u043e\u0433\u043e \u043e"
                        "\u043a\u043d\u0430 */\n"
"        border: 1px solid #333333;\n"
"        border-radius: 4px;\n"
"        padding: 6px 8px;\n"
"    }\n"
"\n"
"    QPushButton {\n"
"        background-color: #2A2A2A;\n"
"        color: #FFFFFF;\n"
"        border: 1px solid #333333;\n"
"        border-radius: 4px;\n"
"        padding: 6px 16px;\n"
"        font-weight: 500;\n"
"    }\n"
"\n"
"    QPushButton:hover {\n"
"        background-color: #333333;\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #BB86FC;\n"
"        color: black;\n"
"    }\n"
"\n"
"    QPushButton#okButton {\n"
"        background-color: #BB86FC;\n"
"        color: black;\n"
"        border: 1px solid #BB86FC;\n"
"    }\n"
"\n"
"    QPushButton#okButton:hover {\n"
"        background-color: #CC99FF;\n"
"    }\n"
"\n"
"    QPushButton#okButton:pressed {\n"
"        background-color: #AA77DD;\n"
"    }\n"
"\n"
"    QPushButton#colorButton {\n"
"        background-color: #2A2A2A;\n"
"        border: 1px solid #333333;\n"
"        b"
                        "order-radius: 4px;\n"
"        padding: 0;\n"
"    }\n"
"\n"
"    QPushButton#colorButton:hover {\n"
"        background-color: #333333;\n"
"    }")
        self.layoutWidget = QWidget(Object_edit)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 225, 290))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.TextLabel = QLabel(self.layoutWidget)
        self.TextLabel.setObjectName(u"TextLabel")

        self.verticalLayout.addWidget(self.TextLabel)

        self.textLineEdit = QLineEdit(self.layoutWidget)
        self.textLineEdit.setObjectName(u"textLineEdit")

        self.verticalLayout.addWidget(self.textLineEdit)

        self.LengthLabel = QLabel(self.layoutWidget)
        self.LengthLabel.setObjectName(u"LengthLabel")

        self.verticalLayout.addWidget(self.LengthLabel)

        self.lengthLineEdit = QLineEdit(self.layoutWidget)
        self.lengthLineEdit.setObjectName(u"lengthLineEdit")

        self.verticalLayout.addWidget(self.lengthLineEdit)

        self.WidthLabel = QLabel(self.layoutWidget)
        self.WidthLabel.setObjectName(u"WidthLabel")

        self.verticalLayout.addWidget(self.WidthLabel)

        self.widthLineEdit = QLineEdit(self.layoutWidget)
        self.widthLineEdit.setObjectName(u"widthLineEdit")

        self.verticalLayout.addWidget(self.widthLineEdit)

        self.ColorLabel = QLabel(self.layoutWidget)
        self.ColorLabel.setObjectName(u"ColorLabel")

        self.verticalLayout.addWidget(self.ColorLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.colorDisplay = QLineEdit(self.layoutWidget)
        self.colorDisplay.setObjectName(u"colorDisplay")

        self.horizontalLayout.addWidget(self.colorDisplay)

        self.colorChooseButton = QPushButton(self.layoutWidget)
        self.colorChooseButton.setObjectName(u"colorChooseButton")

        self.horizontalLayout.addWidget(self.colorChooseButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


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

