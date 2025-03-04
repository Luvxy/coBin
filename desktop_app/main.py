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
from ui.ui_block import BlockMain
from upbit.get_data_upbit import *
from upbit.execute_upbit import *
import finplot as fplt

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
        
        # ✅ Esc 키 방지
        self.installEventFilter(self)
        
        ###################
        # 타이틀바 삭제
        ###################
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
        
        ###########################################################
        # tab2 (블록 선택 & 배치 영역에 스크롤 추가)
        ###########################################################
        
        self.blockFrame = BlockMain()
        self.ui.verticalLayout.addWidget(self.blockFrame)
        self.ui.strategy_combo_2.addItems(["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-DOGE"])
        self.ui.start_button.clicked.connect(self.blockFrame.run_all_blocks)
        self.ui.stop_button.clicked.connect(self.blockFrame.stop_all_blocks)
        
        ###########################################################
        # tab1 그래프 추가 
        # self.ui.chart groupBox에 Chart 클래스 추가
        ###########################################################        
        # finplot 기반 ChartWidget 생성
        self.chart = ChartWidget(coin="KRW-BTC")
        self.chart_layout = QVBoxLayout(self.ui.chart)  # self.ui.chart는 QFrame or QWidget
        self.chart_layout.addWidget(self.chart)
        
        # 코인 리스트 콤보박스
        self.ui.coin_selete.addItems(["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-DOGE"])
        self.ui.coin_selete.currentTextChanged.connect(self.update_chart)
        
        # ✅ 그래프 UI 레이아웃 설정
        self.graph_layout = QVBoxLayout(self.ui.graph)
        self.ui.graph.setLayout(self.graph_layout)

        # ✅ 거래량 차트만 생성 (ax0 없이 ax1만 사용)
        self.ax1 = fplt.create_plot_widget(master=self.ui.graph, rows=1)
        self.graph_layout.addWidget(self.ax1.ax_widget)
        
        # ✅ order book widget 추가
        self.order = OrderBookWidget()
        self.order.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # ✅ 크기 자동 조정

        self.order_layout = QVBoxLayout(self.ui.groupBox_4)  # ✅ 부모 위젯의 레이아웃 설정
        self.order_layout.addWidget(self.order)
        self.order_layout.setContentsMargins(0, 0, 0, 0)  # ✅ 여백 제거
        self.order_layout.setStretch(0, 1)  # ✅ 레이아웃 내 OrderBookWidget이 최대한 확장되도록 설정

        # ✅ 초기 차트 로드
        self.current_coin = "KRW-BTC"
        self.update_chart()

    def update_chart(self):
        new_coin = self.ui.coin_selete.currentText()
        if new_coin == "선택":
            new_coin = "KRW-BTC"

        self.chart.change_coin(new_coin)
        self.order.change_coin(new_coin)  # ✅ OrderBook 변경
        self.current_coin = new_coin
        df = pyupbit.get_ohlcv(new_coin, interval='minute1', count=100)

        if df is None or df.empty:
            print(f"코인 데이터 로드 실패: {new_coin}")
            return

        df.columns = df.columns.str.lower()
        if not {'open', 'close', 'volume'}.issubset(df.columns):
            print(f"필요한 컬럼이 없음: {df.columns}")
            return

        # ✅ 기존 차트 초기화 & 새 데이터 적용
        if hasattr(self, "ax1"):
            self.ax1.reset()
            fplt.volume_ocv(df[['open', 'close', 'volume']], ax=self.ax1)
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore()  # ✅ Esc 키를 무시하여 창이 닫히지 않도록 함
        else:
            super().keyPressEvent(event)  # 기본 동작 유지





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
    # window.show()
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())