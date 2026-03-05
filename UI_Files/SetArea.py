# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetArea.ui'
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
    QLabel, QLineEdit, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_SetArea(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(227, 196)
        Dialog.setStyleSheet(u"QDialog {\n"
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
"        color: b"
                        "lack;\n"
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
"    }")
        self.verticalLayout_4 = QVBoxLayout(Dialog)
        self.verticalLayout_4.setSpacing(14)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelAreaH = QLabel(Dialog)
        self.labelAreaH.setObjectName(u"labelAreaH")
        self.labelAreaH.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)

        self.verticalLayout_2.addWidget(self.labelAreaH)

        self.heightLineEdit = QLineEdit(Dialog)
        self.heightLineEdit.setObjectName(u"heightLineEdit")

        self.verticalLayout_2.addWidget(self.heightLineEdit)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelAreaW = QLabel(Dialog)
        self.labelAreaW.setObjectName(u"labelAreaW")
        self.labelAreaW.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)

        self.verticalLayout.addWidget(self.labelAreaW)

        self.widthLineEdit = QLineEdit(Dialog)
        self.widthLineEdit.setObjectName(u"widthLineEdit")

        self.verticalLayout.addWidget(self.widthLineEdit)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.labelAreaH.setText(QCoreApplication.translate("Dialog", u"\u0412\u044b\u0441\u043e\u0442\u0430 \u043f\u043b\u043e\u0449\u0430\u0434\u043a\u0438:", None))
        self.labelAreaW.setText(QCoreApplication.translate("Dialog", u"\u0428\u0438\u0440\u0438\u043d\u0430 \u043f\u043b\u043e\u0449\u0430\u0434\u043a\u0438:", None))
    # retranslateUi

