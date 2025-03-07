# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CoB2n appLvSRBL.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1060)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowTitle(u"CoB2n")
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, -1, 1921, 1041))
        self.tabWidget.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.chart = QGroupBox(self.tab)
        self.chart.setObjectName(u"chart")
        self.chart.setGeometry(QRect(0, 50, 1401, 691))
        self.charTab1 = QGroupBox(self.tab)
        self.charTab1.setObjectName(u"charTab1")
        self.charTab1.setGeometry(QRect(0, 0, 1401, 41))
        self.label_2 = QLabel(self.charTab1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 14, 71, 16))
        self.access_key = QLineEdit(self.charTab1)
        self.access_key.setObjectName(u"access_key")
        self.access_key.setGeometry(QRect(90, 10, 191, 21))
        self.save_button = QPushButton(self.charTab1)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setGeometry(QRect(690, 10, 31, 21))
        self.api_select = QComboBox(self.charTab1)
        self.api_select.addItem("")
        self.api_select.setObjectName(u"api_select")
        self.api_select.setGeometry(QRect(580, 10, 101, 22))
        self.secret_key = QLineEdit(self.charTab1)
        self.secret_key.setObjectName(u"secret_key")
        self.secret_key.setGeometry(QRect(380, 10, 191, 21))
        self.label_4 = QLabel(self.charTab1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(300, 14, 71, 16))
        self.buy_sell = QGroupBox(self.tab)
        self.buy_sell.setObjectName(u"buy_sell")
        self.buy_sell.setGeometry(QRect(1410, 150, 491, 861))
        self.coin_selete = QComboBox(self.buy_sell)
        self.coin_selete.setObjectName(u"coin_selete")
        self.coin_selete.setGeometry(QRect(10, 10, 151, 22))
        self.buy_button = QPushButton(self.buy_sell)
        self.buy_button.setObjectName(u"buy_button")
        self.buy_button.setGeometry(QRect(320, 830, 75, 23))
        self.persent_10 = QCheckBox(self.buy_sell)
        self.persent_10.setObjectName(u"persent_10")
        self.persent_10.setGeometry(QRect(10, 810, 51, 16))
        self.label_5 = QLabel(self.buy_sell)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(260, 810, 61, 16))
        self.direct_input_2 = QLineEdit(self.buy_sell)
        self.direct_input_2.setObjectName(u"direct_input_2")
        self.direct_input_2.setGeometry(QRect(320, 810, 161, 16))
        self.buy_button_2 = QPushButton(self.buy_sell)
        self.buy_button_2.setObjectName(u"buy_button_2")
        self.buy_button_2.setGeometry(QRect(410, 830, 75, 23))
        self.persent_50 = QCheckBox(self.buy_sell)
        self.persent_50.setObjectName(u"persent_50")
        self.persent_50.setGeometry(QRect(110, 810, 51, 16))
        self.persent_max = QCheckBox(self.buy_sell)
        self.persent_max.setObjectName(u"persent_max")
        self.persent_max.setGeometry(QRect(210, 810, 51, 16))
        self.groupBox_4 = QGroupBox(self.buy_sell)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 70, 471, 731))
        self.persent_75 = QCheckBox(self.buy_sell)
        self.persent_75.setObjectName(u"persent_75")
        self.persent_75.setGeometry(QRect(160, 810, 51, 16))
        self.persent_25 = QCheckBox(self.buy_sell)
        self.persent_25.setObjectName(u"persent_25")
        self.persent_25.setGeometry(QRect(60, 810, 51, 16))
        self.coin_selete_2 = QComboBox(self.buy_sell)
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.setObjectName(u"coin_selete_2")
        self.coin_selete_2.setGeometry(QRect(170, 10, 151, 22))
        self.coin_selete_3 = QComboBox(self.buy_sell)
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.setObjectName(u"coin_selete_3")
        self.coin_selete_3.setGeometry(QRect(330, 10, 151, 22))
        self.label_3 = QLabel(self.buy_sell)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 40, 221, 21))
        self.label_6 = QLabel(self.buy_sell)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(250, 40, 231, 21))
        self.graph = QFrame(self.tab)
        self.graph.setObjectName(u"graph")
        self.graph.setGeometry(QRect(0, 750, 1401, 261))
        self.graph.setFrameShape(QFrame.StyledPanel)
        self.graph.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(1410, 9, 491, 131))
        font = QFont()
        font.setFamily(u"HY\uacac\uace0\ub515")
        font.setPointSize(95)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.scrollArea = QScrollArea(self.tab_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(0, 0, 1911, 1031))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1909, 1029))
        self.strategy_combo = QComboBox(self.scrollAreaWidgetContents)
        self.strategy_combo.addItem("")
        self.strategy_combo.addItem("")
        self.strategy_combo.addItem("")
        self.strategy_combo.addItem("")
        self.strategy_combo.setObjectName(u"strategy_combo")
        self.strategy_combo.setGeometry(QRect(10, 10, 211, 22))
        self.start_button = QPushButton(self.scrollAreaWidgetContents)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setGeometry(QRect(1640, 10, 75, 23))
        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(0, 40, 1311, 971))
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_2 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(1810, 10, 75, 23))
        self.stop_button = QPushButton(self.scrollAreaWidgetContents)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setGeometry(QRect(1720, 10, 81, 23))
        self.strategy_combo_2 = QComboBox(self.scrollAreaWidgetContents)
        self.strategy_combo_2.setObjectName(u"strategy_combo_2")
        self.strategy_combo_2.setGeometry(QRect(230, 10, 151, 20))
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(1320, 210, 581, 801))
        self.history = QListWidget(self.groupBox)
        self.history.setObjectName(u"history")
        self.history.setGeometry(QRect(10, 20, 561, 771))
        self.pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(1320, 50, 581, 151))
        self.pushButton.setStyleSheet(u"QPushButton{\n"
"	font: 14pt \"Franklin Gothic Medium\";\n"
"	background-color: rgb(212, 212, 212);\n"
"	border: none;\n"
"	boder-radius: 20px;\n"
"	\n"
"	color: rgb(255, 70, 73);\n"
"\n"
"	border-left: 1px solid rgb(230,230,230);\n"
"	border-right: 1px solid rgb(230,230,230);\n"
"	border-bottom: 3px solid rgb(230,230,230);\n"
"	border-top: 3px solid rgb(230,230,230);\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgb(222, 222, 222);\n"
"	border-left: rgb(230,230,230);\n"
"	border-right: rgb(230,230,230);\n"
"	border-bottom: rgb(230,230,230);\n"
"\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgb(180, 180, 180);\n"
"	border-left: rgb(230,230,230);\n"
"	border-right: rgb(230,230,230);\n"
"	border-bottom: rgb(230,230,230);\n"
"\n"
"}")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.chart.setTitle("")
        self.charTab1.setTitle("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"access_key", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.api_select.setItemText(0, QCoreApplication.translate("MainWindow", u"Upbit", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"secret_key", None))
        self.buy_sell.setTitle("")
        self.buy_button.setText(QCoreApplication.translate("MainWindow", u"\ub9e4\uc218", None))
        self.persent_10.setText(QCoreApplication.translate("MainWindow", u"10%", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\uc9c1\uc811\uc785\ub825", None))
        self.buy_button_2.setText(QCoreApplication.translate("MainWindow", u"\ub9e4\ub3c4", None))
        self.persent_50.setText(QCoreApplication.translate("MainWindow", u"50%", None))
        self.persent_max.setText(QCoreApplication.translate("MainWindow", u"\ucd5c\ub300", None))
        self.groupBox_4.setTitle("")
        self.persent_75.setText(QCoreApplication.translate("MainWindow", u"75%", None))
        self.persent_25.setText(QCoreApplication.translate("MainWindow", u"25%", None))
        self.coin_selete_2.setItemText(0, QCoreApplication.translate("MainWindow", u"1\ubd84", None))
        self.coin_selete_2.setItemText(1, QCoreApplication.translate("MainWindow", u"5\ubd84", None))
        self.coin_selete_2.setItemText(2, QCoreApplication.translate("MainWindow", u"15\ubd84", None))
        self.coin_selete_2.setItemText(3, QCoreApplication.translate("MainWindow", u"30\ubd84", None))
        self.coin_selete_2.setItemText(4, QCoreApplication.translate("MainWindow", u"1\uc2dc\uac04", None))

        self.coin_selete_3.setItemText(0, QCoreApplication.translate("MainWindow", u"50", None))
        self.coin_selete_3.setItemText(1, QCoreApplication.translate("MainWindow", u"100", None))
        self.coin_selete_3.setItemText(2, QCoreApplication.translate("MainWindow", u"150", None))
        self.coin_selete_3.setItemText(3, QCoreApplication.translate("MainWindow", u"200", None))
        self.coin_selete_3.setItemText(4, QCoreApplication.translate("MainWindow", u"300", None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac \ubcf4\uc720\ub7c9 : 0.0", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"KRW : 0.0", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"COB2N", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\ucc28\ud2b8", None))
        self.strategy_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"\uae30\ubcf8\uc804\ub7b5", None))
        self.strategy_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"Custom 1", None))
        self.strategy_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"Custom 2", None))
        self.strategy_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"Custom 3", None))

        self.start_button.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\ud589", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\uc2e4\ud589 \ubc15\uc2a4", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\ub3c4\uc6c0\ub9d0", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"\uc911\uc9c0", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\uae30\ub85d", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\ube14\ub85d \ucd94\uac00 +", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\uc2e4\ud589", None))
    # retranslateUi

