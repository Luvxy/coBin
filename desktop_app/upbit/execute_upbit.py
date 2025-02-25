import pyupbit
from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt, QMimeData)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient, QDrag)
from PySide6.QtWidgets import *

class UpbitTradeOrder:
    def __init__(self, upbit_api, user):
        self.api = upbit_api
        self.upbit = pyupbit.Upbit(self.api.access_key, self.api.secret_key)
        self.user = user
    
    def get_all_coins(self):
        return pyupbit.get_tickers(fiat="KRW")
            
class StrategySettingArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 스크롤 설정
        self.setWidgetResizable(True)

        # 내부 컨테이너 위젯 (스크롤 영역 내에서 레이아웃 배치)
        self.container = QWidget()
        self.setWidget(self.container)

        # 내부 레이아웃
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(15)

        # 최소 크기 설정으로 스크롤바 생성 유도
        self.container.setMinimumHeight(400)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        text = event.mimeData().text()
        block_type = event.mimeData().data("block_type").data().decode()

        # 블록 타입에 맞춰 새로운 객체 생성
        if block_type == "RateBlock":
            new_block = RateBlock(text, is_draggable=False)
        elif block_type == "ConditionBlock":
            new_block = ConditionBlock(text, is_draggable=False)
        else:
            new_block = BaseBlock(text, is_draggable=False)

        self.layout.addWidget(new_block)
        self.update_container_height()
        event.acceptProposedAction()

    def update_container_height(self):
        # 블록이 추가될 때마다 컨테이너의 최소 높이를 업데이트
        total_height = sum(
            self.layout.itemAt(i).widget().sizeHint().height() + self.layout.spacing()
            for i in range(self.layout.count())
        ) + 20  # 여유 공간

        self.container.setMinimumHeight(total_height)

    def run_all_blocks(self):
        print("=== 블록 순차 실행 시작 ===")
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            # 모든 BaseBlock 기반 클래스 실행
            if isinstance(widget, BaseBlock):
                widget.execute_block()
        print("=== 블록 순차 실행 종료 ===")
        

#######################################################
        

class BaseBlock(QWidget):
    """
    블록의 공통 동작:
    - 드래그 가능 여부 (is_draggable)
    - 삭제 버튼
    - 실행 버튼
    """
    def __init__(self, text, is_draggable=True):
        super().__init__()
        self.is_draggable = is_draggable

        # 스타일
        self.setStyleSheet("""
            QWidget {
                background-color: #ced4da;
                border: 1px solid black;
                border-radius: 5px;
            }
            QLabel {
                font-size: 12px;
                padding: 2px;
            }
            QLineEdit {
                padding: 4px;
                font-size: 12px;
            }
            QComboBox {
                padding: 4px;
                font-size: 12px;
            }
            QPushButton {
                padding: 4px;
                font-size: 12px;
            }
        """)
        self.setMinimumHeight(100)

        # 메인 레이아웃
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # 블록 제목
        self.label = QLabel(text)
        self.layout.addWidget(self.label)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()

        # 삭제 버튼
        self.delete_button = QPushButton("삭제")
        self.delete_button.clicked.connect(self.delete_block)
        # 드래그되어 온 블록만 삭제 버튼 노출
        if not self.is_draggable:
            button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)

    def mousePressEvent(self, event):
        if self.is_draggable and event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            
            # 블록 텍스트 + 블록 타입 정보를 함께 저장
            mime_data.setText(self.label.text())
            mime_data.setData("block_type", self.__class__.__name__.encode())  # 클래스 이름 추가

            drag.setMimeData(mime_data)
            drag.exec(Qt.MoveAction)

    def execute_block(self):
        """ 블록 실행 로직 (자식 클래스에서 오버라이딩 가능) """
        print(f"[BaseBlock] 실행: {self.label.text()}")

    def delete_block(self):
        """ 블록 삭제 (공통 기능) """
        self.setParent(None)
        self.deleteLater()
        

