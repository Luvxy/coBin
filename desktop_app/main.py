import sys
import requests
import json
from PySide6 import QtCore
from PySide6.QtCore import (Qt, QByteArray, QEvent)
from PySide6.QtGui import (QColor, QMovie)
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import *
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument
from ui.ui_login import Ui_login
from ui.ui_main import Ui_MainWindow
from ui.ui_small_window import UI_SmallWindow
from ui.ui_block import *
from upbit.get_data_upbit import *
from upbit.configer import *
from upbit.api_upbit import *
import os
import shutil
from pyqtgraph import PlotWidget, plot, ViewBox
import pyqtgraph as pg
import psutil
import asyncio
import websockets

SURVER_URL = "127.0.0.1:8000"

def set_global_stylesheet(app):
    """QApplication에 글로벌 스타일시트 설정"""
    app.setStyleSheet("""
        QMessageBox {
            background-color: #2E3440;  /* 배경색 */
            color: #ECEFF4;  /* 텍스트 색상 */
            border: 1px solid #4C566A;  /* 테두리 */
            border-radius: 10px;  /* 모서리 둥글게 */
        }
        QMessageBox QLabel {
            color: #ECEFF4;  /* 라벨 텍스트 색상 */
            font-size: 14px;  /* 라벨 글꼴 크기 */
        }
        QMessageBox QPushButton {
            background-color: #81A1C1;  /* 버튼 배경색 */
            color: #2E3440;  /* 버튼 텍스트 색상 */
            border: none;
            border-radius: 5px;  /* 모서리 둥글게 */
            padding: 8px 12px;  /* 내부 여백 */
        }
        QMessageBox QPushButton:hover {
            background-color: #5E81AC;  /* 호버 시 배경색 */
        }
        QMessageBox QPushButton:pressed {
            background-color: #4C566A;  /* 클릭 시 배경색 */
        }
    """)

def is_already_running():
    """현재 디렉토리에 'cobin.exe' 이름의 실행 파일이 2개 이상 실행 중인지 확인"""
    current_pid = os.getpid()
    current_executable = os.path.basename(sys.executable)  # 현재 실행 파일 이름

    # 'cobin.exe' 이름의 실행 파일 개수 확인
    count = 0
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == "cobin.exe":
                count += 1
                # 현재 프로세스는 제외
                if proc.info['pid'] == current_pid:
                    count -= 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # 'cobin.exe'가 2개 이상 실행 중이면 True 반환
    print(f"[INFO] 현재 실행 중인 'cobin.exe' 개수: {count}")
    return count >= 2

def resource_path(relative_path):
    """ PyInstaller 실행 파일에서도 리소스 경로를 찾을 수 있도록 설정 """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)  # PyInstaller 실행 환경
    return os.path.join(os.path.dirname(__file__), relative_path)

def ensure_json_exists():
    """ JSON 파일이 실행 폴더에 없으면 자동 복사 """
    json_filename = "default.json"
    source_path = resource_path(json_filename)  # PyInstaller 내 경로 또는 현재 경로
    dest_path = os.path.join(os.getcwd(), json_filename)  # 실행 폴더에 저장

    if not os.path.exists(dest_path):  # 실행 폴더에 JSON이 없으면 복사
        try:
            shutil.copy(source_path, dest_path)
            print(f"{json_filename}을(를) 실행 폴더로 복사했습니다.")
        except Exception as e:
            print(f"JSON 복사 실패: {e}")

    return dest_path  # ✅ 항상 실행 폴더에서 JSON을 사용하도록 경로 반환

class WebSocketThread(QThread):
    message_received = Signal(dict)  # WebSocket 메시지를 전달하기 위한 Signal

    def __init__(self, user_id, url):
        super().__init__()
        self.user_id = user_id
        self.url = url
        self.running = True  # WebSocket 루프 실행 상태

    async def websocket_loop(self):
        try:
            async with websockets.connect(self.url) as websocket:
                while self.running:
                    message = await websocket.recv()
                    print("Received update:", message)
                    data = json.loads(message)  # JSON 메시지 파싱
                    self.message_received.emit(data)  # 메시지를 Signal로 전달
        except Exception as e:
            print(f"WebSocket 연결 오류: {e}")

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.websocket_loop())

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

