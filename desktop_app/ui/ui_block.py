import sys
import time
from PySide6.QtCore import Qt, QThread, Signal, QObject, QMutex, QWaitCondition
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel,
    QFrame, QDialog, QDialogButtonBox, QComboBox, QLineEdit, QCheckBox, QHBoxLayout
)

# ---------------------
# 부모 조건 클래스
# ---------------------
class Condition(QObject):
    def check_condition(self) -> bool:
        raise NotImplementedError("check_condition()을 자식 클래스에서 오버라이드해야 합니다.")

class ConditionRegistry:
    _registry = {}

    @classmethod
    def register(cls, name):
        def decorator(condition_cls):
            cls._registry[name] = condition_cls
            return condition_cls
        return decorator

    @classmethod
    def get_condition_names(cls):
        return list(cls._registry.keys())

    @classmethod
    def create_condition(cls, name, *args, **kwargs):
        condition_cls = cls._registry.get(name)
        if condition_cls:
            return condition_cls(*args, **kwargs)
        else:
            raise ValueError(f"{name}은(는) 등록되지 않은 Condition입니다.")


# ---------------------
# 샘플 자식 조건    
# ---------------------
@ConditionRegistry.register("캔들 검사")
class CandleCheckCondition(Condition):
    config_fields = {
        "candle_type": {"label": "캔들 종류", "type": str, "default": "양봉", "ui_type": "dropdown", "options": ["양봉", "음봉"]},
        "threshold": {"label": "기준값", "type": float, "default": 100.0, "ui_type": "line_edit"},
        "strict_mode": {"label": "엄격 모드", "type": bool, "default": False, "ui_type": "checkbox"}
    }

    def __init__(self, candle_type="양봉", threshold=100.0, strict_mode=False):
        super().__init__()
        self.candle_type = candle_type
        self.threshold = threshold
        self.strict_mode = strict_mode

    def check_condition(self) -> bool:
        print(f"캔들 타입: {self.candle_type}, 기준값: {self.threshold}, 엄격 모드: {self.strict_mode}")
        return self.threshold > 50  # 예시 로직
    
@ConditionRegistry.register("캔들 확인")
class CandleCheckCondition(Condition):
    config_fields = {
        "quantity": {"label": "구매 수량", "type": int, "default": 1, "ui_type": "line_edit"},
        "price_limit": {"label": "최대 구매가", "type": float, "default": 10000.0, "ui_type": "line_edit"},
        "urgent": {"label": "긴급 구매", "type": bool, "default": False, "ui_type": "checkbox"}
    }

    def __init__(self, candle_type="양봉", threshold=100.0, strict_mode=False):
        super().__init__()
        self.candle_type = candle_type
        self.threshold = threshold
        self.strict_mode = strict_mode

    def check_condition(self) -> bool:
        print(f"캔들 타입: {self.candle_type}, 기준값: {self.threshold}, 엄격 모드: {self.strict_mode}")
        return self.threshold > 50  # 예시 로직




# ---------------------
# 부모 액션 클래스
# ---------------------
class Action(QObject):
    def run_action(self):
        raise NotImplementedError("run_action()을 자식 클래스에서 오버라이드해야 합니다.")

class ActionRegistry:
    _registry = {}

    @classmethod
    def register(cls, name):
        def decorator(action_cls):
            cls._registry[name] = action_cls
            return action_cls
        return decorator

    @classmethod
    def get_action_names(cls):
        return list(cls._registry.keys())

    @classmethod
    def create_action(cls, name, *args, **kwargs):
        action_cls = cls._registry.get(name)
        if action_cls:
            return action_cls(*args, **kwargs)
        else:
            raise ValueError(f"{name}은(는) 등록되지 않은 Action입니다.")






# ---------------------
# 샘플 액션 등록
# ---------------------
@ActionRegistry.register("매수 액션")
class PurchaseAction(Action):
    config_fields = {
        "quantity": {"label": "구매 수량", "type": int, "default": 1, "ui_type": "line_edit"},
        "price_limit": {"label": "최대 구매가", "type": float, "default": 10000.0, "ui_type": "line_edit"},
        "urgent": {"label": "긴급 구매", "type": bool, "default": False, "ui_type": "checkbox"}
    }

    def __init__(self, quantity=1, price_limit=10000.0, urgent=False):
        super().__init__()
        self.quantity = quantity
        self.price_limit = price_limit
        self.urgent = urgent

    def run_action(self):
        urgency = " (긴급)" if self.urgent else ""
        return f"{self.quantity}개 구매 완료 (최대 가격 {self.price_limit}){urgency}"

