# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainyiHBZT.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1915, 1036)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowTitle(u"CoB2n")
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                stop:0 rgba(30, 30, 40, 255), \n"
"                                stop:1 rgba(20, 20, 30, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    color: rgba(220, 220, 230, 230); /* \uc804\uccb4 \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"}")
        self.windowbar = QWidget(self.centralwidget)
        self.windowbar.setObjectName(u"windowbar")
        self.windowbar.setGeometry(QRect(100, 0, 1821, 21))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1911, 1031))
        self.tabWidget.setStyleSheet(u"QTabWidget::pane {\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \ud0ed \uc544\ub798 \ud328\ub110 \ud14c\ub450\ub9ac */\n"
"    background-color: rgba(40, 40, 50, 255); /* \ub2e4\ud06c \ud14c\ub9c8 \ubc30\uacbd */\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: rgba(50, 50, 60, 255); /* \uae30\ubcf8 \ud0ed \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180);\n"
"    border-top-left-radius: 6px;\n"
"    border-top-right-radius: 6px;\n"
"    padding: 8px 15px;\n"
"    margin-right: 2px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(200, 200, 210, 220); /* \uae30\ubcf8 \uae00\uc790\uc0c9 */\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background: rgba(70, 70, 80, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ubc30\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: rgba(100, 100, 120, 255); /* \uc120\ud0dd\ub41c \ud0ed \uac15\uc870 */\n"
"    border-bottom: 2px solid rgba(180, 180, 20"
                        "0, 255); /* \uc120\ud0dd\ub41c \ud0ed \ud558\uc774\ub77c\uc774\ud2b8 */\n"
"    color: rgba(255, 255, 255, 255);\n"
"}\n"
"\n"
"QTabBar::tab:selected:hover {\n"
"    background: rgba(120, 120, 140, 255); /* \uc120\ud0dd\ub41c \uc0c1\ud0dc\uc5d0\uc11c \ub9c8\uc6b0\uc2a4 \uc624\ubc84 */\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* \uc120\ud0dd\ub418\uc9c0 \uc54a\uc740 \ud0ed\uc744 \uc0b4\uc9dd \ub0b4\ub824\uc11c \uc785\uccb4\uac10 */\n"
"}")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"")
        self.chart = QGroupBox(self.tab)
        self.chart.setObjectName(u"chart")
        self.chart.setGeometry(QRect(0, 50, 1401, 661))
        self.chart.setStyleSheet(u"QGroupBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(40, 40, 45, 255), \n"
"                                      stop:1 rgba(25, 25, 30, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180);  /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px;\n"
"    font: 11pt \"Roboto\";\n"
"    color: rgba(220, 220, 220, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"    color: rgba(180, 180, 190, 255);  /* \uc740\uc740\ud55c \ud68c\uc0c9 */\n"
"}\n"
"\n"
"QGroupBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 200);  /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uac15\uc870 */\n"
"}")
        self.charTab1 = QGroupBox(self.tab)
        self.charTab1.setObjectName(u"charTab1")
        self.charTab1.setGeometry(QRect(0, 0, 1401, 41))
        self.charTab1.setStyleSheet(u"QGroupBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(40, 40, 45, 255), \n"
"                                      stop:1 rgba(25, 25, 30, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180);  /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px;\n"
"    font: 11pt \"Roboto\";\n"
"    color: rgba(220, 220, 220, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"    color: rgba(180, 180, 190, 255);  /* \uc740\uc740\ud55c \ud68c\uc0c9 */\n"
"}\n"
"\n"
"QGroupBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 200);  /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uac15\uc870 */\n"
"}")
        self.label_2 = QLabel(self.charTab1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 14, 71, 16))
        self.label_2.setStyleSheet(u"QLabel {\n"
"    background: transparent;  /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: rgba(220, 220, 230, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ub77c\uc774\ud2b8 \uadf8\ub808\uc774 */\n"
"    font: 10.5pt \"Roboto\";\n"
"    padding-top: 0px;\n"
"    padding-bottom: 0px;\n"
"    margin-top: 0px;\n"
"    margin-bottom: 0px;\n"
"}")
        self.access_key = QLineEdit(self.charTab1)
        self.access_key.setObjectName(u"access_key")
        self.access_key.setGeometry(QRect(90, 10, 191, 21))
        self.access_key.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(40, 40, 50, 255);  /* \ub2e4\ud06c \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uae30\ubcf8 \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    selection-background-color: rgba(80, 80, 100, 255); /* \uc120\ud0dd \uc601\uc5ed \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud3ec\ucee4\uc2a4 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}")
        self.save_button = QPushButton(self.charTab1)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setGeometry(QRect(690, 10, 41, 21))
        self.save_button.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450"
                        "\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.api_select = QComboBox(self.charTab1)
        self.api_select.addItem("")
        self.api_select.setObjectName(u"api_select")
        self.api_select.setGeometry(QRect(580, 10, 101, 22))
        self.api_select.setStyleSheet(u"QComboBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"    background-color: rgba(60, 60, 70, 255); /* \ub4dc"
                        "\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc0c9\uc0c1 */\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(down_arrow.png); /* \ub4dc\ub86d\ub2e4\uc6b4 \uc544\uc774\ucf58 (\uc774\ubbf8\uc9c0 \uacbd\ub85c \ud544\uc694) */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgba(40, 40, 50, 255); /* \ub4dc\ub86d\ub2e4\uc6b4 \ub9ac\uc2a4\ud2b8 \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180);\n"
"    selection-background-color: rgba(80, 80, 90, 255); /* \uc120\ud0dd \uc2dc \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"    color: rgba(220, 220, 230, 230);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(100, 100, 120, 255); /* \uc120\ud0dd\ub41c \ud56d\ubaa9 \uac15\uc870 */\n"
"    color: "
                        "rgba(255, 255, 255, 255);\n"
