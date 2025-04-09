import json
import pyupbit
import requests
from PySide6.QtCore import QThread, Signal, QMutex, QWaitCondition, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel,
    QDialog, QDialogButtonBox, QComboBox, QLineEdit, QCheckBox, QHBoxLayout,
    QGroupBox, QMessageBox
)
from PySide6.QtGui import QMovie
from main import LoadingDialog
from ui.actions import *
from ui.conditions import *

SURVER_URL = "127.0.0.1:8000"

from PySide6.QtCore import QThread, Signal


# 백테스트 작업을 수행하는 스레드 클래스

class BacktestWorker(QThread):
    result_signal = Signal(dict)  # 백테스트 결과를 전달하는 시그널
    log_signal = Signal(str)  # 로그 메시지를 전달하는 시그널

    def __init__(self, coin, interval, count, initial_balance, blocks, parent=None):
        super().__init__(parent)
        self.coin = coin
        self.interval = interval
        self.count = count
        self.initial_balance = initial_balance
        self.blocks = blocks
        self.logs = []
        self.buy_price = None  # 매수 가격 초기화

    def run(self):
        try:
            # 초기값 설정
            balance = self.initial_balance
            holdings = 0.0
            wins = 0
            losses = 0

            # 데이터 가져오기
            df = pyupbit.get_ohlcv(self.coin, interval=self.interval, count=self.count)
            if df is None or df.empty:
                self.log_signal.emit("백테스트 데이터를 가져올 수 없습니다.")
                self.logs.append("백테스트 데이터를 가져올 수 없습니다.")
                return

            self.log_signal.emit(f"백테스트 시작: {self.coin}, 데이터 개수: {self.count}, 간격: {self.interval}")
            self.logs.append(f"백테스트 시작: {self.coin}, 데이터 개수: {self.count}, 간격: {self.interval}")

            # 시간 단위로 데이터를 순회
            for index in range(self.count):
                current_time = df.index[index].strftime('%Y-%m-%d %H:%M:%S')  # 실제 시간 가져오기
                # 각 블록 실행
                for block in self.blocks:
                    # 조건 평가
                    all_conditions_met = True
                    for condition in block.conditions:
                        condition_results = condition.backtest(df.iloc[:index + 1])
                        if not condition_results[index]:
                            all_conditions_met = False
                            break

                    # 조건이 모두 만족하거나 조건이 없는 경우 액션 실행
                    if all_conditions_met or not block.conditions:
                        if block.action:
                            # StopLossAction 또는 TakeProfitAction일 경우 buy_price를 추가로 전달
                            if isinstance(block.action, (StopLossAction, TakeProfitAction)):
                                action_results = block.action.backtest(
                                    historical_data=df.iloc[:index + 1],
                                    balance=balance,
                                    holdings=holdings,
                                    buy_price=self.buy_price
                                )
                            else:
                                action_results = block.action.backtest(
                                    historical_data=df.iloc[:index + 1],
                                    balance=balance,
                                    holdings=holdings,
                                    buy_price=self.buy_price
                                )

                            for result in action_results:
                                if result["status"] == "매수 성공":
                                    balance = result["balance"]
                                    holdings = result["holdings"]
                                    self.buy_price = result["buy_price"]  # 매수 가격 저장
                                    # 매수 성공 로그
                                    self.logs.append(f"매수 성공: 시간={current_time}, 잔액={balance:.2f}, 보유량={holdings:.6f}, 매수가={result['buy_price']:.2f}")
                                elif result["status"] == "매도 성공":
                                    balance = result["balance"]
                                    holdings = result["holdings"]
                                    profit = result["profit"]
                                    self.buy_price = None  # 매도 후 매수 가격 초기화
                                    if profit > 0:
                                        wins += 1
                                    elif profit < 0:
                                        losses += 1
                                    # 매도 성공 로그
                                    if not profit == 0:
                                        self.logs.append(f"매도 성공: 시간={current_time}, 잔액={balance:.2f}, 보유량={holdings:.6f}, 수익={profit:.2f}")


            # 백테스트 종료 후 남은 보유 수량 전부 매도
            if holdings > 0:
                final_price = df.iloc[-1]["close"]
                sell_amount = holdings * final_price
                balance += sell_amount
                self.logs.append(f"남은 보유 수량 {holdings:.6f}개를 {final_price:.2f} KRW에 매도하여 {sell_amount:.2f} KRW 추가.")
                self.log_signal.emit(f"남은 보유 수량 {holdings:.6f}개를 {final_price:.2f} KRW에 매도하여 {sell_amount:.2f} KRW 추가.")
                holdings = 0.0

            # 최종 결과 계산
            win_rate = (wins / (wins + losses)) * 100 if (wins + losses) > 0 else 0
            final_message = f"백테스트 완료. 최종 잔액: {balance:.2f}원, 승률: {win_rate:.2f}%"
            self.log_signal.emit(final_message)
            self.logs.append(final_message)

            # 결과 반환
            self.result_signal.emit({
                "initial_balance": self.initial_balance,
                "final_balance": balance,
                "total_trades": wins + losses,
                "wins": wins,
                "losses": losses,
                "win_rate": win_rate
            })

            # 로그를 JSON 파일로 저장
            self.save_logs_to_json()

        except Exception as e:
            error_message = f"백테스트 중 오류 발생: {e}"
            self.log_signal.emit(error_message)
            self.logs.append(error_message)
            self.result_signal.emit({})
            self.save_logs_to_json()

    def save_logs_to_json(self):
        """로그 데이터를 JSON 파일로 저장"""
        filename = f"backtest_logs.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.logs, f, ensure_ascii=False, indent=4)
            self.log_signal.emit(f"백테스트 로그가 {filename}에 저장되었습니다.")
        except Exception as e:
            self.log_signal.emit(f"로그 저장 중 오류 발생: {e}")

