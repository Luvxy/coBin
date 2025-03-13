import sys
import time
import os
import json
import pyupbit
from PySide6.QtCore import Qt, QThread, Signal, QObject, QMutex, QWaitCondition
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel,
    QFrame, QDialog, QDialogButtonBox, QComboBox, QLineEdit, QCheckBox, QHBoxLayout
)
from PySide6.QtGui import QMovie
from main import LoadingDialog

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
# 조건 등록
# ---------------------





@ConditionRegistry.register("지정 캔들 양봉/음봉 확인")
class CheckCandleTypeCondition(Condition):
    config_fields = {
        "candle_index": {"label": "캔들 번호", "type": int, "default": 0, "ui_type": "line_edit"},
        "target_type": {"label": "캔들 유형", "type": str, "default": "양봉", "ui_type": "dropdown", "options": ["양봉", "음봉"]},
        "interval": {"label": "캔들 시간 간격", "type": str, "default": "minute30", "ui_type": "line_edit"},
    }

    def __init__(self, candle_index=0, target_type="양봉", coin="KRW-BTC", interval="minute30"):
        super().__init__()
        self.obj_name = "지정 캔들 양봉/음봉 확인"
        self.name = f"지정 캔들 {candle_index}번째 {target_type} 확인"
        self.candle_index = candle_index
        self.target_type = target_type
        self.coin = coin
        self.interval = interval

    def check_condition(self) -> bool:
        df = pyupbit.get_ohlcv(self.coin, interval=self.interval, count=self.candle_index + 1)
        if df is None or df.empty or len(df) <= self.candle_index:
            print("캔들 데이터를 가져올 수 없음")
            return False

        target_candle = df.iloc[-(self.candle_index + 1)]
        is_bullish = target_candle['open'] < target_candle['close']

        return is_bullish if self.target_type == "양봉" else not is_bullish

@ConditionRegistry.register("거래량 확인")
class CheckVolumeCondition(Condition):
    config_fields = {
        "volume_threshold": {"label": "거래량 기준", "type": float, "default": 1000.0, "ui_type": "line_edit"},
        "check_type": {"label": "비교 유형", "type": str, "default": "이상", "ui_type": "dropdown", "options": ["이상", "이하"]},
        "interval": {"label": "캔들 시간 간격", "type": str, "default": "minute30", "ui_type": "line_edit"},
    }

    def __init__(self, volume_threshold=1000.0, check_type="이상", coin="KRW-BTC", interval="minute30"):
        super().__init__()
        self.obj_name = "거래량 확인"
        self.name = f"거래량 {volume_threshold} {check_type} 확인"
        self.volume_threshold = volume_threshold
        self.check_type = check_type
        self.coin = coin
        self.interval = interval

    def check_condition(self) -> bool:
        df = pyupbit.get_ohlcv(self.coin, interval=self.interval, count=1)
        if df is None or df.empty:
            print("거래량 데이터를 가져올 수 없음")
            return False

        current_volume = df.iloc[-1]['volume']
        print(f"현재 거래량: {current_volume:.2f}")

        return current_volume >= self.volume_threshold if self.check_type == "이상" else current_volume <= self.volume_threshold

