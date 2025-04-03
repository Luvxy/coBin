# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'small_windowLzITTp.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QWidget)

class UI_SmallWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(502, 301)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                stop:0 rgba(30, 30, 40, 255), \n"
"                                stop:1 rgba(20, 20, 30, 255)); /* \ub2e4\ud06c \uadf8\ub77c\ub370\uc774\uc158 */\n"
"    color: rgba(220, 220, 230, 230); /* \uc804\uccb4 \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"}")
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 10, 261, 81))
        self.groupBox_3.setStyleSheet(u"QGroupBox {\n"
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
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 10, 251, 16))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(u"QLabel {\n"
"    background: transparent;  /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: rgba(220, 220, 230, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ub77c\uc774\ud2b8 \uadf8\ub808\uc774 */\n"
"    font: 10.5pt \"Roboto\";\n"
"    padding-top: 0px;\n"
"    padding-bottom: 0px;\n"
"    margin-top: 0px;\n"
"    margin-bottom: 0px;\n"
"}")
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 30, 251, 20))
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(u"QLabel {\n"
"    background: transparent;  /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: rgba(220, 220, 230, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ub77c\uc774\ud2b8 \uadf8\ub808\uc774 */\n"
"    font: 10.5pt \"Roboto\";\n"
"    padding-top: 0px;\n"
"    padding-bottom: 0px;\n"
"    margin-top: 0px;\n"
"    margin-bottom: 0px;\n"
"}")
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 50, 251, 21))
        self.label_11.setFont(font)
        self.label_11.setStyleSheet(u"QLabel {\n"
"    background: transparent;  /* \ubc30\uacbd \ud22c\uba85 */\n"
"    color: rgba(220, 220, 230, 230);  /* \ubd80\ub4dc\ub7ec\uc6b4 \ub77c\uc774\ud2b8 \uadf8\ub808\uc774 */\n"
"    font: 10.5pt \"Roboto\";\n"
"    padding-top: 0px;\n"
"    padding-bottom: 0px;\n"
"    margin-top: 0px;\n"
"    margin-bottom: 0px;\n"
"}")
        self.strategy_combo_2 = QComboBox(self.centralwidget)
        self.strategy_combo_2.setObjectName(u"strategy_combo_2")
        self.strategy_combo_2.setGeometry(QRect(280, 40, 151, 21))
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
        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setGeometry(QRect(280, 70, 75, 23))
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
        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setGeometry(QRect(370, 70, 81, 23))
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
        self.strategy_combo = QComboBox(self.centralwidget)
        self.strategy_combo.setObjectName(u"strategy_combo")
        self.strategy_combo.setGeometry(QRect(280, 10, 211, 22))
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
        self.history = QListWidget(self.centralwidget)
        self.history.setObjectName(u"history")
        self.history.setGeometry(QRect(10, 100, 481, 191))
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
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_3.setTitle("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\uae08\ud654 : 0", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\uc740\ud654 : 0", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\ud589 \uc2dc\uac04 : 0", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\ud589", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"\uc911\uc9c0", None))
    # retranslateUi