# ---------------------
# 블록 클래스
# ---------------------
class BlockWorker(QThread):
    log_signal = Signal(str)

    def __init__(self, block, interval_sec=10, parent=None):
        super().__init__(parent)
        self.block = block
        self.interval_sec = interval_sec
        self.running = True
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()

    def run(self):
        while self.running:
            if self.block.conditions:
                # 조건 결과를 "만족"/"미충족"으로 변환
                results = ["만족" if cond.check_condition() else "미충족" for cond in self.block.conditions]
                self.log_signal.emit(f"Block 실행 결과: {results}")

                # 모든 조건이 "만족"일 경우 액션 실행
                if all(cond.check_condition() for cond in self.block.conditions):
                    action_result = self.block.action.run_action()
                    self.log_signal.emit(action_result)
            else:
                # 조건이 없을 경우 액션 바로 실행
                action_result = self.block.action.run_action()
                self.log_signal.emit(action_result)

            self.msleep(int(self.interval_sec * 1000))


    def stop(self):
        self.mutex.lock()
        self.running = False
        self.wait_condition.wakeAll()
        self.mutex.unlock()


class Block:
    def __init__(self, action, conditions, interval_sec=10):
        self.action = action
        self.conditions = conditions
        self.interval_sec = interval_sec
        self.worker = None

    def start(self):
        if self.worker is None:
            self.worker = BlockWorker(self, self.interval_sec)
            self.worker.start()

    def stop(self):
        if self.worker is not None:
            self.worker.stop()
            self.worker.quit()
            self.worker.wait()
            self.worker = None


# ---------------------
# 블록 생성 Dialog
# ---------------------
from PySide6.QtWidgets import QCheckBox, QComboBox
from PySide6.QtWidgets import QCheckBox, QComboBox

