# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QMainWindow, QMenu,
                               QMenuBar, QSizePolicy, QStatusBar, QToolBar,
                               QWidget, QComboBox, QLabel, QHBoxLayout)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)

        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.actionSavePNG = QAction(MainWindow)
        self.actionSavePNG.setObjectName(u"actionSavePNG")
        self.actionSaveJSON = QAction(MainWindow)
        self.actionSaveJSON.setObjectName(u"actionSaveJSON")
        self.action_6 = QAction(MainWindow)
        self.action_6.setObjectName(u"action_6")
        self.action_7 = QAction(MainWindow)
        self.action_7.setObjectName(u"action_7")
        self.action_8 = QAction(MainWindow)
        self.action_8.setObjectName(u"action_8")
        self.action_10 = QAction(MainWindow)
        self.action_10.setObjectName(u"action_10")
        self.action_11 = QAction(MainWindow)
        self.action_11.setObjectName(u"action_11")
        self.action_12 = QAction(MainWindow)
        self.action_12.setObjectName(u"action_12")
        self.action_13 = QAction(MainWindow)
        self.action_13.setObjectName(u"action_13")
        self.actionAddObject = QAction(MainWindow)
        self.actionAddObject.setObjectName(u"actionAddObject")
        icon = QIcon()
        icon.addFile(u"./Icons/add_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAddObject.setIcon(icon)
        self.actionAddObject.setMenuRole(QAction.NoRole)
        self.actionEditObject = QAction(MainWindow)
        self.actionEditObject.setObjectName(u"actionEditObject")
        icon1 = QIcon()
        icon1.addFile(u"./Icons/edit_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionEditObject.setIcon(icon1)
        self.actionEditObject.setMenuRole(QAction.NoRole)
        self.actionDeleteObject = QAction(MainWindow)
        self.actionDeleteObject.setObjectName(u"actionDeleteObject")
        icon2 = QIcon()
        icon2.addFile(u"./Icons/delete_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionDeleteObject.setIcon(icon2)
        self.actionDeleteObject.setMenuRole(QAction.NoRole)
        self.actionSetArea = QAction(MainWindow)
        self.actionSetArea.setObjectName(u"actionSetArea")
        icon3 = QIcon()
        icon3.addFile(u"./Icons/activity_zone_24dp_FFFFFF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionSetArea.setIcon(icon3)
        self.actionSetArea.setMenuRole(QAction.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(-5, -9, 811, 511))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addSeparator()
        self.menu.addAction(self.actionSavePNG)
        self.menu.addAction(self.actionSaveJSON)
        self.menu.addSeparator()
        self.menu.addAction(self.action_6)
        self.menu_2.addAction(self.action_8)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_7)
        self.menu_3.addAction(self.action_10)
        self.menu_3.addAction(self.action_11)
        self.menu_3.addAction(self.action_12)
        self.menu_4.addAction(self.action_13)
        self.toolBar.addAction(self.actionAddObject)
        self.toolBar.addAction(self.actionEditObject)
        self.toolBar.addAction(self.actionSetArea)
        self.toolBar.addAction(self.actionDeleteObject)


        self.equipmentContainer = QWidget(self.toolBar)
        self.equipmentContainer.setObjectName(u"equipmentContainer")

        layout = QHBoxLayout(self.equipmentContainer)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.labelEquipment = QLabel("Оборудование:", self.equipmentContainer)
        self.labelEquipment.setObjectName(u"labelEquipment")

        self.comboBox = QComboBox(self.equipmentContainer)
        self.comboBox.setObjectName(u"equipmentComboBox")
        self.comboBox.addItems(["Насос",
    "Компрессор",
    "Теплообменник",
    "Реактор",
    "Дистилляционная колонна",
    "Котёл",
    "Турбина",
    "Турбина",
    "Электрогенератор",
    "Конденсатор",
    "Сепаратор",
    "Фильтр",
    "Сушитель",
    "Печь",
    "Электролизёр",
    "Холодильная установка",
    "Вентилятор",
    "Дробилка",
    "Мельница",
    "Элеватор",
    "Конвейер",
    "Пресс",
    "Экструдер",
    "Центрифуга",
    "Абсорбер",
    "Адсорбер",
    "Резервуар",
    "Газгольдер",
    "Нагреватель",
    "Криогенная установка",
    "Установка обратного осмоса",
    "Биореактор",
    "Автоклав",
    "Печь",
    "Смеситель",
    "Гранулятор",
    "Установка для нанесения покрытий",
    "Электростатический фильтр",
    "Скруббер",
    "Установка утилизации тепла",
    "Кислородная станция",
    "Установка для переработки отходов",
    "Машина для формовки",
    "Лебёдка",
    "Подъёмный кран",
    "Станок",
    "Установка для мойки деталей",
    "Охладитель",
    "Газоанализатор",
    "Установка автоматического пожаротушения"])


        self.equipmentContainer.setFixedHeight(32)

        layout.addWidget(self.labelEquipment)
        layout.addWidget(self.comboBox)

        self.toolBar.addWidget(self.equipmentContainer)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0444\u0430\u0439\u043b", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0444\u0430\u0439\u043b", None))
        self.actionSavePNG.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0432 PNG", None))
        self.actionSaveJSON.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0432 JSON", None))
        self.action_6.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0439\u0442\u0438 \u0438\u0437 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b", None))
        self.action_7.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b", None))
        self.action_8.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0444\u0438\u043b\u044c", None))
        self.action_10.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0432\u0435\u0442\u043b\u0430\u044f \u0442\u0435\u043c\u0430", None))
        self.action_11.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043c\u043d\u0430\u044f \u0442\u0435\u043c\u0430", None))
        self.action_12.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u0430\u044f \u0442\u0435\u043c\u0430", None))
        self.action_13.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u0445. \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0430", None))
        self.actionAddObject.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043e\u0431\u044a\u0435\u043a\u0442", None))
#if QT_CONFIG(shortcut)
        self.actionAddObject.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionEditObject.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043e\u0431\u044a\u0435\u043a\u0442", None))
#if QT_CONFIG(shortcut)
        self.actionEditObject.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.actionDeleteObject.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u043e\u0431\u044a\u0435\u043a\u0442", None))
#if QT_CONFIG(shortcut)
        self.actionDeleteObject.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionSetArea.setText(QCoreApplication.translate("MainWindow", u"actionSetArea", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0434", None))
        self.menu_4.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043c\u043e\u0449\u044c", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