"}")
        self.secret_key = QLineEdit(self.charTab1)
        self.secret_key.setObjectName(u"secret_key")
        self.secret_key.setGeometry(QRect(380, 10, 191, 21))
        self.secret_key.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(40, 40, 50, 255);  /* \ub2e4\ud06c \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uae30\ubcf8 \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    selection-background-color: rgba(80, 80, 100, 255); /* \uc120\ud0dd \uc601\uc5ed \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud3ec\ucee4\uc2a4 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}")
        self.label_4 = QLabel(self.charTab1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(300, 14, 71, 16))
        self.label_4.setStyleSheet(u"QLabel {\n"
"    background: transparent;  /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: rgba(220, 220, 230, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ub77c\uc774\ud2b8 \uadf8\ub808\uc774 */\n"
"    font: 10.5pt \"Roboto\";\n"
"    padding-top: 0px;\n"
"    padding-bottom: 0px;\n"
"    margin-top: 0px;\n"
"    margin-bottom: 0px;\n"
"}")
        self.buy_sell = QGroupBox(self.tab)
        self.buy_sell.setObjectName(u"buy_sell")
        self.buy_sell.setGeometry(QRect(1410, 150, 491, 831))
        self.buy_sell.setStyleSheet(u"QGroupBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(40, 40, 45, 255), \n"
"                                      stop:1 rgba(25, 25, 30, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180);  /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px;\n"
"    font: 11pt \"Roboto\";\n"
"    color: rgba(220, 220, 220, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"    color: rgba(180, 180, 190, 255);  /* \uc740\uc740\ud55c \ud68c\uc0c9 */\n"
"}\n"
"\n"
"QGroupBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 200);  /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uac15\uc870 */\n"
"}")
        self.coin_selete = QComboBox(self.buy_sell)
        self.coin_selete.setObjectName(u"coin_selete")
        self.coin_selete.setGeometry(QRect(10, 10, 151, 22))
        self.coin_selete.setStyleSheet(u"QComboBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"    background-color: rgba(60, 60, 70, 255); /* \ub4dc"
                        "\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc0c9\uc0c1 */\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(down_arrow.png); /* \ub4dc\ub86d\ub2e4\uc6b4 \uc544\uc774\ucf58 (\uc774\ubbf8\uc9c0 \uacbd\ub85c \ud544\uc694) */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgba(40, 40, 50, 255); /* \ub4dc\ub86d\ub2e4\uc6b4 \ub9ac\uc2a4\ud2b8 \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180);\n"
"    selection-background-color: rgba(80, 80, 90, 255); /* \uc120\ud0dd \uc2dc \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"    color: rgba(220, 220, 230, 230);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(100, 100, 120, 255); /* \uc120\ud0dd\ub41c \ud56d\ubaa9 \uac15\uc870 */\n"
"    color: "
                        "rgba(255, 255, 255, 255);\n"
"}")
        self.buy_button = QPushButton(self.buy_sell)
        self.buy_button.setObjectName(u"buy_button")
        self.buy_button.setGeometry(QRect(310, 800, 75, 23))
        self.buy_button.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450"
                        "\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.label_5 = QLabel(self.buy_sell)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(70, 800, 61, 16))
        self.label_5.setStyleSheet(u"QLabel {\n"
"    background: transparent;  /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: rgba(220, 220, 230, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ub77c\uc774\ud2b8 \uadf8\ub808\uc774 */\n"
"    font: 10.5pt \"Roboto\";\n"
"    padding-top: 0px;\n"
"    padding-bottom: 0px;\n"
"    margin-top: 0px;\n"
"    margin-bottom: 0px;\n"
"}")
        self.direct_input_2 = QLineEdit(self.buy_sell)
        self.direct_input_2.setObjectName(u"direct_input_2")
        self.direct_input_2.setGeometry(QRect(140, 800, 161, 20))
        self.direct_input_2.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(40, 40, 50, 255);  /* \ub2e4\ud06c \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uae30\ubcf8 \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    selection-background-color: rgba(80, 80, 100, 255); /* \uc120\ud0dd \uc601\uc5ed \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud3ec\ucee4\uc2a4 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}")
        self.buy_button_2 = QPushButton(self.buy_sell)
        self.buy_button_2.setObjectName(u"buy_button_2")
        self.buy_button_2.setGeometry(QRect(400, 800, 75, 23))
        self.buy_button_2.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450"
                        "\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.groupBox_4 = QGroupBox(self.buy_sell)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 90, 471, 701))
        self.groupBox_4.setStyleSheet(u"QGroupBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(40, 40, 45, 255), \n"
"                                      stop:1 rgba(25, 25, 30, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180);  /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px;\n"
"    font: 11pt \"Roboto\";\n"
"    color: rgba(220, 220, 220, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"    color: rgba(180, 180, 190, 255);  /* \uc740\uc740\ud55c \ud68c\uc0c9 */\n"
"}\n"
"\n"
"QGroupBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 200);  /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uac15\uc870 */\n"
"}")
        self.coin_selete_2 = QComboBox(self.buy_sell)
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.addItem("")
        self.coin_selete_2.setObjectName(u"coin_selete_2")
        self.coin_selete_2.setGeometry(QRect(170, 10, 151, 22))
        self.coin_selete_2.setStyleSheet(u"QComboBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"    background-color: rgba(60, 60, 70, 255); /* \ub4dc"
                        "\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc0c9\uc0c1 */\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(down_arrow.png); /* \ub4dc\ub86d\ub2e4\uc6b4 \uc544\uc774\ucf58 (\uc774\ubbf8\uc9c0 \uacbd\ub85c \ud544\uc694) */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgba(40, 40, 50, 255); /* \ub4dc\ub86d\ub2e4\uc6b4 \ub9ac\uc2a4\ud2b8 \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180);\n"
"    selection-background-color: rgba(80, 80, 90, 255); /* \uc120\ud0dd \uc2dc \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"    color: rgba(220, 220, 230, 230);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(100, 100, 120, 255); /* \uc120\ud0dd\ub41c \ud56d\ubaa9 \uac15\uc870 */\n"
"    color: "
                        "rgba(255, 255, 255, 255);\n"
"}")
        self.coin_selete_3 = QComboBox(self.buy_sell)
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.addItem("")
        self.coin_selete_3.setObjectName(u"coin_selete_3")
        self.coin_selete_3.setGeometry(QRect(330, 10, 151, 22))
        self.coin_selete_3.setStyleSheet(u"QComboBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"    background-color: rgba(60, 60, 70, 255); /* \ub4dc"
                        "\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc0c9\uc0c1 */\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(down_arrow.png); /* \ub4dc\ub86d\ub2e4\uc6b4 \uc544\uc774\ucf58 (\uc774\ubbf8\uc9c0 \uacbd\ub85c \ud544\uc694) */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgba(40, 40, 50, 255); /* \ub4dc\ub86d\ub2e4\uc6b4 \ub9ac\uc2a4\ud2b8 \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180);\n"
"    selection-background-color: rgba(80, 80, 90, 255); /* \uc120\ud0dd \uc2dc \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"    color: rgba(220, 220, 230, 230);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(100, 100, 120, 255); /* \uc120\ud0dd\ub41c \ud56d\ubaa9 \uac15\uc870 */\n"
"    color: "
                        "rgba(255, 255, 255, 255);\n"
"}")
        self.label_3 = QLabel(self.buy_sell)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 40, 221, 21))
        self.label_3.setStyleSheet(u"QLabel {\n"
"    background: transparent;  /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: rgba(220, 220, 230, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ub77c\uc774\ud2b8 \uadf8\ub808\uc774 */\n"
"    font: 10.5pt \"Roboto\";\n"
"    padding-top: 0px;\n"
"    padding-bottom: 0px;\n"
"    margin-top: 0px;\n"
"    margin-bottom: 0px;\n"
"}")
        self.label_6 = QLabel(self.buy_sell)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(250, 40, 231, 21))
        self.label_6.setStyleSheet(u"QLabel {\n"
"    background: transparent;  /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: rgba(220, 220, 230, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ub77c\uc774\ud2b8 \uadf8\ub808\uc774 */\n"
"    font: 10.5pt \"Roboto\";\n"
"    padding-top: 0px;\n"
"    padding-bottom: 0px;\n"
"    margin-top: 0px;\n"
"    margin-bottom: 0px;\n"
"}")
        self.label_7 = QLabel(self.buy_sell)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 60, 221, 21))
        self.label_7.setStyleSheet(u"QLabel {\n"
"    background: transparent;  /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: rgba(220, 220, 230, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ub77c\uc774\ud2b8 \uadf8\ub808\uc774 */\n"
"    font: 10.5pt \"Roboto\";\n"
"    padding-top: 0px;\n"
"    padding-bottom: 0px;\n"
"    margin-top: 0px;\n"
"    margin-bottom: 0px;\n"
"}")
        self.label_8 = QLabel(self.buy_sell)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(250, 60, 231, 21))
        self.label_8.setStyleSheet(u"QLabel {\n"
"    background: transparent;  /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: rgba(220, 220, 230, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ub77c\uc774\ud2b8 \uadf8\ub808\uc774 */\n"
"    font: 10.5pt \"Roboto\";\n"
"    padding-top: 0px;\n"
"    padding-bottom: 0px;\n"
"    margin-top: 0px;\n"
"    margin-bottom: 0px;\n"
"}")
        self.graph = QFrame(self.tab)
        self.graph.setObjectName(u"graph")
        self.graph.setGeometry(QRect(0, 720, 1401, 261))
        self.graph.setStyleSheet(u"QFrame {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(40, 40, 45, 255), \n"
"                                      stop:1 rgba(25, 25, 30, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180);  /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px;\n"
"    font: 11pt \"Roboto\";\n"
"    color: rgba(220, 220, 220, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QFrame::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"    color: rgba(180, 180, 190, 255);  /* \uc740\uc740\ud55c \ud68c\uc0c9 */\n"
"}")
        self.graph.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(1410, 0, 491, 131))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(110)
        font.setBold(True)
        font.setItalic(False)
        font.setStyleStrategy(QFont.PreferDefault)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label.setStyleSheet(u"QLabel {\n"
"    background: transparent;\n"
"    color: rgba(230, 230, 240, 255);  /* \ubc1d\uc740 \ud654\uc774\ud2b8\ud1a4 */\n"
"    font: bold 110pt \"Segoe UI\";  /* \ud06c\uace0 \uc138\ub828\ub41c \ud3f0\ud2b8 */\n"
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
        self.strategy_combo.setObjectName(u"strategy_combo")
        self.strategy_combo.setGeometry(QRect(10, 10, 211, 22))
        self.strategy_combo.setStyleSheet(u"QComboBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"    background-color: rgba(60, 60, 70, 255); /* \ub4dc"
                        "\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc0c9\uc0c1 */\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(down_arrow.png); /* \ub4dc\ub86d\ub2e4\uc6b4 \uc544\uc774\ucf58 (\uc774\ubbf8\uc9c0 \uacbd\ub85c \ud544\uc694) */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgba(40, 40, 50, 255); /* \ub4dc\ub86d\ub2e4\uc6b4 \ub9ac\uc2a4\ud2b8 \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180);\n"
"    selection-background-color: rgba(80, 80, 90, 255); /* \uc120\ud0dd \uc2dc \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"    color: rgba(220, 220, 230, 230);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(100, 100, 120, 255); /* \uc120\ud0dd\ub41c \ud56d\ubaa9 \uac15\uc870 */\n"
"    color: "
                        "rgba(255, 255, 255, 255);\n"
"}")
        self.start_button = QPushButton(self.scrollAreaWidgetContents)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setGeometry(QRect(1640, 10, 75, 23))
        self.start_button.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450"
                        "\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(0, 40, 1311, 941))
        self.groupBox_2.setStyleSheet(u"QGroupBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(40, 40, 45, 255), \n"
"                                      stop:1 rgba(25, 25, 30, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180);  /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px;\n"
"    padding: 5px;\n"
"    font: 11pt \"Roboto\";\n"
"    color: rgba(220, 220, 220, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QGroupBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 200);  /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uac15\uc870 */\n"
"}")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_2 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(1810, 10, 75, 23))
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450"
                        "\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.stop_button = QPushButton(self.scrollAreaWidgetContents)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setGeometry(QRect(1720, 10, 81, 23))
        self.stop_button.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450"
                        "\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.strategy_combo_2 = QComboBox(self.scrollAreaWidgetContents)
        self.strategy_combo_2.setObjectName(u"strategy_combo_2")
        self.strategy_combo_2.setGeometry(QRect(1480, 10, 151, 21))
        self.strategy_combo_2.setStyleSheet(u"QComboBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"    background-color: rgba(60, 60, 70, 255); /* \ub4dc"
                        "\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc0c9\uc0c1 */\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(down_arrow.png); /* \ub4dc\ub86d\ub2e4\uc6b4 \uc544\uc774\ucf58 (\uc774\ubbf8\uc9c0 \uacbd\ub85c \ud544\uc694) */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgba(40, 40, 50, 255); /* \ub4dc\ub86d\ub2e4\uc6b4 \ub9ac\uc2a4\ud2b8 \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180);\n"
"    selection-background-color: rgba(80, 80, 90, 255); /* \uc120\ud0dd \uc2dc \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"    color: rgba(220, 220, 230, 230);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(100, 100, 120, 255); /* \uc120\ud0dd\ub41c \ud56d\ubaa9 \uac15\uc870 */\n"
"    color: "
                        "rgba(255, 255, 255, 255);\n"
"}")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(1320, 210, 581, 771))
        self.groupBox.setStyleSheet(u"QGroupBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(40, 40, 45, 255), \n"
"                                      stop:1 rgba(25, 25, 30, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180);  /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px;\n"
"    font: 11pt \"Roboto\";\n"
"    color: rgba(220, 220, 220, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"    color: rgba(180, 180, 190, 255);  /* \uc740\uc740\ud55c \ud68c\uc0c9 */\n"
"}\n"
"\n"
"QGroupBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 200);  /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uac15\uc870 */\n"
"}")
        self.history = QListWidget(self.groupBox)
        self.history.setObjectName(u"history")
        self.history.setGeometry(QRect(10, 10, 561, 751))
        self.history.setStyleSheet(u"QListWidget {\n"
"    background-color: rgba(40, 40, 50, 255);  /* \ub2e4\ud06c\ud55c \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uc740 \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 5px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    padding: 8px;\n"
"    margin: 2px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QListWidget::item:hover {\n"
"    background-color: rgba(70, 70, 80, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uac15\uc870 */\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background-color: rgba(100, 100, 120, 255); /* \uc120\ud0dd\ub41c \ud56d\ubaa9 */\n"
"    color: rgba(255, 255, 255, 255);\n"
"}\n"
"\n"
"QListWidget::item:selected:active {\n"
"    background-color: rgba(120, 120, 140, 255); /* \uc120\ud0dd \uc0c1\ud0dc\uc5d0\uc11c \ud074\ub9ad \uc2dc \uac15\uc870 */\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
""
                        "    background: rgba(50, 50, 60, 255); /* \uc2a4\ud06c\ub864\ubc14 \ubc30\uacbd */\n"
"    width: 8px;\n"
"    margin: 2px 0;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: rgba(120, 120, 130, 255); /* \uc2a4\ud06c\ub864 \ud578\ub4e4 */\n"
"    min-height: 20px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: rgba(150, 150, 160, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uac15\uc870 */\n"
"}\n"
"\n"
"QScrollBar::add-line, QScrollBar::sub-line {\n"
"    background: none; /* \uc704\uc544\ub798 \ubc84\ud2bc \uc81c\uac70 */\n"
"}")
        self.pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(1320, 40, 261, 161))
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 8px 15px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074"
                        "\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.start_button_2 = QPushButton(self.scrollAreaWidgetContents)
        self.start_button_2.setObjectName(u"start_button_2")
        self.start_button_2.setGeometry(QRect(230, 10, 75, 23))
        self.start_button_2.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450"
                        "\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.clear_button = QPushButton(self.scrollAreaWidgetContents)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setGeometry(QRect(310, 10, 75, 23))
        self.clear_button.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450"
                        "\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.back_group = QGroupBox(self.scrollAreaWidgetContents)
        self.back_group.setObjectName(u"back_group")
        self.back_group.setGeometry(QRect(1590, 40, 311, 161))
        self.back_group.setStyleSheet(u"QGroupBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(40, 40, 45, 255), \n"
"                                      stop:1 rgba(25, 25, 30, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180);  /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 8px;\n"
"    font: 11pt \"Roboto\";\n"
"    color: rgba(220, 220, 220, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"    color: rgba(180, 180, 190, 255);  /* \uc740\uc740\ud55c \ud68c\uc0c9 */\n"
"}\n"
"\n"
"QGroupBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 200);  /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uac15\uc870 */\n"
"}")
        self.back_start = QPushButton(self.back_group)
        self.back_start.setObjectName(u"back_start")
        self.back_start.setGeometry(QRect(10, 40, 291, 51))
        self.back_start.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 8px 15px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074"
                        "\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.back_result = QPushButton(self.back_group)
        self.back_result.setObjectName(u"back_result")
        self.back_result.setGeometry(QRect(10, 100, 291, 51))
        self.back_result.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 8px 15px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(80, 80, 90, 255); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(60, 60, 70, 255); /* \ud074\ub9ad \uc2dc \uc5b4\ub450\uc6cc\uc9d0 */\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074"
                        "\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 40, 45, 255); /* \ube44\ud65c\uc131\ud654 \uc2dc \ub354 \uc5b4\ub461\uac8c */\n"
