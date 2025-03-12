import sys
import platform
import requests
import json
from PySide6 import QtCore
from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide6.QtWidgets import *
from ui.ui_login import Ui_login
from ui.ui_main import Ui_MainWindow
from ui.ui_block import *
from upbit.get_data_upbit import *
from upbit.configer import *
from upbit.api_upbit import *
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
        
        ###########################################################
        # 기본 설정
        ###########################################################
        
        # 설정 파일 생성
        config_generator()
        self.ui.access_key.setEchoMode(QLineEdit.Password)
        self.ui.secret_key.setEchoMode(QLineEdit.Password)
        
        # load api keys
        config = config_read()
        self.access_key = config['API']['access_key']
        self.secret_key = config['API']['secret_key']
        
        self.ui.access_key.setText(self.access_key)
        self.ui.secret_key.setText(self.secret_key)
        
        # api 저장
        self.ui.save_button.clicked.connect(self.save_api)
        
        # upbit user 생성
        self.upbit = Upbit_api(self.access_key, self.secret_key)
        self.upbit.create_user()
        
        # button mapping
        self.ui.buy_button.clicked.connect(self.buy_market_order) # 매수
        self.ui.buy_button_2.clicked.connect(self.sell_market_order) # 매도
        
        # ✅ Esc 키 방지
        self.installEventFilter(self)
        
        ###################
        # 타이틀바 삭제
        ###################
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
        
        ###########################################################
        # tab2 (블록 선택 & 배치 영역에 스크롤 추가)
        ###########################################################
        
        self.blockFrame = BlockMain(self.upbit)
        self.ui.pushButton.clicked.connect(self.blockFrame.add_block)
        self.blockFrame.history = self.ui.history
        self.ui.strategy_combo.currentTextChanged.connect(self.load_strategy)
        self.ui.verticalLayout.addWidget(self.blockFrame)
        self.ui.strategy_combo_2.addItems(["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-DOGE"])
        self.ui.start_button.clicked.connect(self.blockFrame.run_all_blocks)
        self.ui.stop_button.clicked.connect(self.blockFrame.stop_all_blocks)
        self.ui.start_button_2.clicked.connect(self.save_custom_strategy)
        self.ui.clear_button.clicked.connect(self.blockFrame.clear_blocks)
        
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
        self.ui.coin_selete_2.currentTextChanged.connect(self.update_chart)
        self.ui.coin_selete_3.currentTextChanged.connect(self.update_chart)
        
        # 그래프 UI 레이아웃 설정
        self.graph_layout = QVBoxLayout(self.ui.graph)
        self.ui.graph.setLayout(self.graph_layout)

        # 거래량 차트만 생성 (ax0 없이 ax1만 사용)
        self.ax1 = fplt.create_plot_widget(master=self.ui.graph, rows=1)

        # ✅ PlotWidget을 QWidget으로 감싸서 추가
        self.graph_container = QWidget()
        self.graph_container_layout = QVBoxLayout(self.graph_container)
        self.graph_container_layout.addWidget(self.ax1.ax_widget)
        self.graph_container.setLayout(self.graph_container_layout)

        self.graph_layout.addWidget(self.graph_container)  # ✅ 감싼 위젯을 추가
        
        # order book widget 추가
        self.order = OrderBookWidget()
        self.order.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # ✅ 크기 자동 조정

        self.order_layout = QVBoxLayout(self.ui.groupBox_4)  # ✅ 부모 위젯의 레이아웃 설정
        self.order_layout.addWidget(self.order)
        self.order_layout.setContentsMargins(0, 0, 0, 0)  # ✅ 여백 제거
        self.order_layout.setStretch(0, 1)  # ✅ 레이아웃 내 OrderBookWidget이 최대한 확장되도록 설정

        # 초기 차트 로드
        self.current_coin = "KRW-BTC"
        self.update_chart()

    # 차트 업데이트 함수
    def update_chart(self):
        new_coin = self.ui.coin_selete.currentText()
        if new_coin == "선택":
            new_coin = "KRW-BTC"

        interval = self.ui.coin_selete_2.currentText()
        count = int(self.ui.coin_selete_3.currentText())
        
        if interval == "1분":
            interval = 'minute1'
        elif interval == "3분":
            interval = 'minute3'
        elif interval == "5분":
            interval = 'minute5'
        elif interval == "15분":
            interval = 'minute15'
        elif interval == "30분":
            interval = 'minute30'
        elif interval == "1시간":
            interval = 'minute60'
        else:
            interval = 'minute30'

        self.chart.change_coin(new_coin, interval, count)  # ChartWidget 변경
        self.order.change_coin(new_coin)  # OrderBook 변경
        self.ui.label_3.setText(f"보유량: {self.upbit.get_balance(new_coin)}")
        self.ui.label_6.setText(f"KRW: {self.upbit.get_balance('KRW')}")
        self.current_coin = new_coin
        df = pyupbit.get_ohlcv(new_coin, interval='minute1', count=100)

        if df is None or df.empty:
            print(f"코인 데이터 로드 실패: {new_coin}")
            return

        df.columns = df.columns.str.lower()
        if not {'open', 'close', 'volume'}.issubset(df.columns):
            print(f"필요한 컬럼이 없음: {df.columns}")
            return

        #  기존 차트 초기화 & 새 데이터 적용
        if hasattr(self, "ax1"):
            self.ax1.reset()
            fplt.volume_ocv(df[['open', 'close', 'volume']], ax=self.ax1)
    
    #  esc 버튼 클릭 시
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore()  # ✅ Esc 키를 무시하여 창이 닫히지 않도록 함
        else:
            super().keyPressEvent(event)  # 기본 동작 유지
            
    # 버장 버튼 클릭 시
    def save_api(self):
        self.access_key = self.ui.access_key.text()
        self.secret_key = self.ui.secret_key.text()
        
        self.upbit.access_key = self.access_key
        self.upbit.secret_key = self.secret_key
        
        config_edit('API', 'access_key', self.access_key)
        config_edit('API', 'secret_key', self.secret_key)
        config_edit('API', 'update', strftime('%Y-%m-%d %H:%M:%S'))
        
        QMessageBox.information(self, 'API 저장', 'API 키가 저장되었습니다.')
        
        self.upbit.create_user()
        if self.upbit.user is None:
            QMessageBox.critical(self, 'API 연결 실패', 'API 키가 올바르지 않습니다.')

        
    def buy_market_order(self):
        ticker = self.ui.coin_selete.currentText()
        cash = self.ui.direct_input_2.text()
        
        self.upbit.buy_market_order(ticker, cash)
        
        QMessageBox.information(self, '매수 주문', '주문이 완료되었습니다.')
        
        self.blance = self.upbit.get_balance(ticker)
        self.ui.label_3.setText(f"보유량: {self.blance}")
        self.ui.label_6.setText(f"KRW: {self.upbit.get_balance('KRW')}")
    
    def sell_market_order(self):
        ticker = self.ui.coin_selete.currentText()
        volume = self.ui.direct_input_2.text()
        
        self.upbit.sell_market_order(ticker, volume)
        
        QMessageBox.information(self, '매도 주문', '주문이 완료되었습니다.')
        self.blance = self.upbit.get_balance(ticker)
        self.ui.label_3.setText(f"보유량: {self.blance}")
        self.ui.label_6.setText(f"KRW: {self.upbit.get_balance('KRW')}")
        
    def load_custom_strategy(self, strategy_name):
        """ JSON 파일에서 Custom 전략 불러오기 """

        file_name = f"{strategy_name.lower().replace(' ', '')}.json"

        if not os.path.exists(file_name):
            print(f"{strategy_name} 전략이 존재하지 않음. 블록 초기화")
            self.blockFrame.clear_blocks()
            return

        with open(file_name, "r", encoding="utf-8") as f:
            strategy_data = json.load(f)

        self.blockFrame.clear_blocks()
        for block_data in strategy_data:
            block = self.blockFrame.add_block()
            if block is None:
                continue

            block_widget = self.blockFrame.layout.itemAt(self.blockFrame.layout.count() - 1).widget().findChild(QListWidget)

            # 조건 불러오기
            for condition_data in block_data["조건"]:
                condition_name = condition_data["이름"]
                condition_settings = condition_data["설정값"]
                condition = ConditionRegistry.create_condition(condition_name, **condition_settings)
                block.conditions.append(condition)
                if block_widget:
                    block_widget.addItem(f"조건: {condition.name}")

            # 액션 불러오기
            if block_data["액션"]:
                action_name = block_data["액션"]["이름"]
                action_settings = block_data["액션"]["설정값"]
                action = ActionRegistry.create_action(action_name, self.blockFrame.upbit, **action_settings)
                block.action = action
                if block_widget:
                    block_widget.addItem(f"액션: {action.name}")

            # 주기 설정 적용
            if hasattr(block, "interval_edit"):
                block.interval_edit.setText(block_data.get("주기", "10"))

        print(f"{strategy_name} 전략을 불러왔습니다.")

    
    def load_strategy(self, strategy_name):
        """ 기본 전략 불러오기 """
        self.blockFrame.clear_blocks()

        if strategy_name == "기본전략":
            self.load_custom_strategy("default")
        else:
            self.load_custom_strategy(strategy_name)

    def save_custom_strategy(self):
        """ 현재 블록 상태를 JSON 파일로 저장 """
        strategy_name = self.ui.strategy_combo.currentText()
        if strategy_name not in ["Custom 1", "Custom 2", "Custom 3"]:
            print("저장 가능한 Custom 전략이 아닙니다.")
            return

        file_name = f"{strategy_name.lower().replace(' ', '')}.json"

        strategy_data = []
        for block in self.blockFrame.blocks:
            block_data = {
                "조건": [],
                "액션": None,
                "주기": block.interval_edit.text() if hasattr(block, "interval_edit") else "10"
            }

            # 조건 저장 (이름 + 설정값)
            for condition in block.conditions:
                condition_data = {
                    "이름": condition.obj_name,
                    "설정값": {key: getattr(condition, key) for key in condition.config_fields}
                }
                block_data["조건"].append(condition_data)

            # 액션 저장 (이름 + 설정값)
            if block.action:
                block_data["액션"] = {
                    "이름": block.action.obj_name,
                    "설정값": {key: getattr(block.action, key) for key in block.action.config_fields}
                }

            strategy_data.append(block_data)

        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(strategy_data, f, ensure_ascii=False, indent=4)

        print(f"{strategy_name} 전략이 저장되었습니다.")





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