@ConditionRegistry.register("현재 가격 확인")
class CheckPriceCondition(Condition):
    config_fields = {
        "price_threshold": {"label": "가격 기준", "type": float, "default": 50000.0, "ui_type": "line_edit"},
        "check_type": {"label": "비교 유형", "type": str, "default": "이상", "ui_type": "dropdown", "options": ["이상", "이하"]}
    }

    def __init__(self, price_threshold=50000.0, check_type="이상", coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "현재 가격 확인"
        self.name = f"현재 가격이 {price_threshold} {check_type} 확인"
        self.price_threshold = price_threshold
        self.check_type = check_type
        self.coin = coin

    def check_condition(self) -> bool:
        current_price = pyupbit.get_current_price(self.coin)
        print(f"현재 가격: {current_price:.2f}")

        return current_price >= self.price_threshold if self.check_type == "이상" else current_price <= self.price_threshold

@ConditionRegistry.register("가격 변동률 확인")
class CheckPriceChangeCondition(Condition):
    config_fields = {
        "change_threshold": {"label": "변동률 기준 (%)", "type": float, "default": 3.0, "ui_type": "line_edit"},
        "check_type": {"label": "비교 유형", "type": str, "default": "이상", "ui_type": "dropdown", "options": ["이상", "이하"]}
    }

    def __init__(self, change_threshold=3.0, check_type="이상", coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "가격 변동률 확인"
        self.name = f"가격 변동률이 {change_threshold}% {check_type} 확인"
        self.change_threshold = change_threshold
        self.check_type = check_type
        self.coin = coin

    def check_condition(self) -> bool:
        df = pyupbit.get_ohlcv(self.coin, interval='minute30', count=2)
        if df is None or df.empty or len(df) < 2:
            print("가격 데이터를 가져올 수 없음")
            return False

        prev_close = df.iloc[-2]['close']
        current_close = df.iloc[-1]['close']
        price_change = (current_close - prev_close) / prev_close * 100
        print(f"가격 변동률: {price_change:.2f}%")

        return price_change >= self.change_threshold if self.check_type == "이상" else price_change <= self.change_threshold


@ConditionRegistry.register("이동평균선 돌파/하회 확인")
class CheckMovingAverageCondition(Condition):
    config_fields = {
        "ma_days": {"label": "이동평균 일수", "type": int, "default": 5, "ui_type": "line_edit"},
        "check_type": {"label": "확인 유형", "type": str, "default": "상향 돌파", "ui_type": "dropdown", "options": ["상향 돌파", "하향 돌파"]}
    }

    def __init__(self, ma_days=5, check_type="상향 돌파", coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "이동평균선 돌파/하회 확인"
        self.name = f"{ma_days}일 동안 이동평균선 {check_type}"
        self.ma_days = ma_days
        self.check_type = check_type
        self.coin = coin

    def check_condition(self) -> bool:
        df = pyupbit.get_ohlcv(self.coin, interval='minute30', count=self.ma_days + 1)
        if df is None or df.empty or len(df) < self.ma_days + 1:
            print("가격 데이터를 가져올 수 없음")
            return False

        ma = df['close'].rolling(window=self.ma_days).mean()
        current_price = df.iloc[-1]['close']
        current_ma = ma.iloc[-1]
        prev_ma = ma.iloc[-2]

        is_break_up = current_price > current_ma > prev_ma
        is_break_down = current_price < current_ma < prev_ma

        return is_break_up if self.check_type == "상향 돌파" else is_break_down
    
@ConditionRegistry.register("시간 범위 선택")
class CheckTimeRangeCondition(Condition):
    config_fields = {
        "start_hour": {"label": "시작 시간 (시)", "type": int, "default": 9, "ui_type": "line_edit"},
        "end_hour": {"label": "종료 시간 (시)", "type": int, "default": 15, "ui_type": "line_edit"},
    }

    def __init__(self, start_hour=9, end_hour=15):
        super().__init__()
        self.obj_name = "시간 범위 선택"
        self.name = f"{start_hour}시 ~ {end_hour}시 사이"
        self.start_hour = start_hour
        self.end_hour = end_hour

    def check_condition(self) -> bool:
        current_hour = time.localtime().tm_hour
        return self.start_hour <= current_hour <= self.end_hour



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

@ConditionRegistry.register("최고가/최저가 비교")
class HighLowComparisonCondition(Condition):
    config_fields = {
        "candle1": {"label": "첫 번째 캔들 인덱스", "type": int, "default": 1, "ui_type": "line_edit"},
        "candle2": {"label": "두 번째 캔들 인덱스", "type": int, "default": 2, "ui_type": "line_edit"},
        "compare_type": {"label": "비교 유형", "type": str, "default": "최고가vs최저가", "ui_type": "dropdown", 
                         "options": ["최고가vs최저가", "최고가vs최고가", "최저가vs최저가", "최고가vs현재가", "최저가vs현재가", "현재가vs최고가", "현재가vs최저가"]},
        "interval": {"label": "캔들 시간 간격", "type": str, "default": "minute30", "ui_type": "line_edit"},
    }

    def __init__(self, candle1=1, candle2=2, compare_type="최고가vs최저가", coin="KRW-BTC", interval="minute30"):
        super().__init__()
        self.obj_name = "최고가/최저가 비교"
        self.candle1 = candle1
        self.candle2 = candle2
        self.compare_type = compare_type
        self.coin = coin
        self.interval = interval
        self.name = f"{candle1}번째와 {candle2}번째 캔들 {compare_type} 비교"

    def check_condition(self) -> bool:
        df = pyupbit.get_ohlcv(self.coin, interval=self.interval, count=max(self.candle1, self.candle2) + 1)
        if df is None or df.empty or len(df) <= max(self.candle1, self.candle2):
            print("캔들 데이터를 가져올 수 없음")
            return False

        high1 = df.iloc[-(self.candle1 + 1)]['high']
        low1 = df.iloc[-(self.candle1 + 1)]['low']
        high2 = df.iloc[-(self.candle2 + 1)]['high']
        low2 = df.iloc[-(self.candle2 + 1)]['low']
        current_price = pyupbit.get_current_price(self.coin)

        if self.compare_type == "최고가vs최저가":
            return high1 > low2
        elif self.compare_type == "최고가vs최고가":
            return high1 > high2
        elif self.compare_type == "최저가vs최저가":
            return low1 > low2
        elif self.compare_type == "최고가vs현재가":
            return high1 > current_price
        elif self.compare_type == "최저가vs현재가":
            return low1 > current_price
        elif self.compare_type == "현재가vs최고가":
            return high1 < current_price
        elif self.compare_type == "현재가vs최저가":
            return low1 < current_price
        else:
            return False






# ---------------------
# 샘플 액션 등록
# ---------------------
@ActionRegistry.register("시장가 매수")
class MarketBuyAction(Action):
    config_fields = {
        "amount": {"label": "매수 금액 (KRW 또는 %)", "type": str, "default": "10000", "ui_type": "line_edit"},
    }

    def __init__(self, upbit, amount="10000", coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "시장가 매수"
        self.upbit = upbit
        self.amount = amount  # 문자열로 입력받아 % 처리 가능
        self.coin = coin
        self.name = f"시장가 매수: {amount} KRW"

    def run_action(self):
        krwb = self.upbit.get_balance("KRW")
        if krwb < 5000:
            return "KRW 잔고 부족"
        balance = krwb * 0.9995  # 현재 보유 KRW
        if self.amount.endswith("%"):  # % 입력 처리
            percent = float(self.amount.strip('%')) / 100
            order_amount = balance * percent
        else:
            order_amount = float(self.amount)
        
        if order_amount > balance:
            return "보유 KRW 부족"
        
        order_result = self.upbit.buy_market_order(self.coin, order_amount)
        return f"시장가 매수 실행: {self.coin} - {order_amount:.2f} KRW" if order_result else "매수 실패"

@ActionRegistry.register("시장가 매도")
class MarketSellAction(Action):
    config_fields = {
        "quantity": {"label": "판매 수량 (개 또는 %)", "type": str, "default": "1", "ui_type": "line_edit"},
    }

    def __init__(self, upbit, quantity="1", coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "시장가 매도"
        self.upbit = upbit
        self.quantity = quantity  # 문자열로 입력받아 % 처리 가능
        self.coin = coin
        self.name = f"시장가 매도: {quantity}개"

    def run_action(self):
        balance = self.upbit.get_balance(self.coin)  # 현재 보유 수량
        if self.quantity.endswith("%"):  # % 입력 처리
            percent = float(self.quantity.strip('%')) / 100
            order_quantity = balance * percent
        else:
            order_quantity = float(self.quantity)
        
        if order_quantity > balance:
            return "보유 수량 부족"
        
        order_result = self.upbit.sell_market_order(self.coin, order_quantity)
        return f"시장가 매도 실행: {self.coin} - {order_quantity:.6f}개" if order_result else "매도 실패"


@ActionRegistry.register("지정가 매수")
class LimitBuyAction(Action):
    config_fields = {
        "price": {"label": "매수 가격", "type": float, "default": 10000.0, "ui_type": "line_edit"},
        "quantity": {"label": "구매 수량", "type": float, "default": 1.0, "ui_type": "line_edit"},
    }

    def __init__(self, upbit, price=10000.0, quantity=1.0, coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "지정가 매수"
        self.upbit = upbit
        self.price = price
        self.quantity = quantity
        self.coin = coin
        self.name = f"지정가 매수: {quantity}개  {price} KRW"

    def run_action(self):
        order_result = self.upbit.buy_limit_order(self.coin, self.price, self.quantity)
        return f"지정가 매수 실행: {self.coin} {self.quantity}개  {self.price} KRW" if order_result else "매수 실패"

@ActionRegistry.register("지정가 매도")
class LimitSellAction(Action):
    config_fields = {
        "price": {"label": "매도 가격", "type": float, "default": 10000.0, "ui_type": "line_edit"},
        "quantity": {"label": "판매 수량", "type": float, "default": 1.0, "ui_type": "line_edit"},
    }

    def __init__(self, upbit, price=10000.0, quantity=1.0, coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "지정가 매도"
        self.upbit = upbit
        self.price = price
        self.quantity = quantity
        self.coin = coin
        self.name = f"지정가 매도: {quantity}개 @ {price} KRW"

    def run_action(self):
        order_result = self.upbit.sell_limit_order(self.coin, self.price, self.quantity)
        return f"지정가 매도 실행: {self.coin} {self.quantity}개 @ {self.price} KRW" if order_result else "매도 실패"


import pyupbit

@ActionRegistry.register("스탑로스(손절)")
class StopLossAction(Action):
    config_fields = {
        "stop_loss_percent": {"label": "손절 기준 수익률 (%)", "type": str, "default": "-5%", "ui_type": "line_edit"},
        "quantity_percent": {"label": "판매 수량 (%)", "type": str, "default": "100%", "ui_type": "line_edit"},
    }

    def __init__(self, upbit, stop_loss_percent="-5%", quantity_percent="100%", coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "스탑로스(손절)"
        self.upbit = upbit
        self.stop_loss_percent = stop_loss_percent
        self.quantity_percent = quantity_percent
        self.coin = coin
        self.buy_price = self.get_buy_price()
        self.name = f"스탑로스(손절): {stop_loss_percent} 손절"

    def get_buy_price(self):
        """보유 코인의 평균 매수가 조회"""
        if not hasattr(self, 'coin') or not self.coin:
            print("get_buy_price: coin 값이 설정되지 않음")
            return None

        balances = self.upbit.get_balances()  # ✅ 전체 잔고 조회
        target_currency = self.coin.replace("KRW-", "")  # 예: "KRW-BTC" → "BTC"
        

        for b in balances:
            if b['currency'] == target_currency:
                return float(b['avg_buy_price'])  # ✅ 평균 매수가 반환

        print(f"get_buy_price: {self.coin} 잔고 없음")
        return None  # 코인이 없으면 None 반환


    def run_action(self):
        self.buy_price = self.get_buy_price()
        
        if self.buy_price is None:
            return "매수가격을 가져올 수 없음"

        current_price = pyupbit.get_current_price(self.coin)
        if current_price is None:
            return "현재 가격을 가져올 수 없음"

        # 손절가 계산 (수익률 기준)
        if self.stop_loss_percent.endswith("%"):
            percent = float(self.stop_loss_percent.strip('%')) / 100
            stop_loss_price = self.buy_price * (1 + percent)
        else:
            stop_loss_price = float(self.stop_loss_percent)

        print(f"매수가: {self.buy_price}, 손절가: {stop_loss_price}")
        
        # 현재 가격이 손절가 이하인지 확인
        if current_price <= stop_loss_price:
            balance = self.upbit.get_balance(self.coin)
            if self.quantity_percent.endswith("%"):
                percent = float(self.quantity_percent.strip('%')) / 100
                sell_quantity = balance * percent
            else:
                sell_quantity = float(self.quantity_percent)

            if sell_quantity > balance:
                return "보유 수량 부족"
            
            order_result = self.upbit.sell_market_order(self.coin, sell_quantity)
            return f"손절 실행: {self.coin} - {sell_quantity:.6f}개 @ {current_price} KRW" if order_result else "손절 실패"
        
        return f"손절 조건 미충족: 현재가 {current_price} KRW, 손절가 {stop_loss_price} KRW"
    
    
@ActionRegistry.register("테이크프로핏(익절)")
class TakeProfitAction(Action):
    config_fields = {
        "take_profit_percent": {"label": "익절 기준 수익률 (%)", "type": str, "default": "10%", "ui_type": "line_edit"},
        "quantity_percent": {"label": "판매 수량 (%)", "type": str, "default": "100%", "ui_type": "line_edit"},
    }

    def __init__(self, upbit, take_profit_percent="10%", quantity_percent="100%", coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "테이크프로핏(익절)"
        self.upbit = upbit
        self.take_profit_percent = take_profit_percent
        self.quantity_percent = quantity_percent
        self.coin = coin
        self.buy_price = self.get_buy_price()
        self.name = f"테이크프로핏(익절): {take_profit_percent} 익절"

    def get_buy_price(self):
        """보유 코인의 평균 매수가 조회"""
        if not hasattr(self, 'coin') or not self.coin:
            print("get_buy_price: coin 값이 설정되지 않음")
            return None

        balances = self.upbit.get_balances()  # ✅ 전체 잔고 조회
        target_currency = self.coin.replace("KRW-", "")  # 예: "KRW-BTC" → "BTC"

        for b in balances:
            if b['currency'] == target_currency:
                return float(b['avg_buy_price'])  # ✅ 평균 매수가 반환

        print(f"get_buy_price: {self.coin} 잔고 없음")
        return None  # 코인이 없으면 None 반환
            

    def run_action(self):
        self.buy_price = self.get_buy_price()
        
        if self.buy_price is None:
            return "매수가격을 가져올 수 없음"

        current_price = pyupbit.get_current_price(self.coin)
        if current_price is None:
            return "현재 가격을 가져올 수 없음"

        # 익절가 계산 (수익률 기준)
        if self.take_profit_percent.endswith("%"):
            percent = float(self.take_profit_percent.strip('%')) / 100
            take_profit_price = self.buy_price * (1 + percent)
        else:
            take_profit_price = float(self.take_profit_percent)

        # 현재 가격이 익절가 이상인지 확인
        if current_price >= take_profit_price:
            balance = self.upbit.get_balance(self.coin)
            if self.quantity_percent.endswith("%"):
                percent = float(self.quantity_percent.strip('%')) / 100
                sell_quantity = balance * percent
            else:
                sell_quantity = float(self.quantity_percent)

            if sell_quantity > balance:
                return "보유 수량 부족"
            
            order_result = self.upbit.sell_market_order(self.coin, sell_quantity)
            return f"익절 실행: {self.coin} - {sell_quantity:.6f}개 @ {current_price} KRW" if order_result else "익절 실패"
        
        return f"익절 조건 미충족: 현재가 {current_price} KRW, 익절가 {take_profit_price} KRW"



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
                results = [cond.check_condition() for cond in self.block.conditions]
                self.log_signal.emit(f"Block 실행 결과: {results}")
                
                if all(results):  # 모든 조건이 True일 경우 액션 실행
                    action_result = self.block.action.run_action()
                    self.log_signal.emit(action_result)

            else:
                # ✅ 조건이 없을 경우 액션 바로 실행
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

        self.layout = QHBoxLayout()
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
        
        self.blocks = []
        self.max_blocks = 4
        
        # 로딩 애니메이션 설정
        self.loading_label = QLabel(self)
        self.loading_movie = QMovie('loading.gif')
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setFixedSize(22, 22)


    def add_to_history(self, message):
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
                    print("이 블록에는 이미 액션이 있습니다.")
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
                    print("이 블록에는 이미 액션이 있습니다.")

    def add_block(self):
        if len(self.blocks) >= self.max_blocks:
            print("더 이상 블록을 추가할 수 없습니다 (최대 4개).")
            return

        # 새 블록 생성
        new_block = Block(None, [], 10)
        self.blocks.append(new_block)

        block_frame = QFrame()
        block_frame.setFrameShape(QFrame.StyledPanel)
        block_layout = QHBoxLayout(block_frame)

        # ─── 왼쪽 (라벨 & 리스트) ───
        left_layout = QVBoxLayout()
        
        block_label = QLabel(f"Block {len(self.blocks)}")
        left_layout.addWidget(block_label)

        block_content = QListWidget()
        left_layout.addWidget(block_content)

        block_layout.addLayout(left_layout)

        # ─── 오른쪽 (주기 입력 & 버튼) ───
        right_layout = QVBoxLayout()

        interval_label = QLabel(f"실행 주기 설정 (초)")
        right_layout.addWidget(interval_label)
        
        interval_edit = QLineEdit()
        interval_edit.setPlaceholderText("주기 (초)")
        right_layout.addWidget(interval_edit)

        add_config_btn = QPushButton("+ 조건/액션 추가")
        add_config_btn.clicked.connect(lambda: self.open_add_dialog(new_block, block_content))
        right_layout.addWidget(add_config_btn)

        # 버튼 하단에 추가 여유 공간
        right_layout.addStretch()

        block_layout.addLayout(right_layout)

        # ➡ 왼쪽 레이아웃(0번)에 더 큰 비율(예: 3), 오른쪽 레이아웃(1번)에 더 작은 비율(예: 1)
        block_layout.setStretch(0, 3)
        block_layout.setStretch(1, 1)

        new_block.interval_edit = interval_edit
        self.layout.addWidget(block_frame)
        
        return new_block  # ✅ 생성된 블록 객체 반환

    def run_all_blocks(self, coin):
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

                # 블록 워커 시작
                if block.worker is None:
                    block.worker = BlockWorker(block, block.interval_sec)
                    block.worker.log_signal.connect(self.add_to_history)
                    block.worker.start()

    def stop_all_blocks(self):   
        #loading gif
        self.loading_screen = LoadingDialog()
        self.loading_screen.show_loading()      
        for block in self.blocks:
            if block.worker is not None:
                block.worker.terminate()  # ✅ 강제 종료
                block.worker = None  # ✅ 바로 None 처리하여 즉시 종료 효과

        self.loading_screen.hide_loading()
        self.add_to_history("모든 블록이 종료되었습니다.")

    def closeEvent(self, event):
        self.stop_all_blocks()
        super().closeEvent(event)
        
    def clear_blocks(self):
        """ 기존 블록 초기화 """
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.blocks.clear()
            

