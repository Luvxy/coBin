import sys
import platform
import requests
import json
from PySide6 import QtCore
from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt, QByteArray, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient, QMovie)
from PySide6.QtWidgets import *
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument
from ui.ui_login import Ui_login
from ui.ui_main import Ui_MainWindow
from ui.ui_block import *
from ui.ui_loading import loading
from upbit.get_data_upbit import *
from upbit.configer import *
from upbit.api_upbit import *
import finplot as fplt
import os
import zipfile
import shutil
import subprocess

# GitHub 저장소 정보
GITHUB_REPO = "luvxy/coBin"  # 변경 필요
LATEST_RELEASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
TOKEN = "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"
DOWNLOAD_PATH = "cobin.exe"
CURRENT_VERSION = "v1.0.5"  # 현재 버전 (매 빌드마다 업데이트 필요)

def get_latest_release():
    """GitHub에서 최신 릴리스 버전 및 다운로드 API URL 가져오기"""
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(LATEST_RELEASE_URL, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        version = data["tag_name"].strip()
        print(f"[DEBUG] 최신 버전: {version}")  # ✅ 디버깅 로그 추가

        for asset in data["assets"]:
            print(f"[DEBUG] Asset Name: {asset['name']}")  # ✅ 릴리스 파일 목록 출력
            print(f"[DEBUG] Asset API URL: {asset['url']}")  # ✅ GitHub API 다운로드 URL

            if asset["name"].endswith(".exe"):  # ✅ .exe 파일 다운로드 가능하도록 수정
                return version, asset["url"]  # ✅ `browser_download_url`이 아니라 `url` 사용
    
    else:
        print(f"API 요청 실패: {response.status_code}, 메시지: {response.text}")
    
    return None, None

def download_update(api_url):
    """GitHub API를 사용하여 업데이트 파일 다운로드"""
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/octet-stream",  # ✅ GitHub에서 직접 다운로드 가능하도록 설정
        "User-Agent": "Mozilla/5.0"
    }

    print(f"[DEBUG] 다운로드 API URL: {api_url}")  # ✅ 디버깅 로그 추가

    response = requests.get(api_url, stream=True, headers=headers)
    print(f"[DEBUG] 다운로드 상태: {response.status_code}")  # ✅ 상태 코드 확인

    if response.status_code == 200:
        with open(DOWNLOAD_PATH, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("[DEBUG] 다운로드 완료 ✅")
        return True

    print(f"[ERROR] 다운로드 실패 ❌ 상태 코드: {response.status_code}, 메시지: {response.text}")
    return False

def install_update():
    """업데이트 파일을 덮어쓰기"""
    exe_path = sys.executable  # 현재 실행 중인 파일 경로

    if os.path.exists(DOWNLOAD_PATH):
        print("업데이트 적용 중...")
        
        # ✅ Windows에서 실행 중인 파일은 바로 덮어쓸 수 없으므로, 새 파일을 실행 후 종료
        new_exe_path = exe_path + ".old"
        os.rename(exe_path, new_exe_path)  # 기존 파일 백업
        shutil.move(DOWNLOAD_PATH, exe_path)  # 새 파일 덮어쓰기

        print("업데이트 완료! 프로그램을 다시 시작합니다.")
        subprocess.Popen([exe_path])
        sys.exit(0)

def check_for_update():
    """현재 버전과 최신 버전을 비교하여 업데이트 수행"""
    latest_version, download_url = get_latest_release()
    
    if latest_version and latest_version != CURRENT_VERSION:
        print(f"새로운 업데이트 발견: {latest_version}")
        if download_update(download_url):
            install_update()
    else:
        print("최신 버전입니다.")

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

from PySide6.QtCore import QThread, Signal

class UpdateThread(QThread):
    update_status = Signal(str)  # UI에 메시지 업데이트
    update_progress = Signal(int)  # 프로그레스 바 업데이트

    def run(self):
        """업데이트 확인 및 실행"""
        latest_version, download_url = get_latest_release()

        if latest_version and latest_version != CURRENT_VERSION:
            self.update_status.emit(f"<strong>업데이트 발견: {latest_version}</strong> 다운로드 중...")
            self.update_progress.emit(20)

            if download_update(download_url):
                self.update_status.emit("<strong>업데이트 완료</strong> 설치 중...")
                self.update_progress.emit(50)

                install_update()

                self.update_status.emit("<strong>업데이트 적용 완료</strong> 프로그램 재시작 중...")
                self.update_progress.emit(100)
                return
        
        self.update_status.emit("<strong>최신 버전입니다.</strong>")
        self.update_progress.emit(100)


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
    def __init__(self, pdf_path):
        super().__init__()

        self.setWindowTitle("PDF 도움말")
        self.setGeometry(100, 100, 1400, 800) 

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
        layout = QVBoxLayout(self)
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        h_layout.addStretch()

        layout.addStretch()
        layout.addLayout(h_layout)
        layout.addStretch()

    def show_loading(self):
        self.show()
        QApplication.processEvents()  # ✅ UI 업데이트 강제 실행

    def hide_loading(self):
        self.hide()
        self.close()
        
# SPLASH SCREEN
class LoadingScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loading()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))

        # ✅ 업데이트 스레드 생성
        self.update_thread = UpdateThread()
        self.update_thread.update_status.connect(self.set_status_text)
        self.update_thread.update_progress.connect(self.update_progress)

        QtCore.QTimer.singleShot(500, lambda: self.set_status_text("<strong>업데이트 확인 중...</strong>"))

        self.show()

        # ✅ 업데이트 스레드 실행
        self.update_thread.start()

    def set_status_text(self, text):
        """로딩 창의 상태 메시지 업데이트"""
        self.ui.label_3.setText(text)
        QApplication.processEvents()  # ✅ UI 업데이트 강제 실행

    def update_progress(self, value):
        """프로그레스 바 값 업데이트"""
        self.ui.progressBar.setValue(value)
        QApplication.processEvents()

    def start_main_window(self):
        """업데이트 완료 후 메인 윈도우 실행"""
        self.main = MainWindow()
        self.main.show()
        self.close()