class ConditionBlock(BaseBlock):
    """
    조건을 체크하는 블록
    """
    def __init__(self, text="조건 블록", is_draggable=True):
        super().__init__(text, is_draggable)

        # BaseBlock에서 이미 실행/삭제 버튼 존재
        # 여기서 '조건' 입력창만 추가
        self.condition_input = QLineEdit()
        self.condition_input.setPlaceholderText("조건을 입력하세요 (예: 수익률>5%)")
        self.layout.insertWidget(1, self.condition_input) 

    def execute_block(self):
        """ 조건 블록 실행 로직 """
        condition_str = self.condition_input.text()
        print(f"[ConditionBlock] 실행: {self.label.text()}, 조건 = {condition_str}")
        # 실제 조건 체크 로직은 여기서 구현
        
class ActionBlock(BaseBlock):
    """
    매수/매도 같은 액션을 실행하는 블록
    """
    def __init__(self, text="액션 블록", is_draggable=True):
        super().__init__(text, is_draggable)

        # 액션을 위한 입력
        self.action_input = QLineEdit()
        self.action_input.setPlaceholderText("액션을 입력하세요 (예: 매수, 매도)")
        self.layout.insertWidget(1, self.action_input)

    def execute_block(self):
        """ 액션 블록 실행 로직 """
        action_str = self.action_input.text()
        print(f"[ActionBlock] 실행: {self.label.text()}, 액션 = {action_str}")
        # 매수/매도 API 호출 등
        
class RateBlock(BaseBlock):
    """
    선택 1: '증가' or '감소'  (수익률 condition)
    입력 1: 수익률 % (정수/실수)
    선택 2: '매수' or '매도'
    입력 2: 수량 % (정수/실수)
    """
    def __init__(self, text="수익률 조건+액션 블록", is_draggable=True):
        super().__init__(text, is_draggable)

        # 블록 라벨을 재정의해도 됨
        self.label.setText("수익률 조건/액션 설정")

        # 콤보박스 / 라인에디트를 넣을 레이아웃
        form_layout = QHBoxLayout()

        # (1) 수익률 증가/감소
        self.condition_combo = QComboBox()
        self.condition_combo.addItems(["증가", "감소"])

        # (2) 수익률 퍼센트 입력
        self.condition_rate_input = QLineEdit()
        self.condition_rate_input.setFixedWidth(50)
        self.condition_rate_input.setPlaceholderText("수익률 %")

        # (3) 매수/매도
        self.action_combo = QComboBox()
        self.action_combo.addItems(["매수", "매도"])

        # (4) 수량 퍼센트
        self.action_rate_input = QLineEdit()
        self.action_rate_input.setFixedWidth(50)
        self.action_rate_input.setPlaceholderText("수량 %")

        # 레이아웃 배치
        form_layout.addWidget(QLabel("수익률"))
        form_layout.addWidget(self.condition_combo)
        form_layout.addWidget(self.condition_rate_input)

        form_layout.addSpacing(15)

        form_layout.addWidget(QLabel("액션"))
        form_layout.addWidget(self.action_combo)
        form_layout.addWidget(self.action_rate_input)

        # 버튼 레이아웃 위로 넣기 위해 insertWidget 사용
        self.layout.insertLayout(1, form_layout)

    def execute_block(self):
        """
        블록 실행 시 (예) 
        - 수익률이 X% '증가/감소' 인지 확인
        - 조건 만족 시 '매수/매도' (수량 %) 실행
        """
        condition_type = self.condition_combo.currentText()   # '증가' or '감소'
        condition_rate = self.condition_rate_input.text()     # '5' 등
        action_type = self.action_combo.currentText()         # '매수' or '매도'
        action_rate = self.action_rate_input.text()           # '10' 등

        # 실제 로직 (가상):
        # 1. 현재 수익률 계산
        # 2. condition_type, condition_rate 비교
        # 3. 조건 만족 시 upbit API로 action_type(매수 or 매도) 실행
        #    - 수량 = 현재 보유량 * (action_rate / 100)

        print(f"[RateBlock] 실행!")
        print(f"수익률이 {condition_rate}% {condition_type}일 때, {action_rate}% {action_type} 진행")

        # 예) 현실 로직: 
        # if check_current_rate() >= float(condition_rate):  # 증가
        #     upbit_trade.buy_or_sell(action_type, calc_amount(action_rate))