# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginRbsOSa.ui'
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


class Ui_login(object):
    def setupUi(self, login):
        if login.objectName():
            login.setObjectName(u"login")
        login.resize(698, 493)
        login.setInputMethodHints(Qt.ImhNone)
        self.centralwidget = QWidget(login)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 691, 471))
        self.frame.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(51, 51, 51);\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 130, 691, 81))
        font = QFont()
        font.setFamily(u"\ub3cb\uc6c0")
        font.setPointSize(50)
        self.label.setFont(font)
        self.label.setStyleSheet(u"QLabel{\n"
"	color: rgb(255, 255, 255);\n"
"}")
        self.label.setAlignment(Qt.AlignCenter)
        self.user_id = QLineEdit(self.frame)
        self.user_id.setObjectName(u"user_id")
        self.user_id.setGeometry(QRect(240, 230, 211, 20))
        self.user_password = QLineEdit(self.frame)
        self.user_password.setObjectName(u"user_password")
        self.user_password.setGeometry(QRect(240, 260, 211, 20))
        self.user_password.setInputMethodHints(Qt.ImhHiddenText|Qt.ImhNoAutoUppercase|Qt.ImhNoPredictiveText|Qt.ImhSensitiveData)
        self.user_password.setEchoMode(QLineEdit.Password)
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(240, 290, 211, 51))
        login.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(login)
        self.statusbar.setObjectName(u"statusbar")
        login.setStatusBar(self.statusbar)

        self.retranslateUi(login)

        QMetaObject.connectSlotsByName(login)
    # setupUi

    def retranslateUi(self, login):
        login.setWindowTitle(QCoreApplication.translate("login", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("login", u"Login", None))
        self.user_id.setText("")
        self.user_password.setText("")
        self.pushButton.setText(QCoreApplication.translate("login", u"Login", None))
    # retranslateUi