class BlockConfigDialog(QDialog):
    def __init__(self, parent=None, upbit=None):
        super().__init__(parent)
        self.setWindowTitle("조건/액션 추가")
        self.upbit = upbit
        
        
        # ✅ 다이얼로그 스타일 설정
        self.setStyleSheet("""
            QDialog {
                background-color: #2E3440;  /* 다이얼로그 배경색 */
                border-radius: 10px;  /* 모서리 둥글게 */
                padding: 15px;  /* 내부 여백 */
            }
            QLabel {
                color: #D8DEE9;  /* 라벨 텍스트 색상 */
                font-size: 14px;  /* 라벨 글꼴 크기 */
                font-weight: bold;  /* 라벨 글꼴 굵게 */
            }
            QComboBox {
                background-color: #3B4252;  /* 콤보박스 배경색 */
                border: 1px solid #4C566A;  /* 테두리 색상 */
                border-radius: 5px;  /* 모서리 둥글게 */
                padding: 5px;  /* 내부 여백 */
                color: #ECEFF4;  /* 텍스트 색상 */
            }
            QComboBox QAbstractItemView {
                background-color: #3B4252;  /* 드롭다운 배경색 */
                border: 1px solid #4C566A;  /* 드롭다운 테두리 */
                color: #ECEFF4;  /* 드롭다운 텍스트 색상 */
            }
            QLineEdit {
                border: 1px solid #4C566A;  /* 테두리 색상 */
                border-radius: 5px;  /* 모서리 둥글게 */
                padding: 5px;  /* 내부 여백 */
                color: #ECEFF4;  /* 텍스트 색상 */
            }
            QLineEdit:focus {
                border: 1px solid #81A1C1;  /* 포커스 시 테두리 색상 */
            }
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
        # 레이아웃 설정
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 조건/액션 선택
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("조건 추가")
        self.mode_combo.addItem("액션 추가")
        self.layout.addWidget(QLabel("추가할 항목 선택"))
        self.layout.addWidget(self.mode_combo)
        self.mode_combo.currentTextChanged.connect(self.toggle_mode)

        # 조건 콤보박스
        self.condition_combo = QComboBox()
        for cond_name in ConditionRegistry.get_condition_names():
            self.condition_combo.addItem(cond_name)
        self.layout.addWidget(self.condition_combo)
        self.condition_combo.hide()  # 초기에는 숨김
        self.condition_combo.currentTextChanged.connect(self.load_action_fields)

        # 액션 콤보박스
        self.action_combo = QComboBox()
        for act_name in ActionRegistry.get_action_names():
            self.action_combo.addItem(act_name)
        self.layout.addWidget(self.action_combo)
        self.action_combo.hide()  # 초기에는 숨김
        self.action_combo.currentTextChanged.connect(self.load_action_fields)

        # 동적으로 생성되는 필드 레이아웃
        self.dynamic_fields_layout = QHBoxLayout()
        self.layout.addLayout(self.dynamic_fields_layout)

        # 버튼 박스
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # 초기 화면
        self.toggle_mode("조건 추가")

    def toggle_mode(self, mode):
        """조건/액션 모드 전환"""
        self.clear_dynamic_fields()

        if mode == "조건 추가":
            self.condition_combo.show()
            self.action_combo.hide()
            self.load_action_fields(self.condition_combo.currentText())
        elif mode == "액션 추가":
            self.condition_combo.hide()
            self.action_combo.show()
            self.load_action_fields(self.action_combo.currentText())

    def load_action_fields(self, name, is_action=False, obj=None):
        """조건/액션 필드 로드"""
        self.clear_dynamic_fields()

        # 조건/액션 선택에 따라 레지스트리 분기
        if self.mode_combo.currentText() == "조건 추가":
            registry = ConditionRegistry
        else:
            registry = ActionRegistry
        
        if is_action:
            registry = ActionRegistry

        # 레지스트리에서 클래스 가져오기
        action_cls = registry._registry.get(name)
        if not action_cls or not hasattr(action_cls, 'config_fields'):
            print(f"'{name}'에 대한 config_fields를 찾을 수 없습니다.")
            return

        self.input_fields = {}
        for field_name, field_info in action_cls.config_fields.items():
            label = QLabel(field_info['label'])
            self.dynamic_fields_layout.addWidget(label)

            ui_type = field_info.get("ui_type", "line_edit")
            if ui_type == "line_edit":
                input_widget = QLineEdit()
                input_widget.setText(str(getattr(self, field_name, field_info['default'])))
            elif ui_type == "checkbox":
                input_widget = QCheckBox()
                input_widget.setChecked(bool(getattr(self, field_name, field_info['default'])))
            elif ui_type == "dropdown":
                input_widget = QComboBox()
                for option in field_info.get("options", []):
                    input_widget.addItem(option)
                input_widget.setCurrentText(str(getattr(self, field_name, field_info['default'])))
            else:
                input_widget = QLineEdit()

            self.dynamic_fields_layout.addWidget(input_widget)
            self.input_fields[field_name] = (input_widget, field_info['type'], ui_type)
            
    def clear_dynamic_fields(self):
        """동적 필드 초기화"""
        while self.dynamic_fields_layout.count():
            item = self.dynamic_fields_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.input_fields = {}

    def get_config_data(self):
        """대화상자에서 입력된 데이터 가져오기"""
        mode = self.mode_combo.currentText()

        if mode == "조건 추가":
            name = self.condition_combo.currentText()
            registry = ConditionRegistry
        else:
            name = self.action_combo.currentText()
            registry = ActionRegistry

        kwargs = {}
        for field_name, (widget, field_type, ui_type) in self.input_fields.items():
            if ui_type == "line_edit":
                value = widget.text()
            elif ui_type == "checkbox":
                value = widget.isChecked()
            elif ui_type == "dropdown":
                value = widget.currentText()
            else:
                value = widget.text()

            try:
                kwargs[field_name] = field_type(value)
            except ValueError:
                kwargs[field_name] = field_type()  # 기본값 사용

        # 조건/액션에 따라 객체 생성
        new_object = registry.create_condition(name, **kwargs) if mode == "조건 추가" else registry.create_action(name, self.upbit, **kwargs)
        return mode[:-3], new_object  # "조건 추가" → "조건", "액션 추가" → "액션"

   


# ---------------------
# 메인 윈도우
# ---------------------
class BlockMain(QWidget):
    log_signal = Signal(str)

    def __init__(self, upbit):
        super().__init__()
        self.setWindowTitle("PyQt5 Block System as Frame")
        self.upbit = upbit

        self.blocks = []
        self.layout = QVBoxLayout(self)

        # History (결과 출력)
        self.history = QListWidget()
        
        # point label
        self.point1 = QLabel()
        self.point2 = QLabel()
        self.remain_time = QLabel()
        
        self.blocks = []
        self.max_blocks = 4
        
        # point1 = free, point2 = paid
        self.point = {
            "point1": 0,
            "point2": 0,
        }
        
        # 로딩 애니메이션 설정
        self.loading_label = QLabel(self)
        self.loading_movie = QMovie('loading.gif')
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setFixedSize(22, 22)

        # 포인트 소모 추적
        self.consumed_points = {
            "point1": 0,
            "point2": 0,
        }
    
    def update_upbit(self, new_upbit):
        """Upbit 객체 업데이트"""
        self.upbit = new_upbit
        print("BlockMain: Upbit 객체가 업데이트되었습니다.")
        # 블록 내 조건/액션의 Upbit 객체도 업데이트
        for block in self.blocks:
            if block.action:
                block.action.upbit = new_upbit
            for condition in block.conditions:
                if hasattr(condition, "upbit"):
                    condition.upbit = new_upbit
    
    def add_to_history(self, message):
        if message != "매수가격을 가져올 수 없음":
            self.history.addItem(message)
            self.history.scrollToBottom()

    def open_add_dialog(self, block, block_content_widget, pre_selected=None):
        """
        블록에 조건/액션 추가하는 대화상자 호출
        pre_selected가 있을 경우, 해당 조건/액션을 자동으로 추가.
        """
        if pre_selected:
            registry = ConditionRegistry if pre_selected in ConditionRegistry._registry else ActionRegistry
            obj = registry.create_condition(pre_selected) if registry == ConditionRegistry else registry.create_action(pre_selected, self.upbit)

            if isinstance(obj, Condition):
                block.conditions.append(obj)
                block_content_widget.addItem("조건: " + obj.name)
            elif isinstance(obj, Action):
                if block.action is None:
                    block.action = obj
                    block_content_widget.addItem("액션: " + obj.name)
                else:
                    QMessageBox.warning(self, "액션 추가 실패", "이 블록에는 이미 액션이 있습니다.")
            return

        # 기존 방식 (사용자가 직접 추가)
        dialog = BlockConfigDialog(parent=self, upbit=self.upbit)
        if dialog.exec_() == QDialog.Accepted:
            config_type, obj = dialog.get_config_data()

            if config_type == "조건":
                block.conditions.append(obj)
                block_content_widget.addItem("조건: " + obj.name)
            elif config_type == "액션":
                if block.action is None:
                    block.action = obj
                    block_content_widget.addItem("액션: " + obj.name)
                else:
                    QMessageBox.warning(self, "액션 추가 실패", "이 블록에는 이미 액션이 있습니다.")

    def add_block(self):
        if len(self.blocks) >= self.max_blocks:
            print("더 이상 블록을 추가할 수 없습니다 (최대 4개).")
            return

        # 새 블록 생성
        new_block = Block(None, [], 10)
        self.blocks.append(new_block)

        # QGroupBox 생성
        block_group = QGroupBox(f"Block {len(self.blocks)}")
        block_group.setStyleSheet("""
            QGroupBox {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                                stop:0 rgba(40, 40, 50, 255), 
                                                stop:1 rgba(30, 30, 40, 255)); /* 다크 그라데이션 */
                border: 1px solid rgba(100, 100, 110, 180); /* 테두리 색상 */
                border-radius: 10px; /* 모서리 둥글게 */
                margin-top: 10px; /* 제목과 내용 간격 */
                padding: 10px; /* 내부 여백 */
            }
            QGroupBox::title {
                color: rgba(220, 220, 230, 230); /* 제목 색상 */
                font-size: 12pt; /* 제목 글꼴 크기 */
                font-weight: bold; /* 제목 글꼴 굵게 */
                subcontrol-origin: margin;
                subcontrol-position: top left; /* 제목 위치 */
                padding: 5px 15px; /* 제목 여백 */
                background-color: transparent; /* 제목 배경 투명 */
            }
            QGroupBox:hover {
                border: 1px solid rgba(150, 150, 160, 220); /* 호버 시 테두리 색상 */
                background-color: rgba(50, 50, 60, 255); /* 호버 시 배경색 */
            }
        """)
        block_layout = QHBoxLayout(block_group)

        # ─── 왼쪽 (라벨 & 리스트) ───
        left_layout = QVBoxLayout()

        block_content = QListWidget()
        block_content.setStyleSheet("""
            QListWidget {
                background-color: #3B4252;  /* 리스트 배경색 */
                border: 1px solid #4C566A;  /* 테두리 색상 */
                border-radius: 5px;  /* 모서리 둥글게 */
                padding: 5px;  /* 내부 여백 */
                color: #ECEFF4;  /* 글자 색상 */
            }
            QListWidget::item {
                padding: 5px;  /* 항목 내부 여백 */
            }
            QListWidget::item:selected {
                background-color: #81A1C1;  /* 선택된 항목 배경색 */
                color: #2E3440;  /* 선택된 항목 글꼴 색상 */
            }
        """)
        block_content.itemDoubleClicked.connect(lambda item: self.edit_or_delete_item(new_block, block_content, item))  # ✅ 더블클릭 이벤트 연결
        left_layout.addWidget(block_content)

        block_layout.addLayout(left_layout)

        # ─── 오른쪽 (주기 입력 & 버튼) ───
        right_layout = QVBoxLayout()

        interval_label = QLabel(f"실행 주기 설정 (초)")
        interval_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #D8DEE9;
            }
        """)
        right_layout.addWidget(interval_label)

        interval_edit = QLineEdit()
        interval_edit.setPlaceholderText("주기 (초)")
        interval_edit.setStyleSheet("""
            QLineEdit {
                background-color: #3B4252;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 5px;
                color: #ECEFF4;
            }
            QLineEdit:focus {
                border: 1px solid #81A1C1;  /* 포커스 시 테두리 색상 */
            }
        """)
        right_layout.addWidget(interval_edit)

        add_config_btn = QPushButton("+ 조건/액션 추가")
        add_config_btn.setStyleSheet("""
            QPushButton {
                background-color: #81A1C1;  /* 버튼 배경색 */
                color: #2E3440;  /* 버튼 글꼴 색상 */
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #5E81AC;  /* 호버 시 배경색 */
            }
            QPushButton:pressed {
                background-color: #4C566A;  /* 클릭 시 배경색 */
            }
        """)
        add_config_btn.clicked.connect(lambda: self.open_add_dialog(new_block, block_content))
        right_layout.addWidget(add_config_btn)

        # 버튼 하단에 추가 여유 공간
        right_layout.addStretch()

        block_layout.addLayout(right_layout)

        # ➡ 왼쪽 레이아웃(0번)에 더 큰 비율(예: 3), 오른쪽 레이아웃(1번)에 더 작은 비율(예: 1)
        block_layout.setStretch(0, 3)
        block_layout.setStretch(1, 1)

        new_block.interval_edit = interval_edit
        self.layout.addWidget(block_group)

        return new_block  # ✅ 생성된 블록 객체 반환
    
    
    def edit_or_delete_item(self, block, block_content, item):
        """조건/액션 수정"""
        item_text = item.text()
        is_condition = item_text.startswith("조건: ")
        obj_name = item_text.replace("조건: ", "").replace("액션: ", "")

        # 조건 또는 액션 객체 찾기
        obj = None
        if is_condition:
            obj = next((cond for cond in block.conditions if cond.name == obj_name), None)
        else:
            obj = block.action if block.action and block.action.name == obj_name else None

        if not obj:
            return

        # 기존 조건/액션 삭제
        if is_condition:
            block.conditions.remove(obj)
        else:
            block.action = None
        block_content.takeItem(block_content.row(item))  # UI에서 제거

        # 새 조건/액션 추가
        self.open_add_dialog(block, block_content)
    
    def run_all_blocks(self, coin):
        if self.point["point1"] < 1 and self.point["point2"] < 1:
            self.add_to_history("포인트가 부족합니다.")
            return
        
        for block in self.blocks:
            if block.action is not None:
                # 각 조건과 액션에 coin 업데이트
                for condition in block.conditions:
                    if hasattr(condition, "coin"):
                        condition.coin = coin

                if hasattr(block.action, "coin"):
                    block.action.coin = coin

                # 실행 주기 설정
                if hasattr(block, "interval_edit"):
                    text = block.interval_edit.text()
                    if text.strip().isdigit():
                        block.interval_sec = int(text.strip())
                        
                # ToggleBlockAction 처리
                if isinstance(block.action, ToggleBlockAction):
                    result = block.action.run_action(self.blocks)
                    self.add_to_history(result)
                    continue
                
                # 타이머 추가
                # 타이머는 1분당 point1를 1씩 차감
                # 만약 point1 = 0이 되면 point2를 1씩 차감
                # point2 = 0이 되면 더 이상 블록 실행 불가
                # 블록 쓰레드 종료
                if block.worker is None:
                    block.worker = BlockWorker(block, block.interval_sec)
                    block.worker.log_signal.connect(self.add_to_history)
                    block.worker.start()
                    
                    self.timer = QTimer()
                    self.timer.setInterval(60000)  # 1분마다 실행
                    self.timer.timeout.connect(self.update_point)
                    self.timer.start()
                    
    def update_point(self):
        """포인트를 차감하고 소모된 포인트를 추적"""
        if self.point["point1"] > 0:
            self.point["point1"] -= 1
            self.consumed_points["point1"] += 1
            self.point1.setText(f"금화: {self.point["point1"]}")
            remain_time = self.point_to_time(self.point["point1"] + self.point["point2"])
            self.remain_time.setText(f"남은시간: {remain_time}분")
        elif self.point["point2"] > 0:
            self.point["point2"] -= 1
            self.consumed_points["point2"] += 1
            self.point1.setText(f"금화: {self.point["point2"]}")
            remain_time = self.point_to_time(self.point["point1"] + self.point["point2"])
            self.remain_time.setText(f"남은시간: {remain_time}분")
        else:
            self.stop_all_blocks()
            remain_time = self.point_to_time(self.point["point1"] + self.point["point2"])
            self.remain_time.setText(f"남은시간: {remain_time}분")
            self.add_to_history("포인트가 부족합니다.")
            return
        
    def stop_all_blocks(self):
        """모든 블록을 중지하고 소모된 포인트를 서버로 전송"""
        # 로딩 애니메이션 표시
        self.loading_screen = LoadingDialog()
        self.loading_screen.show_loading()

        for block in self.blocks:
            if block.worker is not None:
                block.worker.terminate()  # ✅ 강제 종료
                block.worker = None  # ✅ 바로 None 처리하여 즉시 종료 효과
        
        try:
            self.timer.stop()
        except:
            pass

        # 서버로 소모된 포인트 전송
        try:
            self.send_consumed_points_to_server()
        except:
            QMessageBox.information(self, "서버 연결 실패", "서버와 연결 실패했습니다.")
        # 로딩 애니메이션 숨기기

        self.loading_screen.hide_loading()

        self.add_to_history("모든 블록이 종료되었습니다.")
        
    def send_consumed_points_to_server(self):
        """소모된 포인트를 서버로 전송"""
        # 토큰 갱신
        try:
            new_token = self.upbit.refresh_token()  # Upbit 객체에 refresh_token 메서드가 있다고 가정
            if not new_token:
                raise ValueError("토큰 갱신 실패: 새 토큰이 None입니다.")
            self.upbit.token = new_token  # 갱신된 토큰 업데이트
        except Exception as e:
            return

        # 서버 요청 URL 및 헤더 설정
        url = f"http://{SURVER_URL}/api/user/update_consumed_points/"  # 슬래시 확인
        headers = {
            "Authorization": f"Bearer {self.upbit.token}",  # 갱신된 토큰 사용
            "Content-Type": "application/json"
        }
        data = {
            "consumed_point1": self.consumed_points["point1"],
            "consumed_point2": self.consumed_points["point2"]
        }
        
        try:
            # 서버로 POST 요청 전송
            response = requests.post(url, headers=headers, json=data)
            print(response)
            if response.status_code == 200:
                self.add_to_history("소모된 포인트가 서버에 성공적으로 저장되었습니다.")
                # 요청 성공 시 소모된 포인트 초기화
                self.consumed_points = {"point1": 0, "point2": 0}
            else:
                # 요청 실패 시 상세 오류 메시지 출력
                self.add_to_history(f"서버 요청 실패: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            # 네트워크 오류 처리
            self.add_to_history(f"서버 요청 중 네트워크 오류 발생: {e}")
        except Exception as e:
            # 기타 예외 처리
            self.add_to_history(f"서버 요청 중 알 수 없는 오류 발생: {e}")

    def closeEvent(self, event):
        """창 닫기 이벤트에서 모든 블록을 중지하고 포인트를 서버로 전송"""
        self.stop_all_blocks()
        super().closeEvent(event)
        
    def clear_blocks(self):
        """ 기존 블록 초기화 """
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        self.blocks.clear()
    
    def point_to_time(self, point):
        """point를 시:분:초 형식으로 변환합니다."""
        hours = point // 60
        minutes = point % 60
        # 시:분 형식으로 변환
        return f"{hours:02}:{minutes:02}"
    
    #############################################################
    # 백테스트
    #############################################################
    def run_backtest(self, coin, interval, count, initial_balance):
        """
        백테스트 실행 (쓰레드 기반)
        :param coin: 테스트할 코인 (예: "KRW-BTC")
        :param interval: 분봉 간격 (예: "minute1", "minute5")
        :param count: 가져올 데이터 개수
        :param initial_balance: 초기 자본 (예: 1000000)
        """
        self.thread = QThread()
        self.backtest_worker = BacktestWorker(coin, interval, count, initial_balance, self.blocks)
        self.backtest_worker.moveToThread(self.thread)

        # 연결 설정
        self.thread.started.connect(self.backtest_worker.run)
        self.backtest_worker.log_signal.connect(self.add_to_history)
        self.backtest_worker.result_signal.connect(self.handle_backtest_result)
        self.backtest_worker.result_signal.connect(self.thread.quit)  # 작업 완료 시 쓰레드 종료
        self.thread.finished.connect(self.thread.deleteLater)

        # 쓰레드 시작
        self.thread.start()
        
    def handle_backtest_result(self, result):
        """
        백테스트 결과 처리
        :param result: dict, 백테스트 결과
        """
        if not result:
            self.add_to_history("백테스트가 실패했습니다.")
            return

        self.add_to_history("백테스트 결과:")
        self.add_to_history(f"초기 잔액: {result['initial_balance']}원")
        self.add_to_history(f"최종 잔액: {result['final_balance']}원")
        self.add_to_history(f"총 거래 횟수: {result['total_trades']}회")
        self.add_to_history(f"승리 횟수: {result['wins']}회")
        self.add_to_history(f"패배 횟수: {result['losses']}회")
        self.add_to_history(f"승률: {result['win_rate']:.2f}%")