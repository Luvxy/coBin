# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CoB2n appbDGqdG.ui'
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
from ui.ui_block import BlockMain


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
        self.coin_selete.addItem("")
        self.coin_selete.setObjectName(u"coin_selete")
        self.coin_selete.setGeometry(QRect(10, 10, 181, 22))
        self.groupBox = QGroupBox(self.buy_sell)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 40, 471, 241))
        self.checkBox_10 = QCheckBox(self.buy_sell)
        self.checkBox_10.setObjectName(u"checkBox_10")
        self.checkBox_10.setGeometry(QRect(10, 290, 51, 16))
        self.checkBox_25 = QCheckBox(self.buy_sell)
        self.checkBox_25.setObjectName(u"checkBox_25")
        self.checkBox_25.setGeometry(QRect(60, 290, 51, 16))
        self.checkBox_50 = QCheckBox(self.buy_sell)
        self.checkBox_50.setObjectName(u"checkBox_50")
        self.checkBox_50.setGeometry(QRect(110, 290, 51, 16))
        self.checkBox_75 = QCheckBox(self.buy_sell)
        self.checkBox_75.setObjectName(u"checkBox_75")
        self.checkBox_75.setGeometry(QRect(160, 290, 51, 16))
        self.checkBox_max = QCheckBox(self.buy_sell)
        self.checkBox_max.setObjectName(u"checkBox_max")
        self.checkBox_max.setGeometry(QRect(210, 290, 51, 16))
        self.label_3 = QLabel(self.buy_sell)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(260, 290, 61, 16))
        self.direct_input = QLineEdit(self.buy_sell)
        self.direct_input.setObjectName(u"direct_input")
        self.direct_input.setGeometry(QRect(320, 290, 161, 16))
        self.buy_button = QPushButton(self.buy_sell)
        self.buy_button.setObjectName(u"buy_button")
        self.buy_button.setGeometry(QRect(410, 310, 75, 23))
        self.checkBox_11 = QCheckBox(self.buy_sell)
        self.checkBox_11.setObjectName(u"checkBox_11")
        self.checkBox_11.setGeometry(QRect(10, 810, 51, 16))
        self.label_5 = QLabel(self.buy_sell)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(260, 810, 61, 16))
        self.direct_input_2 = QLineEdit(self.buy_sell)
        self.direct_input_2.setObjectName(u"direct_input_2")
        self.direct_input_2.setGeometry(QRect(320, 810, 161, 16))
        self.buy_button_2 = QPushButton(self.buy_sell)
        self.buy_button_2.setObjectName(u"buy_button_2")
        self.buy_button_2.setGeometry(QRect(410, 830, 75, 23))
        self.checkBox_51 = QCheckBox(self.buy_sell)
        self.checkBox_51.setObjectName(u"checkBox_51")
        self.checkBox_51.setGeometry(QRect(110, 810, 51, 16))
        self.checkBox_max_2 = QCheckBox(self.buy_sell)
        self.checkBox_max_2.setObjectName(u"checkBox_max_2")
        self.checkBox_max_2.setGeometry(QRect(210, 810, 51, 16))
        self.groupBox_4 = QGroupBox(self.buy_sell)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 380, 471, 421))
        self.checkBox_76 = QCheckBox(self.buy_sell)
        self.checkBox_76.setObjectName(u"checkBox_76")
        self.checkBox_76.setGeometry(QRect(160, 810, 51, 16))
        self.checkBox_26 = QCheckBox(self.buy_sell)
        self.checkBox_26.setObjectName(u"checkBox_26")
        self.checkBox_26.setGeometry(QRect(60, 810, 51, 16))
        self.label_6 = QLabel(self.buy_sell)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 360, 101, 16))
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
        self.pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(230, 10, 75, 23))
        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(0, 40, 1901, 971))
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.block_system_frame = BlockMain()
        self.verticalLayout.addWidget(self.block_system_frame)

        self.pushButton_2 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(1810, 10, 75, 23))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        # Close Button 추가
        self.close_button = QPushButton('X', MainWindow)
        self.close_button.setGeometry(1897, 5, 16, 16)  # 위치와 크기 조절
        self.close_button.setStyleSheet("""
            QPushButton {
                color: black;
                border: none;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: gray;
            }
        """)
        self.close_button.clicked.connect(QApplication.quit)
        
        
        QMetaObject.connectSlotsByName(MainWindow)
        
        # X 버튼
    # setupUi

    def retranslateUi(self, MainWindow):
        self.chart.setTitle("")
        self.charTab1.setTitle("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"access_key", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.api_select.setItemText(0, QCoreApplication.translate("MainWindow", u"Upbit", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"secret_key", None))
        self.buy_sell.setTitle("")
        self.coin_selete.setItemText(0, QCoreApplication.translate("MainWindow", u"\uc120\ud0dd", None))

        self.groupBox.setTitle("")
        self.checkBox_10.setText(QCoreApplication.translate("MainWindow", u"10%", None))
        self.checkBox_25.setText(QCoreApplication.translate("MainWindow", u"25%", None))
        self.checkBox_50.setText(QCoreApplication.translate("MainWindow", u"50%", None))
        self.checkBox_75.setText(QCoreApplication.translate("MainWindow", u"75%", None))
        self.checkBox_max.setText(QCoreApplication.translate("MainWindow", u"\ucd5c\ub300", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\uc9c1\uc811\uc785\ub825", None))
        self.buy_button.setText(QCoreApplication.translate("MainWindow", u"\ub9e4\uc218", None))
        self.checkBox_11.setText(QCoreApplication.translate("MainWindow", u"10%", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\uc9c1\uc811\uc785\ub825", None))
        self.buy_button_2.setText(QCoreApplication.translate("MainWindow", u"\ub9e4\ub3c4", None))
        self.checkBox_51.setText(QCoreApplication.translate("MainWindow", u"50%", None))
        self.checkBox_max_2.setText(QCoreApplication.translate("MainWindow", u"\ucd5c\ub300", None))
        self.groupBox_4.setTitle("")
        self.checkBox_76.setText(QCoreApplication.translate("MainWindow", u"75%", None))
        self.checkBox_26.setText(QCoreApplication.translate("MainWindow", u"25%", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac \ubcf4\uc720 \ud604\ud669", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"COB2N", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\ucc28\ud2b8", None))
        self.strategy_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"\uae30\ubcf8\uc804\ub7b5", None))
        self.strategy_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"Custom 1", None))
        self.strategy_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"Custom 2", None))
        self.strategy_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"Custom 3", None))

        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\ud589", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\uc2e4\ud589 \ubc15\uc2a4", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\ub3c4\uc6c0\ub9d0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\uc2e4\ud589", None))
    # retranslateUi