@ActionRegistry.register("매도 액션")
class SellAction(Action):
    config_fields = {
        "quantity": {"label": "판매 수량%", "type": int, "default": 1, "ui_type": "line_edit"},
    }

    def __init__(self, quantity=1):
        super().__init__()
        self.quantity = quantity

    def run_action(self):
        return f"{self.quantity}개 판매 완료"







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
            results = [cond.check_condition() for cond in self.block.conditions]
            self.log_signal.emit(f"Block 실행 결과: {results}")

            # 모든 조건이 True일 경우 액션 실행 (원하시는 로직대로)
            if all(results):
                action_result = self.block.action.run_action()
                # 액션이 반환한 메시지를 history에 표시
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("조건/액션 추가")

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # 조건/액션 선택
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("선택")
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

        # ✅ 동적으로 생성되는 필드 레이아웃
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
        self.clear_dynamic_fields()

        if mode == "선택":
            self.condition_combo.hide()
            self.action_combo.hide()

        elif mode == "조건 추가":
            self.condition_combo.show()
            self.action_combo.hide()
            self.load_action_fields(self.condition_combo.currentText())

        elif mode == "액션 추가":
            self.condition_combo.hide()
            self.action_combo.show()
            self.load_action_fields(self.action_combo.currentText())

    def load_action_fields(self, name):
        self.clear_dynamic_fields()

        # ✅ 조건/액션 선택에 따라 레지스트리 분기
        if self.mode_combo.currentText() == "조건 추가":
            registry = ConditionRegistry
        else:
            registry = ActionRegistry

        action_cls = registry._registry.get(name)
        if not action_cls or not hasattr(action_cls, 'config_fields'):
            return

        self.input_fields = {}
        for field_name, field_info in action_cls.config_fields.items():
            label = QLabel(field_info['label'])
            self.dynamic_fields_layout.addWidget(label)

            ui_type = field_info.get("ui_type", "line_edit")
            if ui_type == "line_edit":
                input_widget = QLineEdit()
                input_widget.setText(str(field_info['default']))
            elif ui_type == "checkbox":
                input_widget = QCheckBox()
                input_widget.setChecked(bool(field_info['default']))
            elif ui_type == "dropdown":
                input_widget = QComboBox()
                for option in field_info.get("options", []):
                    input_widget.addItem(option)
            else:
                input_widget = QLineEdit()

            self.dynamic_fields_layout.addWidget(input_widget)
            self.input_fields[field_name] = (input_widget, field_info['type'], ui_type)

    def clear_dynamic_fields(self):
        while self.dynamic_fields_layout.count():
            item = self.dynamic_fields_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.input_fields = {}
        
    def get_config_data(self):
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

        # ✅ 조건/액션에 따라 객체 생성
        new_object = registry.create_condition(name, **kwargs) if mode == "조건 추가" else registry.create_action(name, **kwargs)
        return mode[:-3], new_object  # "조건 추가" → "조건", "액션 추가" → "액션"

   


# ---------------------
# 메인 윈도우
# ---------------------
class BlockMain(QWidget):
    log_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Block System as Frame")

        self.layout = QVBoxLayout(self)

        # 실행/중지 버튼
        self.run_all_button = QPushButton("실행")
        self.run_all_button.clicked.connect(self.run_all_blocks)
        self.layout.addWidget(self.run_all_button)

        self.stop_all_button = QPushButton("중지")
        self.stop_all_button.clicked.connect(self.stop_all_blocks)
        self.layout.addWidget(self.stop_all_button)

        # 블록 추가 버튼
        self.add_block_button = QPushButton("+ 블록 추가")
        self.add_block_button.clicked.connect(self.add_block)
        self.layout.addWidget(self.add_block_button)

        # History (결과 출력)
        self.history = QListWidget()
        self.layout.addWidget(QLabel("History"))
        self.layout.addWidget(self.history)

        self.blocks = []
        self.max_blocks = 4

    def add_to_history(self, message):
        self.history.addItem(message)
        self.history.scrollToBottom()

    def open_add_dialog(self, block, block_content_widget):
        dialog = BlockConfigDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            config_type, obj = dialog.get_config_data()

            if config_type == "조건":
                block.conditions.append(obj)
                block_content_widget.addItem("조건: " + obj.__class__.__name__)
            elif config_type == "액션":
                if block.action is None:
                    block.action = obj
                    block_content_widget.addItem("액션: " + obj.__class__.__name__)
                else:
                    print("이 블록에는 이미 액션이 있습니다.")

    def add_block(self):
        if len(self.blocks) >= self.max_blocks:
            print("더 이상 블록을 추가할 수 없습니다 (최대 4개).")
            return

        new_block = Block(None, [], 10)  # 빈 블록 생성
        self.blocks.append(new_block)

        # 🔹 블록 Frame 생성
        block_frame = QFrame()
        block_frame.setFrameShape(QFrame.StyledPanel)
        block_layout = QHBoxLayout(block_frame)

        # 블록 제목
        block_label = QLabel(f"Block {len(self.blocks)}")
        block_layout.addWidget(block_label)

        # 조건/액션 표시용 리스트
        block_content = QListWidget()
        block_layout.addWidget(block_content)

        # 조건/액션 추가 버튼
        add_config_btn = QPushButton("+ 조건/액션 추가")
        add_config_btn.clicked.connect(lambda: self.open_add_dialog(new_block, block_content))
        block_layout.addWidget(add_config_btn)

        # 블록 UI 배치
        self.layout.addWidget(block_frame)

    def run_all_blocks(self):
        for block in self.blocks:
            if block.action is not None and block.conditions:
                if block.worker is None:
                    block.worker = BlockWorker(block, block.interval_sec)
                    block.worker.log_signal.connect(self.add_to_history)
                    block.worker.start()

    def stop_all_blocks(self):
        for block in self.blocks:
            block.stop()
        self.add_to_history("모든 블록이 중지되었습니다.")

    def closeEvent(self, event):
        self.stop_all_blocks()
        super().closeEvent(event)