"    color: rgba(120, 120, 130, 180); /* \ube44\ud65c\uc131\ud654\ub41c \ud14d\uc2a4\ud2b8 */\n"
"    border: 1px solid rgba(80, 80, 90, 150);\n"
"}")
        self.back_count = QComboBox(self.back_group)
        self.back_count.setObjectName(u"back_count")
        self.back_count.setGeometry(QRect(10, 10, 141, 21))
        self.back_count.setStyleSheet(u"QComboBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"    background-color: rgba(60, 60, 70, 255); /* \ub4dc"
                        "\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc0c9\uc0c1 */\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(down_arrow.png); /* \ub4dc\ub86d\ub2e4\uc6b4 \uc544\uc774\ucf58 (\uc774\ubbf8\uc9c0 \uacbd\ub85c \ud544\uc694) */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgba(40, 40, 50, 255); /* \ub4dc\ub86d\ub2e4\uc6b4 \ub9ac\uc2a4\ud2b8 \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180);\n"
"    selection-background-color: rgba(80, 80, 90, 255); /* \uc120\ud0dd \uc2dc \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"    color: rgba(220, 220, 230, 230);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(100, 100, 120, 255); /* \uc120\ud0dd\ub41c \ud56d\ubaa9 \uac15\uc870 */\n"
"    color: "
                        "rgba(255, 255, 255, 255);\n"
"}")
        self.back_time = QComboBox(self.back_group)
        self.back_time.setObjectName(u"back_time")
        self.back_time.setGeometry(QRect(160, 10, 141, 21))
        self.back_time.setStyleSheet(u"QComboBox {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                      stop:0 rgba(50, 50, 55, 255), \n"
"                                      stop:1 rgba(30, 30, 35, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    border: 1px solid rgba(100, 100, 110, 180); /* \uc587\uace0 \uc138\ub828\ub41c \ud14c\ub450\ub9ac */\n"
"    border-radius: 6px;\n"
"    padding: 0px 10px;\n"
"    font: 10.5pt \"Roboto\";\n"
"    color: rgba(220, 220, 230, 230); /* \ubd80\ub4dc\ub7ec\uc6b4 \ud654\uc774\ud2b8 \ud1a4 */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid rgba(150, 150, 160, 220); /* \ub9c8\uc6b0\uc2a4 \uc624\ubc84 \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid rgba(180, 180, 200, 255); /* \ud074\ub9ad \uc2dc \ud14c\ub450\ub9ac \uac15\uc870 */\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"    background-color: rgba(60, 60, 70, 255); /* \ub4dc"
                        "\ub86d\ub2e4\uc6b4 \ubc84\ud2bc \uc0c9\uc0c1 */\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(down_arrow.png); /* \ub4dc\ub86d\ub2e4\uc6b4 \uc544\uc774\ucf58 (\uc774\ubbf8\uc9c0 \uacbd\ub85c \ud544\uc694) */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgba(40, 40, 50, 255); /* \ub4dc\ub86d\ub2e4\uc6b4 \ub9ac\uc2a4\ud2b8 \ubc30\uacbd */\n"
"    border: 1px solid rgba(100, 100, 110, 180);\n"
"    selection-background-color: rgba(80, 80, 90, 255); /* \uc120\ud0dd \uc2dc \ubc30\uacbd */\n"
"    selection-color: rgba(255, 255, 255, 255);\n"
"    color: rgba(220, 220, 230, 230);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(100, 100, 120, 255); /* \uc120\ud0dd\ub41c \ud56d\ubaa9 \uac15\uc870 */\n"
"    color: "
                        "rgba(255, 255, 255, 255);\n"
"}")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
    
        # ✅ 종료 버튼 추가
        self.exit_button = QPushButton(self.centralwidget)
        self.exit_button.setObjectName(u"exit_button")
        self.exit_button.setGeometry(QRect(1880, 5, 30, 25))  # 오른쪽 상단에 위치
        self.exit_button.setStyleSheet("""
                QPushButton {
                background-color: #4C566A;  /* 버튼 배경색 */
                color: #ECEFF4;  /* 버튼 텍스트 색상 */
                border: none;
                border-radius: 5px;  /* 모서리 둥글게 */
                }
                QPushButton:hover {
                background-color: #5E81AC;  /* 호버 시 배경색 */
                }
                QPushButton:pressed {
                background-color: #3B4252;  /* 클릭 시 배경색 */
                }
        """)
        self.exit_button.setText("X")
        self.exit_button.clicked.connect(QApplication.quit)  # 클릭 시 프로그램 종료
        
        # 네모 버튼 추가
        self.minimize_button = QPushButton(self.centralwidget)
        self.minimize_button.setGeometry(1850, 5, 30, 25)  # 버튼 위치와 크기 설정
        self.minimize_button.setText("□")  # 네모 모양 텍스트
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #4C566A;  /* 버튼 배경색 */
                color: #ECEFF4;  /* 버튼 텍스트 색상 */
                border: none;
                border-radius: 5px;  /* 모서리 둥글게 */
            }
            QPushButton:hover {
                background-color: #5E81AC;  /* 호버 시 배경색 */
            }
            QPushButton:pressed {
                background-color: #3B4252;  /* 클릭 시 배경색 */
            }
        """)

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
        self.groupBox_4.setTitle("")
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
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\ubcf4\uc720 KRW : ", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\uc218\uc775\ub960 : ", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"COB2N", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\ucc28\ud2b8", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\ud589", None))
        self.groupBox_2.setTitle("")
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\ub3c4\uc6c0\ub9d0", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"\uc911\uc9c0", None))
        self.groupBox.setTitle("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\ube14\ub85d \ucd94\uac00 +", None))
        self.start_button_2.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.clear_button.setText(QCoreApplication.translate("MainWindow", u"\ucd08\uae30\ud654", None))
        self.back_group.setTitle("")
        self.back_start.setText(QCoreApplication.translate("MainWindow", u"\ubc31\ud14c\uc2a4\ud2b8 \uc2dc\uc791", None))
        self.back_result.setText(QCoreApplication.translate("MainWindow", u"\ubc31\ud14c\uc2a4\ud2b8 \uacb0\uacfc \ud655\uc778\ud558\uae30", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\uc2e4\ud589", None))
        pass
    # retranslateUi

