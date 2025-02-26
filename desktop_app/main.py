import sys
import platform
import requests
from PySide6 import QtCore
from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide6.QtWidgets import *

from ui.ui_login import Ui_login
from ui.ui_main import Ui_MainWindow
from upbit.execute_upbit import *

class User():
    def __init__(self, username, password):
        self.username = username
    
    # firebase에 활동 로그 저장
    def save_log(self, log):
        pass
    
    # firebase에 활동 로그 조회
    def load_log(self):
        pass



# 메인 윈도우 클래스
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        ###################
        # 타이틀바 삭제
        ###################
        
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
        
        ###########################################################
        # tab2 (블록 선택 & 배치 영역에 스크롤 추가)
        ###########################################################
        



# 로그인 윈도우 클래스
class SpleshScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_login()
        self.ui.setupUi(self)
        
        
        ###################
        # 타이틀바 삭제
        ###################
        
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        
        
        ###################
        # 그림자 설정
        ###################
        
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.frame.setGraphicsEffect(self.shadow)
        
        self.show()
        
        self.ui.pushButton.clicked.connect(self.login_button_clicked)
    
    
    ###########################
    # 로그인
    ###########################
    def login_button_clicked(self):
        url = 'http://127.0.0.1:8000/api/token/'
        
        payload = {
            'username': self.ui.user_id.text(),
            'password': self.ui.user_password.text(),
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens['access']
            print("Access Token:", access_token)

            # 보호된 API에 접근
            headers = {'Authorization': f'Bearer {access_token}'}
            api_response = requests.get('http://127.0.0.1:8000/protected-api/', headers=headers)

            if api_response.status_code == 200:
                print("성공적으로 접근:", api_response.json())
                self.main = MainWindow()
                self.main.show()
                
                self.close()
            else:
                print("API 접근 실패:", api_response.status_code)
                # 로그인 실패 메시지 팝업
                QMessageBox.critical(self, '로그인 실패', '아이디 또는 비밀번호가 일치하지 않습니다.')
        else:
            print("로그인 실패:", response.json())
            # 로그인 실패 메시지 팝업
            QMessageBox.critical(self, '로그인 실패', '아이디 또는 비밀번호가 일치하지 않습니다.')
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = SpleshScreen()
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())