class CustomViewBox(ViewBox):
    """x축으로만 움직일 수 있도록 제한하고 줌 기능 제거"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseDragEvent(self, ev, axis=None):
        """마우스 드래그 이벤트를 x축으로만 제한"""
        if axis is None or axis == 0:  # x축으로만 움직임 허용
            super().mouseDragEvent(ev, axis=0)
        else:
            ev.ignore()

    def mouseClickEvent(self, ev):
        """마우스 클릭 이벤트 처리"""
        super().mouseClickEvent(ev)

    def mouseWheelEvent(self, ev):
        """마우스 휠 이벤트 비활성화 (줌 제거)"""
        ev.ignore()  # 모든 줌 동작 비활성화

class User():
    def __init__(self, username, password):
        self.username = username
    
    # firebase에 활동 로그 저장
    def save_log(self, log):
        pass
    
    # firebase에 활동 로그 조회
    def load_log(self):
        pass

class PdfViewer(QMainWindow):
    def __init__(self, pdf_path, x=100, y=100, width=1400, height=800):
        super().__init__()

        self.setWindowTitle("PDF 도움말")
        self.setGeometry(x, y, width, height) 

        # PDF 뷰어 설정
        self.pdf_view = QPdfView(self)
        self.pdf_doc = QPdfDocument(self)
        self.pdf_doc.load(pdf_path)
        self.pdf_view.setDocument(self.pdf_doc)

        # 📌 전체 페이지 스크롤 가능하도록 설정
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)

        # 📌 기본 줌 크기 설정
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.Custom)
        self.pdf_view.setZoomFactor(0.7)  # 기본 100% 배율

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.pdf_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

class SmallWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = UI_SmallWindow()  # ui_small_window의 UI 클래스 사용
        self.ui.setupUi(self)  # UI 초기화

    def closeEvent(self, event):
        """작은 창이 닫힐 때 메인 UI를 다시 표시"""
        if self.parent():  # 부모(MainWindow)가 있는 경우
            self.parent().show()  # 부모(MainWindow)를 다시 표시
            self.parent().blockFrame.history = self.parent().ui.history  # 부모의 history와 연결
        super().closeEvent(event)  # 기본 closeEvent 호출
        
    def changeEvent(self, event):
        """창 상태 변경 이벤트 처리"""
        if event.type() == QEvent.WindowStateChange:
            print(f"현재 창 상태: {self.windowState()}")
            if self.windowState() == Qt.WindowMaximized:  # 창이 전체화면 상태로 전환되었을 때
                if self.parent():  # 부모(MainWindow)가 있는 경우
                    self.close()  # 작은 창 닫기
                    self.parent().show()  # 부모(MainWindow)를  다시 표시
            elif self.windowState() == Qt.WindowMinimized:  # 최소화 상태일 경우
                event.ignore()  # 아무 작업도 하지 않음
        super().changeEvent(event)

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)  # ✅ 항상 위에 표시
        self.setAttribute(Qt.WA_TranslucentBackground)  # ✅ 배경 투명
        self.setFixedSize(50, 50)  # ✅ 크기 조정 가능 (GIF 크기에 맞게 변경 가능)

        # ✅ GIF 파일 경로 설정
        gif_path = os.path.join(os.path.dirname(__file__), "resources", "loading.gif")

        # ✅ QLabel 설정
        self.label = QLabel(self)
        self.movie = QMovie(gif_path, QByteArray(), self)
        self.label.setMovie(self.movie)
        self.movie.setCacheMode(QMovie.CacheAll)  # ✅ GIF를 미리 로드
        self.show()
        self.movie.start() 

        # ✅ GIF를 중앙 정렬
        self.setup_layout()

    def show_loading(self):
        self.show()
        QApplication.processEvents()  # ✅ UI 업데이트 강제 실행

    def hide_loading(self):
        self.hide()
        self.close()

    def setup_layout(self):
        layout = QVBoxLayout(self)
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        h_layout.addStretch()

        layout.addStretch()
        layout.addLayout(h_layout)
        layout.addStretch()

# 메인 윈도우 클래스
class MainWindow(QMainWindow):
    def __init__(self, token, id, password):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # UI 초기화
        self.token = token
        self.id = id
        self.password = password
        
        # WebSocketThread 초기화
        self.websocket_thread = WebSocketThread(
            user_id=self.id,
            url=f"ws://{SURVER_URL}/ws/points/{self.id}/"
        )
        self.websocket_thread.message_received.connect(self.update_points)  # 메시지 수신 시 UI 업데이트
        self.websocket_thread.start()  # WebSocketThread 시작
        
        # 타이틀바 숨기기
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 모든 테두리 제거

        # ✅ 화면 크기 설정
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)  # 전체 화면 크기로 설정
        self.showMaximized()  # 창을 최대화하여 화면에 맞춤

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

        # ✅ Upbit API 초기화
        self.upbit = Upbit_api(self.access_key, self.secret_key, self.id, self.password)
        self.upbit.create_user()

        # UI 초기화 및 신호 연결
        self.setup_ui()
        self.setup_signals()
        self.preload_tab2_data()
        self.open_patchnote()    

    def update_points(self, data):
        """WebSocket 메시지를 수신하여 UI를 업데이트"""
        point1 = data.get("point1", 0)
        point2 = data.get("point2", 0)
        self.ui.label_9.setText(f"금화: {point1}")
        self.ui.label_10.setText(f"은화: {point2}")
        
    def closeEvent(self, event):
        """창 닫기 이벤트에서 WebSocketThread 종료"""
        self.websocket_thread.stop()
        super().closeEvent(event)

    def setup_ui(self):
        """UI 초기화"""
        self.setup_tab1()
        self.setup_tab2()
        
        self.ui.minimize_button.clicked.connect(self.show_small_window)  # 버튼 클릭 시 동작 연결
        
        # 유저 정보 불러오기
        user_data = self.fetch_user_info()
        
        # point1 = free, point2 = paid
        self.blockFrame.point['point1'] = user_data.get('point1', 0) or 0
        self.blockFrame.point['point2'] = user_data.get('point2', 0) or 0
        
        self.ui.label_9.setText(f"금화: {user_data['point1']}")
        self.ui.label_10.setText(f"은화: {user_data['point2']}")
        points = user_data['point1'] + user_data['point2']
        self.ui.label_11.setText(f"남은 시간: {self.blockFrame.point_to_time(points)}")

    def setup_signals(self):
        """신호 연결"""
        self.ui.save_button.clicked.connect(self.save_api)
        self.ui.start_button.clicked.connect(lambda: self.blockFrame.run_all_blocks(self.ui.strategy_combo_2.currentText()))
        self.ui.stop_button.clicked.connect(self.blockFrame.stop_all_blocks)
        self.ui.coin_selete.currentIndexChanged.connect(self.update_chart)
        self.ui.coin_selete_2.currentIndexChanged.connect(self.update_chart)
        self.ui.coin_selete_3.currentIndexChanged.connect(self.update_chart)
        self.ui.buy_button.clicked.connect(self.buy_market_order)
        self.ui.buy_button_2.clicked.connect(self.sell_market_order)
        self.ui.strategy_combo.currentIndexChanged.connect(self.load_strategy)
        self.ui.start_button_2.clicked.connect(self.save_custom_strategy)
        self.ui.clear_button.clicked.connect(self.blockFrame.clear_blocks)
        self.ui.pushButton_2.clicked.connect(self.open_pdf_viewer)
        self.ui.back_start.clicked.connect(self.backtest)  # 백테스트 실행 버튼
        self.ui.back_result.clicked.connect(self.display_backtest_results)  # 결과 표시 버튼
        self.ui.strategy_combo.addItems(["기본전략","custom1", "custom2", "custom3", "custom4", "custom5"])
        self.ui.back_count.addItems(["20", "30", "50", "100", "200", "500"])
        self.ui.back_time.addItems(["1분", "3분", "5분", "15분", "30분", "1시간"])

    def setup_tab1(self):
        """Tab1 초기화 (그래프 복구)"""
        # ✅ ChartWidget 추가
        self.chart = ChartWidget(coin="KRW-BTC")
        self.chart_layout = QVBoxLayout(self.ui.chart)  # self.ui.chart는 QFrame 또는 QWidget
        self.chart_layout.addWidget(self.chart)

        # ✅ Order Book 추가
        self.order = OrderBookWidget()
        self.order.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.order_layout = QVBoxLayout(self.ui.groupBox_4)  # self.ui.groupBox_4는 Order Book 영역
        self.order_layout.addWidget(self.order)
        self.order_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
        self.order_layout.setStretch(0, 1)  # Order Book이 최대한 확장되도록 설정

        # ✅ 거래량 차트 추가 (pyqtgraph 사용)
        self.graph_widget = PlotWidget(viewBox=CustomViewBox())  # CustomViewBox 사용
        self.graph_widget.setBackground('#2E3440')  # 배경색 설정
        self.graph_widget.showGrid(x=False, y=False)  # 격자 비활성화
        self.graph_widget.setLabel('left', 'Volume', color='#ECEFF4', size='12pt')  # Y축 라벨
        self.graph_widget.setLabel('bottom', 'Time', color='#ECEFF4', size='12pt')  # X축 라벨
        self.graph_widget.getAxis('left').setPen(pg.mkPen(color='#ECEFF4', width=1.5))  # Y축 색상 및 두께
        self.graph_widget.getAxis('bottom').setPen(pg.mkPen(color='#ECEFF4', width=1.5))  # X축 색상 및 두께
        self.graph_widget.getAxis('left').setStyle(tickTextOffset=10, tickFont=pg.QtGui.QFont("Arial", 12))  # Y축 폰트
        self.graph_widget.getAxis('bottom').setStyle(tickTextOffset=10, tickFont=pg.QtGui.QFont("Arial", 12))  # X축 폰트
        self.graph_widget.setMouseEnabled(x=False, y=False)  # 마우스 줌/팬 비활성화

        self.ui.coin_selete.addItems(["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-DOGE"])
        self.ui.strategy_combo_2.addItems(["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-DOGE"])
        self.graph_layout = QVBoxLayout(self.ui.graph)
        self.graph_layout.addWidget(self.graph_widget)

        # 초기 차트 로드
        self.current_coin = "KRW-BTC"
        self.update_main()
        self.update_chart()

    def setup_tab2(self):
        """Tab2 초기화"""
        self.blockFrame = BlockMain(self.upbit)
        self.ui.pushButton.clicked.connect(self.blockFrame.add_block)
        self.ui.verticalLayout.addWidget(self.blockFrame)
        self.blockFrame.history = self.ui.history
        self.blockFrame.point1 = self.ui.label_9
        self.blockFrame.point2 = self.ui.label_10
        self.blockFrame.remain_time = self.ui.label_11
        
    def show_small_window(self):
        """메인 UI를 숨기고 작은 창을 띄움"""
        self.hide()  # 메인 UI 숨기기
        self.small_window = SmallWindow(self)  # 작은 창 생성

        # 작은 창의 콤보박스와 메인 창의 콤보박스를 연결
        self.small_window.ui.strategy_combo.currentIndexChanged.connect(
            self.ui.strategy_combo.setCurrentIndex
        )
        self.ui.strategy_combo.currentIndexChanged.connect(
            self.small_window.ui.strategy_combo.setCurrentIndex
        )

        self.small_window.ui.strategy_combo_2.currentIndexChanged.connect(
            self.ui.strategy_combo_2.setCurrentIndex
        )
        self.ui.strategy_combo_2.currentIndexChanged.connect(
            self.small_window.ui.strategy_combo_2.setCurrentIndex
        )
        
        self.small_window.ui.strategy_combo_2.addItems(["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-DOGE"])
        self.small_window.ui.strategy_combo.addItems(["기본전략","custom1", "custom2", "custom3", "custom4", "custom5"])

        # 작은 창의 다른 UI 요소와 메인 창의 요소 연결
        self.small_window.ui.label_9.setText(self.ui.label_9.text())
        self.small_window.ui.label_10.setText(self.ui.label_10.text())
        self.small_window.ui.label_11.setText(self.ui.label_11.text())

        self.blockFrame.history = self.small_window.ui.history

        # 작은 창의 버튼과 메인 창의 버튼 동작 연결
        self.small_window.ui.start_button.clicked.connect(
            lambda: self.blockFrame.run_all_blocks(self.ui.strategy_combo_2.currentText())
        )
        self.small_window.ui.stop_button.clicked.connect(self.blockFrame.stop_all_blocks)


        self.small_window.show()
    
    def preload_tab2_data(self):
        """tab2에서 필요한 데이터를 미리 로드"""
        print("tab2 데이터를 미리 로드 중...")
        self.blockFrame.add_block()  # 예시: 블록 추가
        self.load_custom_strategy("default")  # 기본 전략 로드
        print("tab2 데이터 로드 완료.")

    def fetch_user_info(self):
        """Django 서버로 요청을 보내 유저 정보를 가져옵니다."""
        url = f"http://{SURVER_URL}/api/user/{self.id}"  # Django 서버의 API URL
        headers = {
            "Authorization": f"Bearer {self.token}"  # JWT 토큰을 헤더에 포함
        }
        
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"HTTP 요청 실패: {e}")
            return {"point1": 99999, "point2": 99999}  # 기본값 반환

        if response.status_code == 200:
            result = response.json()
            user_data = result.get('user_data', {})
            return {
                "point1": user_data.get("point1", 0) or 0,  # None일 경우 0으로 설정
                "point2": user_data.get("point2", 0) or 0   # None일 경우 0으로 설정
            }
        else:
            print("유저 정보 요청 실패:", response.status_code, response.text)
            return {"point1": 0, "point2": 0}  # 기본값 반환
    
    def update_chart(self):
        """차트 업데이트"""
        # ✅ 로딩 화면 표시
        self.loading_screen = LoadingDialog()
        self.loading_screen.show_loading()

        try:
            new_coin = self.ui.coin_selete.currentText()
            if new_coin == "선택":
                new_coin = "KRW-BTC"

            interval = self.ui.coin_selete_2.currentText()
            count = int(self.ui.coin_selete_3.currentText())

            interval_mapping = {
                "1분": "minute1",
                "3분": "minute3",
                "5분": "minute5",
                "15분": "minute15",
                "30분": "minute30",
                "1시간": "minute60"
            }
            interval = interval_mapping.get(interval, "minute30")

            self.chart.change_coin(new_coin, interval, count)
            self.order.change_coin(new_coin)

            # ✅ 차트 데이터 로드
            df = pyupbit.get_ohlcv(new_coin, interval=interval, count=count)
            if df is None or df.empty:
                self.loading_screen.hide_loading()
                QMessageBox.warning(self, "데이터 로드 실패", f"{new_coin}의 데이터를 불러오지 못했습니다.")
                return

            self.update_main()
            
            df['time'] = df.index
            self.graph_widget.clear()  # 기존 데이터 삭제
            self.graph_widget.plot(df['time'], df['volume'], pen=pg.mkPen(color='#81A1C1', width=2.5))  # 거래량 차트

        except Exception as e:
            print(e)
            QMessageBox.critical(self, "오류", f"차트 업데이트 중 오류가 발생했습니다: {e}")

        finally:
            # ✅ 로딩 화면 종료
            self.loading_screen.hide_loading()
            
    # 메인화면 정보 업데이트
    def update_main(self):
        """메인 화면 정보 업데이트"""
        # Upbit API 요청 테스트
        test = self.upbit.get_balances()
        if not test or isinstance(test, dict) and test.get("error"):
            # API 요청 실패 시 에러 메시지 표시 및 종료
            return
        
        
        ticker = self.ui.coin_selete.currentText()  # 선택된 코인
        self.blance = self.upbit.get_balance(ticker) or 0.0  # 보유 코인 수량 (None일 경우 0.0으로 설정)
        current_price = self.upbit.get_current_price(ticker) or 0.0  # 현재가 (None일 경우 0.0으로 설정)
        krw_balance = self.upbit.get_balance("KRW") or 0.0  # 보유 원화 (None일 경우 0.0으로 설정)
        avg_buy_price = self.upbit.get_avg_buy_price(ticker) or 0.0  # 매수 평단가 (None일 경우 0.0으로 설정)

        # 보유 KRW 계산: volume * 현재가 + KRW
        total_krw = (self.blance * current_price) + krw_balance

        # UI 업데이트
        # 보유량 소수점 8자리까지 표시
        self.ui.label_3.setText(f"보유량: {self.blance:.8f}")
        self.ui.label_6.setText(f"보유현금: {krw_balance:.0f}원")
        self.ui.label_7.setText(f"총 보유 KRW: {total_krw:.0f}")  # 총 보유 KRW 표시

        # 수익률 계산
        if self.blance > 0 and avg_buy_price > 0:  # 보유량과 매수 평단가가 있을 경우에만 계산
            profit_rate = ((current_price - avg_buy_price) / avg_buy_price) * 100

            # 수익률 텍스트 생성 (HTML 사용)
            if profit_rate > 0:
                profit_text = f"수익률: <span style='color: blue;'>{profit_rate:.2f}%</span>"
            else:
                profit_text = f"수익률: <span style='color: red;'>{profit_rate:.2f}%</span>"

            self.ui.label_8.setText(profit_text)  # HTML 텍스트 설정
        else:
            self.ui.label_8.setText("수익률: N/A")  # 보유량이 없을 경우 표시
    
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
        
        self.upbit = Upbit_api(self.access_key, self.secret_key, self.id, self.password)
        
        self.upbit.create_user()
        if self.upbit.user is None:
            QMessageBox.critical(self, 'API 연결 실패', 'API 키가 올바르지 않습니다.')

        if self.blockFrame:
            self.blockFrame.update_upbit(self.upbit)
        
        self.update_main()
        
    def buy_market_order(self):
        """시장가 매수"""
        ticker = self.ui.coin_selete.currentText()
        current_krw_balance = self.upbit.get_balance("KRW")  # 현재 보유 원화

        input_value = self.ui.direct_input_2.text().strip()  # 입력값 가져오기
        if input_value.endswith('%'):  # 입력값이 퍼센트인지 확인
            percent = int(input_value.rstrip('%'))  # '%' 제거 후 정수로 변환
            cash = (current_krw_balance * percent / 100) * 0.9995  # 수수료 0.05% 적용
        else:
            cash = int(input_value) * 0.9995  # 입력된 금액 사용

        if cash > current_krw_balance:
            QMessageBox.warning(self, "잔액 부족", "보유 원화가 부족합니다.")
            return

        self.upbit.buy_market_order(ticker, cash)  # 매수 실행
        QMessageBox.information(self, '매수 주문', '주문이 완료되었습니다.')
        self.update_main()
    
    def sell_market_order(self):
        """시장가 매도"""
        ticker = self.ui.coin_selete.currentText()
        current_volume = self.upbit.get_balance(ticker)  # 현재 보유 코인 수량

        input_value = self.ui.direct_input_2.text().strip()  # 입력값 가져오기
        if input_value.endswith('%'):  # 입력값이 퍼센트인지 확인
            percent = int(input_value.rstrip('%'))  # '%' 제거 후 정수로 변환
            volume = current_volume * percent / 100  # 퍼센트만큼 매도
        else:
            volume = float(input_value)  # 입력된 수량 사용

        if volume > current_volume:
            QMessageBox.warning(self, "잔량 부족", "보유 코인이 부족합니다.")
            return

        # 소수점 자리수 제한 (Upbit는 최대 8자리까지 허용)
        volume = round(volume, 8)
        
        self.upbit.sell_market_order(ticker, volume)  # 매도 실행
        QMessageBox.information(self, '매도 주문', '주문이 완료되었습니다.')
        self.update_main()
        
    def load_custom_strategy(self, strategy_name):
        """ JSON 파일에서 Custom 전략 불러오기 """
        file_name = f"{strategy_name.lower().replace(' ', '')}.json"
        file_path = os.path.join(os.getcwd(), file_name)  # ✅ 실행 폴더에서 JSON 로드

        try:
            if not os.path.exists(file_path):
                QMessageBox.warning(self, "파일 없음", f"{file_path} 파일이 존재하지 않습니다.")
                self.blockFrame.clear_blocks()
                return

            with open(file_path, "r", encoding="utf-8") as f:
                strategy_data = json.load(f)

        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "JSON 오류", f"JSON 파일을 읽는 중 오류가 발생했습니다: {e}")
            self.blockFrame.clear_blocks()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"전략 로드 중 알 수 없는 오류가 발생했습니다: {e}")
            self.blockFrame.clear_blocks()

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
    
    def load_strategy(self):
        """ 기본 전략 불러오기 """
        self.blockFrame.clear_blocks()
        strategy_name = self.ui.strategy_combo.currentText()

        if strategy_name == "기본전략":
            self.load_custom_strategy("default")
        else:
            self.load_custom_strategy(strategy_name)

    def save_custom_strategy(self):
        """ 현재 블록 상태를 JSON 파일로 저장 """        
        strategy_name = self.ui.strategy_combo.currentText()
        
        if strategy_name == "기본전략":
            strategy_name = "default"

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

        QMessageBox.information(self, '저장', f'{strategy_name} 전략이 저장되었습니다.')

    def open_pdf_viewer(self):
        viewer_path = os.path.join(os.path.dirname(__file__), "resources", "프로그램 설명서.pdf")
        self.viewer = PdfViewer(viewer_path)  # PDF 파일 경로 설정
        self.viewer.show()
        
    def open_patchnote(self):
        viewer_path = os.path.join(os.path.dirname(__file__), "resources", "패치노트.pdf")
        self.viewer = PdfViewer(viewer_path, width=880, height=650)  # PDF 파일 경로 설정
        self.viewer.show()

    ###################################################################################
    # 백테스트
    ###################################################################################
    def backtest(self):
        """백테스트 실행"""
        coin = self.ui.strategy_combo_2.currentText()
        interval = self.ui.back_time.currentText()
        count = int(self.ui.back_count.currentText())        
        initial_balance = 1000000  # 초기 자본 (100만원)
        
        # interval 매핑
        interval_mapping = {
            "1분": "minute1",
            "3분": "minute3",
            "5분": "minute5",
            "15분": "minute15",
            "30분": "minute30",
            "1시간": "minute60"
        }
        interval = interval_mapping.get(interval, "minute30")

        # 백테스트 실행
        results = self.blockFrame.run_backtest(coin, interval, count, initial_balance)

        # 결과 저장
        result_file = f"{coin}_backtest_results.json"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
    
    def display_backtest_results(self):
        """backtest_logs.json 파일을 자동으로 불러와 결과를 표시"""
        file_name = "backtest_logs.json"  # 파일 이름 고정
        if not os.path.exists(file_name):
            QMessageBox.warning(self, "파일 없음", f"{file_name} 파일이 존재하지 않습니다.")
            return

        try:
            with open(file_name, "r", encoding="utf-8") as f:
                logs = json.load(f)  # JSON 파일 읽기

            # 파일 내용 확인 및 결과 추출
            start_message = next((log for log in logs if "백테스트 시작" in log), None)
            end_message = next((log for log in logs if "백테스트 완료" in log), None)

            if not start_message or not end_message:
                QMessageBox.warning(self, "결과 없음", "백테스트 결과를 찾을 수 없습니다.")
                return

            # 결과 메시지 파싱
            try:
                # 백테스트 시작 정보
                start_details = start_message.split(":")[1].strip().split(", ")
                coin = start_details[0] if len(start_details) > 0 else "알 수 없음"
                data_count = start_details[1].split(" ")[1] if len(start_details) > 1 else "알 수 없음"
                interval = start_details[2].split(" ")[1] if len(start_details) > 2 else "알 수 없음"

                # 백테스트 완료 정보
                end_details = end_message.split(". ")[1].split(", ") if ". " in end_message else []
                final_balance = end_details[0].split(": ")[1] if len(end_details) > 0 else "알 수 없음"
                win_rate = end_details[1].split(": ")[1] if len(end_details) > 1 else "알 수 없음"

                # 매수/매도 성공 로그 추출
                trade_logs = [
                    log for log in logs
                    if "매수 성공" in log or "매도 성공" in log
                ]

                # 결과 텍스트 생성
                result_text = (
                    f"<b>코인:</b> {coin}<br>"
                    f"<b>데이터 개수:</b> {data_count}<br>"
                    f"<b>간격:</b> {interval}<br>"
                    f"<b>최종 잔액:</b> {final_balance}<br>"
                    f"<b>승률:</b> {win_rate}<br><br>"
                    f"<b>거래 내역:</b><br>"
                )
                for trade_log in trade_logs:
                    result_text += f"{trade_log}<br>"

            except (IndexError, AttributeError) as e:
                QMessageBox.critical(self, "오류", f"백테스트 결과를 파싱하는 중 오류가 발생했습니다: {e}")
                return

            # 새 창에 결과 표시
            result_window = QDialog(self)
            result_window.setWindowTitle("백테스트 결과")
            result_window.setFixedSize(600, 400)
            result_window.setStyleSheet("""
                QDialog {
                    background-color: #2E3440;  /* 배경색 */
                    color: #ECEFF4;  /* 텍스트 색상 */
                    border: 1px solid #4C566A;  /* 테두리 */
                    border-radius: 10px;  /* 모서리 둥글게 */
                }
                QLabel {
                    color: #ECEFF4;  /* 라벨 텍스트 색상 */
                    font-size: 14px;  /* 라벨 글꼴 크기 */
                }
            """)

            layout = QVBoxLayout(result_window)
            result_label = QLabel(result_text)
            result_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            result_label.setWordWrap(True)
            result_label.setTextFormat(Qt.RichText)  # HTML 형식 지원
            layout.addWidget(result_label)

            close_button = QPushButton("닫기")
            close_button.setStyleSheet("""
                QPushButton {
                    background-color: #81A1C1;  /* 버튼 배경색 */
                    color: #2E3440;  /* 버튼 텍스트 색상 */
                    border: none;
                    border-radius: 5px;  /* 모서리 둥글게 */
                    padding: 8px 12px;  /* 내부 여백 */
                }
                QPushButton:hover {
                    background-color: #5E81AC;  /* 호버 시 배경색 */
                }
                QPushButton:pressed {
                    background-color: #4C566A;  /* 클릭 시 배경색 */
                }
            """)
            close_button.clicked.connect(result_window.close)
            layout.addWidget(close_button, alignment=Qt.AlignCenter)

            result_window.exec_()
        except json.JSONDecodeError:
            QMessageBox.critical(self, "오류", "백테스트 로그 파일이 올바른 JSON 형식이 아닙니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"백테스트 결과를 불러오는 중 오류가 발생했습니다: {e}")
    
    
# 로그인 윈도우 클래스
class SpleshScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_login()
        self.ui.setupUi(self)
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.frame.setGraphicsEffect(self.shadow)
        
        self.show()
        
        self.ui.pushButton.clicked.connect(self.login_button_clicked)
    
    def login_button_clicked(self):
        url = f'http://{SURVER_URL}/api/token/'
        
        payload = {
            'username': self.ui.user_id.text(),
            'password': self.ui.user_password.text(),
        }
        
        try:
            response = requests.post(url, json=payload)
        except requests.exceptions.RequestException as e:
            print(f"HTTP 요청 오류: {e}")
            return None
        
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens['access']
            print("Access Token:", access_token)

            # 보호된 API에 접근
            headers = {'Authorization': f'Bearer {access_token}'}
            api_response = requests.get(f'http://{SURVER_URL}/protected-api/', headers=headers)

            if api_response.status_code == 200:
                print("성공적으로 접근:", api_response.json())
                self.main = MainWindow(access_token, self.ui.user_id.text(), self.ui.user_password.text())
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
        
        
def login_button_clicked(id, password):
    """로그인 요청을 보내고 JWT 토큰을 반환합니다."""
    url = 'http://127.0.0.1:8000/api/token/'
    
    payload = {
        'username': id,
        'password': password,
    }
    
    try:
        response = requests.post(url, data=payload)  # data를 사용
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 오류: {e}")
        return None

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access']
        return access_token
    else:
        print("로그인 실패:", response.json())
        return None
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_global_stylesheet(app)  # 글로벌 스타일시트 설정
    if is_already_running():
        # 메세지 박스로 이미 실행 중임을 알림
        print("[INFO] 이미 실행 중인 프로그램이 있습니다.")
        QMessageBox.critical(None, "오류", "이미 실행 중인 프로그램이 있습니다.")
        sys.exit(0)
    # window = SpleshScreen()
    # window.show()
    # window = LoadingScreen()
    token = login_button_clicked("brunch", "qaz4455!")
    window = MainWindow(token, "brunch", "qaz4455!")
    window.show()
    
    sys.exit(app.exec())