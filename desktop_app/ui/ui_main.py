# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainrPSCCg.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGroupBox, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1918, 1036)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowTitle(u"CoB2n")
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget{\n"
"	background-color: #2E3440;\n"
"}")
        self.windowbar = QWidget(self.centralwidget)
        self.windowbar.setObjectName(u"windowbar")
        self.windowbar.setGeometry(QRect(100, 0, 1821, 21))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1911, 1031))
        self.tabWidget.setStyleSheet(u"/* QTabWidget \ubc30\uacbd */\n"
"QTabWidget::pane {\n"
"    background-color: #2E3440; /* \uc804\uccb4 \ubc30\uacbd */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"/* \ud0ed \ubc14 \uc2a4\ud0c0\uc77c */\n"
"QTabBar::tab {\n"
"    background-color: #4C566A; /* \uae30\ubcf8 \ud0ed \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae30\ubcf8 \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    padding: 8px 16px;\n"
"    border-top-left-radius: 6px;\n"
"    border-top-right-radius: 6px;\n"
"    border: 2px solid #4C566A;\n"
"    margin-right: 2px;\n"
"}\n"
"\n"
"/* \uc120\ud0dd\ub41c \ud0ed */\n"
"QTabBar::tab:selected {\n"
"    background-color: #81A1C1; /* \uc120\ud0dd\ub41c \ud0ed \ubc30\uacbd */\n"
"    color: white;\n"
"    border: 2px solid #88C0D0;\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QTabBar::tab:hover {\n"
"    background-color: #5E81AC;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ud0ed */\n"
"QTabBar::tab:!selected {\n"
"    bac"
                        "kground-color: #4C566A;\n"
"    color: #D8DEE9;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ud0ed + \ub9c8\uc6b0\uc2a4 \ud638\ubc84 */\n"
"QTabBar::tab:!selected:hover {\n"
"    background-color: #5E81AC;\n"
"}\n"
"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"")
        self.chart = QGroupBox(self.tab)
        self.chart.setObjectName(u"chart")
        self.chart.setGeometry(QRect(0, 50, 1401, 661))
        self.chart.setStyleSheet(u"/* \uae30\ubcf8 QGroupBox \uc2a4\ud0c0\uc77c */\n"
"QGroupBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"}\n"
"\n"
"/* \uadf8\ub8f9\ubc15\uc2a4 \uc81c\ubaa9 \uc2a4\ud0c0\uc77c */\n"
"QGroupBox::title {\n"
"    color: #D8DEE9; /* \uc81c\ubaa9 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* \uc81c\ubaa9 \uc704\uce58 */\n"
"    padding: 2px 10px;\n"
"    background-color: transparent; /* \uc81c\ubaa9 \ubc30\uacbd \ud22c\uba85 */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QGroupBox:hover {\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"")
        self.charTab1 = QGroupBox(self.tab)
        self.charTab1.setObjectName(u"charTab1")
        self.charTab1.setGeometry(QRect(0, 0, 1401, 41))
        self.charTab1.setStyleSheet(u"/* \uae30\ubcf8 QGroupBox \uc2a4\ud0c0\uc77c */\n"
"QGroupBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"}\n"
"\n"
"/* \uadf8\ub8f9\ubc15\uc2a4 \uc81c\ubaa9 \uc2a4\ud0c0\uc77c */\n"
"QGroupBox::title {\n"
"    color: #D8DEE9; /* \uc81c\ubaa9 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* \uc81c\ubaa9 \uc704\uce58 */\n"
"    padding: 2px 10px;\n"
"    background-color: transparent; /* \uc81c\ubaa9 \ubc30\uacbd \ud22c\uba85 */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QGroupBox:hover {\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"")
        self.label_2 = QLabel(self.charTab1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 14, 71, 16))
        self.label_2.setStyleSheet(u"QLabel {\n"
"    background-color: transparent; /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"/* \uac15\uc870 \uc2a4\ud0c0\uc77c */\n"
"QLabel[highlight=\"true\"] {\n"
"    color: #81A1C1; /* \uac15\uc870\ub41c \uae00\uc790\uc0c9 */\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.access_key = QLineEdit(self.charTab1)
        self.access_key.setObjectName(u"access_key")
        self.access_key.setGeometry(QRect(90, 10, 191, 21))
        self.access_key.setStyleSheet(u"QLineEdit {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \uae30\ubcf8 \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"    selection-background-color: #5E81AC; /* \uc120\ud0dd \uc601\uc5ed \ubc30\uacbd\uc0c9 */\n"
"    selection-color: white; /* \uc120\ud0dd\ub41c \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"}\n"
"\n"
"/* \ud3ec\ucee4\uc2a4 \ub418\uc5c8\uc744 \ub54c */\n"
"QLineEdit:focus {\n"
"    border: 2px solid #81A1C1; /* \ud65c\uc131\ud654\ub41c \uc0c1\ud0dc\uc5d0\uc11c\uc758 \ud14c\ub450\ub9ac */\n"
"    background-color: #3B4252;\n"
"}\n"
"")
        self.save_button = QPushButton(self.charTab1)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setGeometry(QRect(690, 10, 41, 21))
        self.save_button.setStyleSheet(u"/* \uae30\ubcf8 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: #4C566A; /* \ubc84\ud2bc \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae00\uc790 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 2px solid #4C566A;\n"
"    border-radius: 8px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QPushButton:hover {\n"
"    background-color: #5E81AC;\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \ud074\ub9ad (Pressed) \uc0c1\ud0dc */\n"
"QPushButton:pressed {\n"
"    background-color: #81A1C1;\n"
"    border: 2px solid #88C0D0;\n"
"    color: white;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ubc84\ud2bc */\n"
"QPushButton:disabled {\n"
"    background-color: #3B4252;\n"
"    color: #7E8A9A;\n"
"    border: 2px solid #3B4252;\n"
"}\n"
"")
        self.api_select = QComboBox(self.charTab1)
        self.api_select.addItem("")
        self.api_select.setObjectName(u"api_select")
        self.api_select.setGeometry(QRect(580, 10, 101, 22))
        self.api_select.setStyleSheet(u"QComboBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"    padding: 0px 10px;\n"
"    selection-background-color: #5E81AC; /* \uc120\ud0dd\ud55c \ud56d\ubaa9 \ubc30\uacbd */\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 25px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc544\uc774\ucf58 */\n"
"QComboBox::down-arrow {\n"
"    image: url(down-arrow.png); /* \uc6d0\ud558\ub294 \ud654\uc0b4\ud45c \uc774\ubbf8\uc9c0\ub85c \ubcc0\uacbd \uac00\ub2a5 */\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \ud638\ubc84 \ud6a8\uacfc */\n"
"QComboBox::drop-down:hover {\n"
"    background-color: #434C5E;\n"
"}\n"
"\n"
"/* \ub9ac\uc2a4\ud2b8"
                        " \ud31d\uc5c5 \uc2a4\ud0c0\uc77c */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #3B4252;\n"
"    border: 1px solid #4C566A;\n"
"    selection-background-color: #81A1C1;\n"
"    selection-color: white;\n"
"    color: #ECEFF4;\n"
"    outline: 0;\n"
"}\n"
"")
        self.secret_key = QLineEdit(self.charTab1)
        self.secret_key.setObjectName(u"secret_key")
        self.secret_key.setGeometry(QRect(380, 10, 191, 21))
        self.secret_key.setStyleSheet(u"QLineEdit {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \uae30\ubcf8 \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"    selection-background-color: #5E81AC; /* \uc120\ud0dd \uc601\uc5ed \ubc30\uacbd\uc0c9 */\n"
"    selection-color: white; /* \uc120\ud0dd\ub41c \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"}\n"
"\n"
"/* \ud3ec\ucee4\uc2a4 \ub418\uc5c8\uc744 \ub54c */\n"
"QLineEdit:focus {\n"
"    border: 2px solid #81A1C1; /* \ud65c\uc131\ud654\ub41c \uc0c1\ud0dc\uc5d0\uc11c\uc758 \ud14c\ub450\ub9ac */\n"
"    background-color: #3B4252;\n"
"}\n"
"")
        self.label_4 = QLabel(self.charTab1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(300, 14, 71, 16))
        self.label_4.setStyleSheet(u"QLabel {\n"
"    background-color: transparent; /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"/* \uac15\uc870 \uc2a4\ud0c0\uc77c */\n"
"QLabel[highlight=\"true\"] {\n"
"    color: #81A1C1; /* \uac15\uc870\ub41c \uae00\uc790\uc0c9 */\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.buy_sell = QGroupBox(self.tab)
        self.buy_sell.setObjectName(u"buy_sell")
        self.buy_sell.setGeometry(QRect(1410, 150, 491, 831))
        self.buy_sell.setStyleSheet(u"/* \uae30\ubcf8 QGroupBox \uc2a4\ud0c0\uc77c */\n"
"QGroupBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"}\n"
"\n"
"/* \uadf8\ub8f9\ubc15\uc2a4 \uc81c\ubaa9 \uc2a4\ud0c0\uc77c */\n"
"QGroupBox::title {\n"
"    color: #D8DEE9; /* \uc81c\ubaa9 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* \uc81c\ubaa9 \uc704\uce58 */\n"
"    padding: 2px 10px;\n"
"    background-color: transparent; /* \uc81c\ubaa9 \ubc30\uacbd \ud22c\uba85 */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QGroupBox:hover {\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"")
        self.coin_selete = QComboBox(self.buy_sell)
        self.coin_selete.setObjectName(u"coin_selete")
        self.coin_selete.setGeometry(QRect(10, 10, 151, 22))
        self.coin_selete.setStyleSheet(u"QComboBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"    padding: 0px 10px;\n"
"    selection-background-color: #5E81AC; /* \uc120\ud0dd\ud55c \ud56d\ubaa9 \ubc30\uacbd */\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 25px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc544\uc774\ucf58 */\n"
"QComboBox::down-arrow {\n"
"    image: url(down-arrow.png); /* \uc6d0\ud558\ub294 \ud654\uc0b4\ud45c \uc774\ubbf8\uc9c0\ub85c \ubcc0\uacbd \uac00\ub2a5 */\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \ud638\ubc84 \ud6a8\uacfc */\n"
"QComboBox::drop-down:hover {\n"
"    background-color: #434C5E;\n"
"}\n"
"\n"
"/* \ub9ac\uc2a4\ud2b8"
                        " \ud31d\uc5c5 \uc2a4\ud0c0\uc77c */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #3B4252;\n"
"    border: 1px solid #4C566A;\n"
"    selection-background-color: #81A1C1;\n"
"    selection-color: white;\n"
"    color: #ECEFF4;\n"
"    outline: 0;\n"
"}\n"
"")
        self.buy_button = QPushButton(self.buy_sell)
        self.buy_button.setObjectName(u"buy_button")
        self.buy_button.setGeometry(QRect(320, 800, 75, 23))
        self.buy_button.setStyleSheet(u"/* \uae30\ubcf8 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: #4C566A; /* \ubc84\ud2bc \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae00\uc790 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 2px solid #4C566A;\n"
"    border-radius: 8px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QPushButton:hover {\n"
"    background-color: #5E81AC;\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \ud074\ub9ad (Pressed) \uc0c1\ud0dc */\n"
"QPushButton:pressed {\n"
"    background-color: #81A1C1;\n"
"    border: 2px solid #88C0D0;\n"
"    color: white;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ubc84\ud2bc */\n"
"QPushButton:disabled {\n"
"    background-color: #3B4252;\n"
"    color: #7E8A9A;\n"
"    border: 2px solid #3B4252;\n"
"}\n"
"")
        self.label_5 = QLabel(self.buy_sell)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(260, 780, 61, 16))
        self.label_5.setStyleSheet(u"QLabel {\n"
"    background-color: transparent; /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"/* \uac15\uc870 \uc2a4\ud0c0\uc77c */\n"
"QLabel[highlight=\"true\"] {\n"
"    color: #81A1C1; /* \uac15\uc870\ub41c \uae00\uc790\uc0c9 */\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.direct_input_2 = QLineEdit(self.buy_sell)
        self.direct_input_2.setObjectName(u"direct_input_2")
        self.direct_input_2.setGeometry(QRect(320, 776, 161, 20))
        self.direct_input_2.setStyleSheet(u"QLineEdit {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \uae30\ubcf8 \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"    padding: 0px 10px;\n"
"    selection-background-color: #5E81AC; /* \uc120\ud0dd \uc601\uc5ed \ubc30\uacbd\uc0c9 */\n"
"    selection-color: white; /* \uc120\ud0dd\ub41c \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"}\n"
"\n"
"/* \ud3ec\ucee4\uc2a4 \ub418\uc5c8\uc744 \ub54c */\n"
"QLineEdit:focus {\n"
"    border: 2px solid #81A1C1; /* \ud65c\uc131\ud654\ub41c \uc0c1\ud0dc\uc5d0\uc11c\uc758 \ud14c\ub450\ub9ac */\n"
"    background-color: #3B4252;\n"
"}\n"
"")
        self.buy_button_2 = QPushButton(self.buy_sell)
        self.buy_button_2.setObjectName(u"buy_button_2")
        self.buy_button_2.setGeometry(QRect(410, 800, 75, 23))
        self.buy_button_2.setStyleSheet(u"/* \uae30\ubcf8 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: #4C566A; /* \ubc84\ud2bc \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae00\uc790 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 2px solid #4C566A;\n"
"    border-radius: 8px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QPushButton:hover {\n"
"    background-color: #5E81AC;\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \ud074\ub9ad (Pressed) \uc0c1\ud0dc */\n"
"QPushButton:pressed {\n"
"    background-color: #81A1C1;\n"
"    border: 2px solid #88C0D0;\n"
"    color: white;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ubc84\ud2bc */\n"
"QPushButton:disabled {\n"
"    background-color: #3B4252;\n"
"    color: #7E8A9A;\n"
"    border: 2px solid #3B4252;\n"
"}\n"
"")
        self.persent_50 = QCheckBox(self.buy_sell)
        self.persent_50.setObjectName(u"persent_50")
        self.persent_50.setGeometry(QRect(10, 780, 61, 16))
        self.persent_50.setStyleSheet(u"QCheckBox {\n"
"    color: #D8DEE9; /* \uae30\ubcf8 \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    spacing: 8px; /* \uccb4\ud06c\ubc15\uc2a4\uc640 \ud14d\uc2a4\ud2b8 \uac04\uaca9 */\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ubc15\uc2a4 \uae30\ubcf8 \uc2a4\ud0c0\uc77c */\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 4px;\n"
"    border: 2px solid #4C566A;\n"
"    background-color: #2E3440;\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ubc15\uc2a4 \uccb4\ud06c\ub410\uc744 \ub54c */\n"
"QCheckBox::indicator:checked {\n"
"    background-color: rgb(114, 255, 82); /* \uccb4\ud06c\ub41c \uc0c1\ud0dc \ubc30\uacbd\uc0c9 */\n"
"    border: 2px solid #88C0D0;\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \uc62c\ub838\uc744 \ub54c */\n"
"QCheckBox::indicator:hover {\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ub410\uace0 \ub9c8\uc6b0\uc2a4 \uc62c\ub838\uc744 \ub54c */\n"
"QCheckBox::indicator:checked:hover {\n"
"    background-color: #88C0D0;\n"
"}\n"
"")
        self.persent_max = QCheckBox(self.buy_sell)
        self.persent_max.setObjectName(u"persent_max")
        self.persent_max.setGeometry(QRect(190, 780, 61, 16))
        self.persent_max.setStyleSheet(u"QCheckBox {\n"
"    color: #D8DEE9; /* \uae30\ubcf8 \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    spacing: 8px; /* \uccb4\ud06c\ubc15\uc2a4\uc640 \ud14d\uc2a4\ud2b8 \uac04\uaca9 */\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ubc15\uc2a4 \uae30\ubcf8 \uc2a4\ud0c0\uc77c */\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 4px;\n"
"    border: 2px solid #4C566A;\n"
"    background-color: #2E3440;\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ubc15\uc2a4 \uccb4\ud06c\ub410\uc744 \ub54c */\n"
"QCheckBox::indicator:checked {\n"
"    background-color: rgb(114, 255, 82); /* \uccb4\ud06c\ub41c \uc0c1\ud0dc \ubc30\uacbd\uc0c9 */\n"
"    border: 2px solid #88C0D0;\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \uc62c\ub838\uc744 \ub54c */\n"
"QCheckBox::indicator:hover {\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ub410\uace0 \ub9c8\uc6b0\uc2a4 \uc62c\ub838\uc744 \ub54c */\n"
"QCheckBox::indicator:checked:hover {\n"
"    background-color: #88C0D0;\n"
"}\n"
"")
        self.groupBox_4 = QGroupBox(self.buy_sell)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 70, 471, 691))
        self.groupBox_4.setStyleSheet(u"")
        self.persent_75 = QCheckBox(self.buy_sell)
        self.persent_75.setObjectName(u"persent_75")
        self.persent_75.setGeometry(QRect(70, 780, 61, 16))
        self.persent_75.setStyleSheet(u"QCheckBox {\n"
"    color: #D8DEE9; /* \uae30\ubcf8 \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    spacing: 8px; /* \uccb4\ud06c\ubc15\uc2a4\uc640 \ud14d\uc2a4\ud2b8 \uac04\uaca9 */\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ubc15\uc2a4 \uae30\ubcf8 \uc2a4\ud0c0\uc77c */\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 4px;\n"
"    border: 2px solid #4C566A;\n"
"    background-color: #2E3440;\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ubc15\uc2a4 \uccb4\ud06c\ub410\uc744 \ub54c */\n"
"QCheckBox::indicator:checked {\n"
"    background-color: rgb(114, 255, 82); /* \uccb4\ud06c\ub41c \uc0c1\ud0dc \ubc30\uacbd\uc0c9 */\n"
"    border: 2px solid #88C0D0;\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \uc62c\ub838\uc744 \ub54c */\n"
"QCheckBox::indicator:hover {\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ub410\uace0 \ub9c8\uc6b0\uc2a4 \uc62c\ub838\uc744 \ub54c */\n"
"QCheckBox::indicator:checked:hover {\n"
"    background-color: #88C0D0;\n"
"}\n"
"")
        self.coin_selete_2 = QComboBox(self.buy_sell)
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.setObjectName(u"coin_selete_2")
        self.coin_selete_2.setGeometry(QRect(170, 10, 151, 22))
        self.coin_selete_2.setStyleSheet(u"QComboBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"    padding: 0px 10px;\n"
"    selection-background-color: #5E81AC; /* \uc120\ud0dd\ud55c \ud56d\ubaa9 \ubc30\uacbd */\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 25px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc544\uc774\ucf58 */\n"
"QComboBox::down-arrow {\n"
"    image: url(down-arrow.png); /* \uc6d0\ud558\ub294 \ud654\uc0b4\ud45c \uc774\ubbf8\uc9c0\ub85c \ubcc0\uacbd \uac00\ub2a5 */\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \ud638\ubc84 \ud6a8\uacfc */\n"
"QComboBox::drop-down:hover {\n"
"    background-color: #434C5E;\n"
"}\n"
"\n"
"/* \ub9ac\uc2a4\ud2b8"
                        " \ud31d\uc5c5 \uc2a4\ud0c0\uc77c */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #3B4252;\n"
"    border: 1px solid #4C566A;\n"
"    selection-background-color: #81A1C1;\n"
"    selection-color: white;\n"
"    color: #ECEFF4;\n"
"    outline: 0;\n"
"}\n"
"")
        self.coin_selete_3 = QComboBox(self.buy_sell)
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.setObjectName(u"coin_selete_3")
        self.coin_selete_3.setGeometry(QRect(330, 10, 151, 22))
        self.coin_selete_3.setStyleSheet(u"QComboBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"    padding: 0px 10px;\n"
"    selection-background-color: #5E81AC; /* \uc120\ud0dd\ud55c \ud56d\ubaa9 \ubc30\uacbd */\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 25px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc544\uc774\ucf58 */\n"
"QComboBox::down-arrow {\n"
"    image: url(down-arrow.png); /* \uc6d0\ud558\ub294 \ud654\uc0b4\ud45c \uc774\ubbf8\uc9c0\ub85c \ubcc0\uacbd \uac00\ub2a5 */\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \ud638\ubc84 \ud6a8\uacfc */\n"
"QComboBox::drop-down:hover {\n"
"    background-color: #434C5E;\n"
"}\n"
"\n"
"/* \ub9ac\uc2a4\ud2b8"
                        " \ud31d\uc5c5 \uc2a4\ud0c0\uc77c */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #3B4252;\n"
"    border: 1px solid #4C566A;\n"
"    selection-background-color: #81A1C1;\n"
"    selection-color: white;\n"
"    color: #ECEFF4;\n"
"    outline: 0;\n"
"}\n"
"")
        self.label_3 = QLabel(self.buy_sell)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 40, 221, 21))
        self.label_3.setStyleSheet(u"QLabel {\n"
"    background-color: transparent; /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"/* \uac15\uc870 \uc2a4\ud0c0\uc77c */\n"
"QLabel[highlight=\"true\"] {\n"
"    color: #81A1C1; /* \uac15\uc870\ub41c \uae00\uc790\uc0c9 */\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.label_6 = QLabel(self.buy_sell)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(250, 40, 231, 21))
        self.label_6.setStyleSheet(u"QLabel {\n"
"    background-color: transparent; /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"/* \uac15\uc870 \uc2a4\ud0c0\uc77c */\n"
"QLabel[highlight=\"true\"] {\n"
"    color: #81A1C1; /* \uac15\uc870\ub41c \uae00\uc790\uc0c9 */\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.persent_76 = QCheckBox(self.buy_sell)
        self.persent_76.setObjectName(u"persent_76")
        self.persent_76.setGeometry(QRect(130, 780, 61, 16))
        self.persent_76.setStyleSheet(u"QCheckBox {\n"
"    color: #D8DEE9; /* \uae30\ubcf8 \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    spacing: 8px; /* \uccb4\ud06c\ubc15\uc2a4\uc640 \ud14d\uc2a4\ud2b8 \uac04\uaca9 */\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ubc15\uc2a4 \uae30\ubcf8 \uc2a4\ud0c0\uc77c */\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 4px;\n"
"    border: 2px solid #4C566A;\n"
"    background-color: #2E3440;\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ubc15\uc2a4 \uccb4\ud06c\ub410\uc744 \ub54c */\n"
"QCheckBox::indicator:checked {\n"
"    background-color: rgb(114, 255, 82); /* \uccb4\ud06c\ub41c \uc0c1\ud0dc \ubc30\uacbd\uc0c9 */\n"
"    border: 2px solid #88C0D0;\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \uc62c\ub838\uc744 \ub54c */\n"
"QCheckBox::indicator:hover {\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \uccb4\ud06c\ub410\uace0 \ub9c8\uc6b0\uc2a4 \uc62c\ub838\uc744 \ub54c */\n"
"QCheckBox::indicator:checked:hover {\n"
"    background-color: #88C0D0;\n"
"}\n"
"")
        self.graph = QFrame(self.tab)
        self.graph.setObjectName(u"graph")
        self.graph.setGeometry(QRect(0, 720, 1401, 261))
        self.graph.setStyleSheet(u"/* QFrame \uae30\ubcf8 \uc2a4\ud0c0\uc77c */\n"
"QFrame {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4); /* \uadf8\ub9bc\uc790 \ud6a8\uacfc */\n"
"}\n"
"")
        self.graph.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(1410, 9, 491, 131))
        font = QFont()
        font.setFamilies([u"HY\uacac\uace0\ub515"])
        font.setPointSize(95)
        self.label.setFont(font)
        self.label.setStyleSheet(u"QLabel{\n"
"	color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.strategy_combo.setStyleSheet(u"QComboBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"    padding: 0px 10px;\n"
"    selection-background-color: #5E81AC; /* \uc120\ud0dd\ud55c \ud56d\ubaa9 \ubc30\uacbd */\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 25px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc544\uc774\ucf58 */\n"
"QComboBox::down-arrow {\n"
"    image: url(down-arrow.png); /* \uc6d0\ud558\ub294 \ud654\uc0b4\ud45c \uc774\ubbf8\uc9c0\ub85c \ubcc0\uacbd \uac00\ub2a5 */\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \ud638\ubc84 \ud6a8\uacfc */\n"
"QComboBox::drop-down:hover {\n"
"    background-color: #434C5E;\n"
"}\n"
"\n"
"/* \ub9ac\uc2a4\ud2b8"
                        " \ud31d\uc5c5 \uc2a4\ud0c0\uc77c */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #3B4252;\n"
"    border: 1px solid #4C566A;\n"
"    selection-background-color: #81A1C1;\n"
"    selection-color: white;\n"
"    color: #ECEFF4;\n"
"    outline: 0;\n"
"}\n"
"")
        self.start_button = QPushButton(self.scrollAreaWidgetContents)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setGeometry(QRect(1640, 10, 75, 23))
        self.start_button.setStyleSheet(u"/* \uae30\ubcf8 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: #4C566A; /* \ubc84\ud2bc \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae00\uc790 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 2px solid #4C566A;\n"
"    border-radius: 8px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QPushButton:hover {\n"
"    background-color: #5E81AC;\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \ud074\ub9ad (Pressed) \uc0c1\ud0dc */\n"
"QPushButton:pressed {\n"
"    background-color: #81A1C1;\n"
"    border: 2px solid #88C0D0;\n"
"    color: white;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ubc84\ud2bc */\n"
"QPushButton:disabled {\n"
"    background-color: #3B4252;\n"
"    color: #7E8A9A;\n"
"    border: 2px solid #3B4252;\n"
"}\n"
"")
        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(0, 40, 1311, 941))
        self.groupBox_2.setStyleSheet(u"/* \uae30\ubcf8 QGroupBox \uc2a4\ud0c0\uc77c */\n"
"QGroupBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"    margin-top: 12px; /* \uc81c\ubaa9\uacfc \uadf8\ub8f9 \ubc15\uc2a4 \uac04 \uac04\uaca9 */\n"
"    padding: 10px;\n"
"}\n"
"\n"
"/* \uadf8\ub8f9\ubc15\uc2a4 \uc81c\ubaa9 \uc2a4\ud0c0\uc77c */\n"
"QGroupBox::title {\n"
"    color: #D8DEE9; /* \uc81c\ubaa9 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* \uc81c\ubaa9 \uc704\uce58 */\n"
"    padding: 2px 10px;\n"
"    background-color: #2E3440; /* \uc81c\ubaa9 \ubc30\uacbd \ud22c\uba85 */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QGroupBox:hover {\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_2 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(1810, 10, 75, 23))
        self.pushButton_2.setStyleSheet(u"/* \uae30\ubcf8 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: #4C566A; /* \ubc84\ud2bc \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae00\uc790 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 2px solid #4C566A;\n"
"    border-radius: 8px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QPushButton:hover {\n"
"    background-color: #5E81AC;\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \ud074\ub9ad (Pressed) \uc0c1\ud0dc */\n"
"QPushButton:pressed {\n"
"    background-color: #81A1C1;\n"
"    border: 2px solid #88C0D0;\n"
"    color: white;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ubc84\ud2bc */\n"
"QPushButton:disabled {\n"
"    background-color: #3B4252;\n"
"    color: #7E8A9A;\n"
"    border: 2px solid #3B4252;\n"
"}\n"
"")
        self.stop_button = QPushButton(self.scrollAreaWidgetContents)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setGeometry(QRect(1720, 10, 81, 23))
        self.stop_button.setStyleSheet(u"/* \uae30\ubcf8 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: #4C566A; /* \ubc84\ud2bc \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae00\uc790 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 2px solid #4C566A;\n"
"    border-radius: 8px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QPushButton:hover {\n"
"    background-color: #5E81AC;\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \ud074\ub9ad (Pressed) \uc0c1\ud0dc */\n"
"QPushButton:pressed {\n"
"    background-color: #81A1C1;\n"
"    border: 2px solid #88C0D0;\n"
"    color: white;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ubc84\ud2bc */\n"
"QPushButton:disabled {\n"
"    background-color: #3B4252;\n"
"    color: #7E8A9A;\n"
"    border: 2px solid #3B4252;\n"
"}\n"
"")
        self.strategy_combo_2 = QComboBox(self.scrollAreaWidgetContents)
        self.strategy_combo_2.setObjectName(u"strategy_combo_2")
        self.strategy_combo_2.setGeometry(QRect(1480, 10, 151, 21))
        self.strategy_combo_2.setStyleSheet(u"QComboBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    color: #D8DEE9; /* \uae00\uc790\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"    padding: 0px 10px;\n"
"    selection-background-color: #5E81AC; /* \uc120\ud0dd\ud55c \ud56d\ubaa9 \ubc30\uacbd */\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 25px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc544\uc774\ucf58 */\n"
"QComboBox::down-arrow {\n"
"    image: url(down-arrow.png); /* \uc6d0\ud558\ub294 \ud654\uc0b4\ud45c \uc774\ubbf8\uc9c0\ub85c \ubcc0\uacbd \uac00\ub2a5 */\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"/* \ub4dc\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \ud638\ubc84 \ud6a8\uacfc */\n"
"QComboBox::drop-down:hover {\n"
"    background-color: #434C5E;\n"
"}\n"
"\n"
"/* \ub9ac\uc2a4\ud2b8"
                        " \ud31d\uc5c5 \uc2a4\ud0c0\uc77c */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #3B4252;\n"
"    border: 1px solid #4C566A;\n"
"    selection-background-color: #81A1C1;\n"
"    selection-color: white;\n"
"    color: #ECEFF4;\n"
"    outline: 0;\n"
"}\n"
"")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(1320, 210, 581, 771))
        self.groupBox.setStyleSheet(u"/* \uae30\ubcf8 QGroupBox \uc2a4\ud0c0\uc77c */\n"
"QGroupBox {\n"
"    background-color: #2E3440; /* \ubc30\uacbd\uc0c9 */\n"
"    border: 2px solid #4C566A; /* \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px; /* \ubaa8\uc11c\ub9ac \ub465\uae00\uac8c */\n"
"}\n"
"\n"
"/* \uadf8\ub8f9\ubc15\uc2a4 \uc81c\ubaa9 \uc2a4\ud0c0\uc77c */\n"
"QGroupBox::title {\n"
"    color: #D8DEE9; /* \uc81c\ubaa9 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* \uc81c\ubaa9 \uc704\uce58 */\n"
"    padding: 2px 10px;\n"
"    background-color: transparent; /* \uc81c\ubaa9 \ubc30\uacbd \ud22c\uba85 */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QGroupBox:hover {\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"")
        self.history = QListWidget(self.groupBox)
        self.history.setObjectName(u"history")
        self.history.setGeometry(QRect(10, 20, 561, 741))
        self.history.setStyleSheet(u"/* QListWidget \uc804\uccb4 \ubc30\uacbd */\n"
"QListWidget {\n"
"    background-color: #2E3440; /* \ub9ac\uc2a4\ud2b8 \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae30\ubcf8 \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    border: 2px solid #4C566A;\n"
"    border-radius: 8px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"/* \ub9ac\uc2a4\ud2b8 \uc544\uc774\ud15c \uae30\ubcf8 \uc2a4\ud0c0\uc77c */\n"
"QListWidget::item {\n"
"    background-color: #3B4252; /* \uae30\ubcf8 \uc544\uc774\ud15c \ubc30\uacbd */\n"
"    padding: 8px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QListWidget::item:hover {\n"
"    background-color: #5E81AC;\n"
"}\n"
"\n"
"/* \uc120\ud0dd\ub41c \uc544\uc774\ud15c */\n"
"QListWidget::item:selected {\n"
"    background-color: #81A1C1;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* \uc120\ud0dd\ub41c \uc544\uc774\ud15c (\ube44\ud65c\uc131\ud654 \uc0c1\ud0dc) */\n"
"QListWidget::item:selected:!active {\n"
"    background-color: #4C566A;\n"
""
                        "    color: #D8DEE9;\n"
"}\n"
"")
        self.pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(1320, 50, 581, 151))
        self.pushButton.setStyleSheet(u"/* \uae30\ubcf8 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: #4C566A; /* \ubc84\ud2bc \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae00\uc790 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 2px solid #4C566A;\n"
"    border-radius: 8px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QPushButton:hover {\n"
"    background-color: #5E81AC;\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \ud074\ub9ad (Pressed) \uc0c1\ud0dc */\n"
"QPushButton:pressed {\n"
"    background-color: #81A1C1;\n"
"    border: 2px solid #88C0D0;\n"
"    color: white;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ubc84\ud2bc */\n"
"QPushButton:disabled {\n"
"    background-color: #3B4252;\n"
"    color: #7E8A9A;\n"
"    border: 2px solid #3B4252;\n"
"}\n"
"")
        self.start_button_2 = QPushButton(self.scrollAreaWidgetContents)
        self.start_button_2.setObjectName(u"start_button_2")
        self.start_button_2.setGeometry(QRect(230, 10, 75, 23))
        self.start_button_2.setStyleSheet(u"/* \uae30\ubcf8 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: #4C566A; /* \ubc84\ud2bc \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae00\uc790 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 2px solid #4C566A;\n"
"    border-radius: 8px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QPushButton:hover {\n"
"    background-color: #5E81AC;\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \ud074\ub9ad (Pressed) \uc0c1\ud0dc */\n"
"QPushButton:pressed {\n"
"    background-color: #81A1C1;\n"
"    border: 2px solid #88C0D0;\n"
"    color: white;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ubc84\ud2bc */\n"
"QPushButton:disabled {\n"
"    background-color: #3B4252;\n"
"    color: #7E8A9A;\n"
"    border: 2px solid #3B4252;\n"
"}\n"
"")
        self.clear_button = QPushButton(self.scrollAreaWidgetContents)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setGeometry(QRect(310, 10, 75, 23))
        self.clear_button.setStyleSheet(u"/* \uae30\ubcf8 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: #4C566A; /* \ubc84\ud2bc \ubc30\uacbd */\n"
"    color: #D8DEE9; /* \uae00\uc790 \uc0c9\uc0c1 */\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 2px solid #4C566A;\n"
"    border-radius: 8px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"}\n"
"\n"
"/* \ub9c8\uc6b0\uc2a4 \ud638\ubc84 \uc2dc */\n"
"QPushButton:hover {\n"
"    background-color: #5E81AC;\n"
"    border: 2px solid #81A1C1;\n"
"}\n"
"\n"
"/* \ud074\ub9ad (Pressed) \uc0c1\ud0dc */\n"
"QPushButton:pressed {\n"
"    background-color: #81A1C1;\n"
"    border: 2px solid #88C0D0;\n"
"    color: white;\n"
"}\n"
"\n"
"/* \ube44\ud65c\uc131\ud654\ub41c \ubc84\ud2bc */\n"
"QPushButton:disabled {\n"
"    background-color: #3B4252;\n"
"    color: #7E8A9A;\n"
"    border: 2px solid #3B4252;\n"
"}\n"
"")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
        
        # ✅ 종료 버튼 추가
        self.exit_button = QPushButton(self.centralwidget)
        self.exit_button.setObjectName(u"exit_button")
        self.exit_button.setGeometry(QRect(1880, 5, 30, 25))  # 오른쪽 상단에 위치
        self.exit_button.setStyleSheet("""
                QPushButton {
                color: white;  /* 글자 색상 */
                border: none;
                }
                QPushButton:hover {
                background-color: #D08770;  /* 호버 시 색상 */
                }
                QPushButton:pressed {
                background-color: #A54242;  /* 클릭 시 색상 */
                }
        """)
        self.exit_button.setText("X")
        self.exit_button.clicked.connect(QApplication.quit)  # 클릭 시 프로그램 종료
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
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\uc9c1\uc811\uc785\ub825", None))
        self.buy_button_2.setText(QCoreApplication.translate("MainWindow", u"\ub9e4\ub3c4", None))
        self.persent_50.setText(QCoreApplication.translate("MainWindow", u"25%", None))
        self.persent_max.setText(QCoreApplication.translate("MainWindow", u"\ucd5c\ub300", None))
        self.groupBox_4.setTitle("")
        self.persent_75.setText(QCoreApplication.translate("MainWindow", u"50%", None))
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
        self.persent_76.setText(QCoreApplication.translate("MainWindow", u"75%", None))
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
        self.start_button_2.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.clear_button.setText(QCoreApplication.translate("MainWindow", u"\ucd08\uae30\ud654", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\uc2e4\ud589", None))
        pass
    # retranslateUi