# 메인 윈도우 클래스
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
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
        # 타이틀바
        ###################
        
        # 타이틀바 숨기기
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
        self.ui.start_button.clicked.connect(lambda: self.blockFrame.run_all_blocks(self.ui.strategy_combo_2.currentText()))
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
        self.ui.pushButton_2.clicked.connect(self.open_pdf_viewer)
        
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
        self.load_custom_strategy("default")

    # 차트 업데이트 함수
    def update_chart(self):
        
        #loading gif
        self.loading_screen = LoadingDialog()
        self.loading_screen.show_loading() 
        
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
        df = pyupbit.get_ohlcv(new_coin, interval=interval, count=count)

        if df is None or df.empty:
            print(f"코인 데이터 로드 실패: {new_coin}")
            return

        df.columns = df.columns.str.lower()
        if not {'open', 'close', 'volume'}.issubset(df.columns):
            print(f"필요한 컬럼이 없음: {df.columns}")
            return

        self.ax1.reset()
        fplt.volume_ocv(df[['open', 'close', 'volume']], ax=self.ax1)
        
        
        # loading gif 종료
        self.loading_screen.hide_loading()
    
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
        file_path = os.path.join(os.getcwd(), file_name)  # ✅ 실행 폴더에서 JSON 로드

        try:
            if not os.path.exists(file_path):
                print(f"파일이 존재하지 않음: {file_path}")
                self.blockFrame.clear_blocks()
                return

            with open(file_path, "r", encoding="utf-8") as f:
                print(f"파일 로드: {file_path}")
                strategy_data = json.load(f)

        except Exception as e:
            print(f"load_custom_strategy() 예외 발생: {e}")
            self.blockFrame.clear_blocks()
            return

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
                self.main = LoadingScreen()
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
    check_for_update()
    app = QApplication(sys.argv)
    # window = SpleshScreen()
    # window.show()
    window = LoadingScreen()
    window.show()
    sys.exit(app.exec())