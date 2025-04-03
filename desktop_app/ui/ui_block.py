import sys
import time
import os
import json
import pyupbit
import requests
from PySide6.QtCore import Qt, QThread, Signal, QObject, QMutex, QWaitCondition, QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel,
    QFrame, QDialog, QDialogButtonBox, QComboBox, QLineEdit, QCheckBox, QHBoxLayout,
    QGroupBox, QMessageBox
)
from PySide6.QtGui import QMovie
from main import LoadingDialog

SURVER_URL = "127.0.0.1:8000"

from PySide6.QtCore import QThread, Signal


# 백테스트 작업을 수행하는 스레드 클래스
import json
from datetime import datetime

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
                                    holdings=holdings
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
        self.current_data = None  # 현재 데이터

    def check_condition(self) -> bool:
        if self.current_data is not None:
            # 현재 데이터 기반으로 조건 평가
            is_bullish = self.current_data['open'] < self.current_data['close']
            return is_bullish if self.target_type == "양봉" else not is_bullish

        # 백테스트가 아닌 경우, 실시간 데이터 가져오기
        df = pyupbit.get_ohlcv(self.coin, interval=self.interval, count=self.candle_index + 1)
        if df is None or df.empty or len(df) <= self.candle_index:
            print("캔들 데이터를 가져올 수 없음")
            return False

        target_candle = df.iloc[-(self.candle_index + 1)]
        is_bullish = target_candle['open'] < target_candle['close']
        return is_bullish if self.target_type == "양봉" else not is_bullish
    
    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        for index in range(len(historical_data)):
            if index < self.candle_index:
                # 데이터가 부족한 경우 False로 처리
                results.append(False)
                continue

            target_candle = historical_data.iloc[index - self.candle_index]
            is_bullish = target_candle['open'] < target_candle['close']
            result = is_bullish if self.target_type == "양봉" else not is_bullish
            results.append(result)
        return results

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
    
    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 조건을 평가합니다.
        :param historical_data: DataFrame, 거래량 데이터를 포함한 과거 데이터
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        for index, row in historical_data.iterrows():
            current_volume = row['volume']
            result = current_volume >= self.volume_threshold if self.check_type == "이상" else current_volume <= self.volume_threshold
            results.append(result)
        return results

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

    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        for index, row in historical_data.iterrows():
            current_price = row['close']
            result = current_price >= self.price_threshold if self.check_type == "이상" else current_price <= self.price_threshold
            results.append(result)
        return results


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

    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        for index in range(1, len(historical_data)):
            prev_close = historical_data.iloc[index - 1]['close']
            current_close = historical_data.iloc[index]['close']
            price_change = (current_close - prev_close) / prev_close * 100
            result = price_change >= self.change_threshold if self.check_type == "이상" else price_change <= self.change_threshold
            results.append(result)
        results.insert(0, False)  # 첫 번째 데이터는 비교할 이전 데이터가 없으므로 False
        return results


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
    
    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        ma_series = historical_data['close'].rolling(window=self.ma_days).mean()

        for index in range(len(historical_data)):
            if index < self.ma_days:
                # 이동평균선을 계산할 데이터가 부족한 경우 False로 처리
                results.append(False)
                continue

            current_price = historical_data.iloc[index]['close']
            current_ma = ma_series.iloc[index]
            prev_ma = ma_series.iloc[index - 1]

            if self.check_type == "상향 돌파":
                result = current_price > current_ma > prev_ma
            elif self.check_type == "하향 돌파":
                result = current_price < current_ma < prev_ma
            else:
                result = False

            results.append(result)

        return results
    
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

    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        for index, row in historical_data.iterrows():
            # 시간 정보 추출 (예: '2023-03-01 09:30:00' → 9)
            current_hour = row.name.hour
            result = self.start_hour <= current_hour <= self.end_hour
            results.append(result)
        return results

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
        
    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        for index in range(len(historical_data)):
            if index < max(self.candle1, self.candle2):
                # 비교할 데이터가 부족한 경우 False로 처리
                results.append(False)
                continue

            high1 = historical_data.iloc[index - self.candle1]['high']
            low1 = historical_data.iloc[index - self.candle1]['low']
            high2 = historical_data.iloc[index - self.candle2]['high']
            low2 = historical_data.iloc[index - self.candle2]['low']
            current_price = historical_data.iloc[index]['close']

            if self.compare_type == "최고가vs최저가":
                result = high1 > low2
            elif self.compare_type == "최고가vs최고가":
                result = high1 > high2
            elif self.compare_type == "최저가vs최저가":
                result = low1 > low2
            elif self.compare_type == "최고가vs현재가":
                result = high1 > current_price
            elif self.compare_type == "최저가vs현재가":
                result = low1 > current_price
            elif self.compare_type == "현재가vs최고가":
                result = current_price > high1
            elif self.compare_type == "현재가vs최저가":
                result = current_price > low1
            else:
                result = False

            results.append(result)
        return results


@ConditionRegistry.register("분할매수 조건")
class CheckDCACondition(Condition):
    config_fields = {
        "max_buy_count": {"label": "최대 매수 횟수", "type": int, "default": 3, "ui_type": "line_edit"},
        "price_drop_percent": {"label": "매수 기준 하락률 (%)", "type": float, "default": 2.0, "ui_type": "line_edit"},
    }

    def __init__(self, max_buy_count=3, price_drop_percent=2.0, coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "분할매수 조건"
        self.max_buy_count = max_buy_count
        self.price_drop_percent = price_drop_percent
        self.coin = coin
        self.buy_count = 0  # 현재 매수 횟수
        self.last_buy_price = None  # 마지막 매수가 저장
        self.name = f"최대 {max_buy_count}회 매수, {price_drop_percent}% 하락 시 매수"

    def check_condition(self) -> bool:
        if self.buy_count >= self.max_buy_count:
            return False  # 최대 횟수 초과

        current_price = pyupbit.get_current_price(self.coin)
        if current_price is None:
            return False

        if self.last_buy_price is None:
            self.last_buy_price = current_price
            return True  # 첫 매수는 무조건 실행

        price_drop = (self.last_buy_price - current_price) / self.last_buy_price * 100
        if price_drop >= self.price_drop_percent:
            return True

        return False

    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        buy_count = 0
        last_buy_price = None

        for index, row in historical_data.iterrows():
            if buy_count >= self.max_buy_count:
                # 최대 매수 횟수를 초과한 경우 False로 처리
                results.append(False)
                continue

            current_price = row['close']

            if last_buy_price is None:
                # 첫 매수는 무조건 True
                last_buy_price = current_price
                results.append(True)
                buy_count += 1
            else:
                # 가격 하락률 계산
                price_drop = (last_buy_price - current_price) / last_buy_price * 100
                if price_drop >= self.price_drop_percent:
                    results.append(True)
                    last_buy_price = current_price
                    buy_count += 1
                else:
                    results.append(False)

        return results


@ConditionRegistry.register("DTC 기술 지표 조건")
class CheckDTCIndicatorCondition(Condition):
    config_fields = {
        "rsi_threshold": {"label": "RSI 기준값", "type": float, "default": 30.0, "ui_type": "line_edit"},
    }

    def __init__(self, rsi_threshold=30.0, coin="KRW-BTC", interval="minute30"):
        super().__init__()
        self.obj_name = "DTC 기술 지표 조건"
        self.rsi_threshold = rsi_threshold
        self.coin = coin
        self.interval = interval
        self.name = f"RSI {rsi_threshold} 이하"

    def check_condition(self) -> bool:
        df = pyupbit.get_ohlcv(self.coin, interval=self.interval, count=14)
        if df is None or df.empty:
            return False

        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        current_rsi = rsi.iloc[-1]
        return current_rsi <= self.rsi_threshold
    
    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 RSI 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        delta = historical_data["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        for index in range(len(historical_data)):
            if index < 14:
                # RSI를 계산할 데이터가 부족한 경우 False로 처리
                results.append(False)
                continue

            current_rsi = rsi.iloc[index]
            result = current_rsi <= self.rsi_threshold
            results.append(result)

        return results

@ConditionRegistry.register("DTC 변동성 조건")
class CheckDTCVolatilityCondition(Condition):
    config_fields = {
        "volatility_threshold": {"label": "변동성 기준 (%)", "type": float, "default": 2.0, "ui_type": "line_edit"},
    }

    def __init__(self, volatility_threshold=2.0, coin="KRW-BTC", interval="minute30"):
        super().__init__()
        self.obj_name = "DTC 변동성 조건"
        self.volatility_threshold = volatility_threshold
        self.coin = coin
        self.interval = interval
        self.name = f"변동성 {volatility_threshold}% 이상"

    def check_condition(self) -> bool:
        df = pyupbit.get_ohlcv(self.coin, interval=self.interval, count=2)
        if df is None or df.empty or len(df) < 2:
            return False

        prev_close = df.iloc[-2]["close"]
        current_close = df.iloc[-1]["close"]
        price_change = abs(current_close - prev_close) / prev_close * 100
        return price_change >= self.volatility_threshold

    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 변동성 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        for index in range(1, len(historical_data)):
            prev_close = historical_data.iloc[index - 1]["close"]
            current_close = historical_data.iloc[index]["close"]
            price_change = abs(current_close - prev_close) / prev_close * 100
            result = price_change >= self.volatility_threshold
            results.append(result)
        results.insert(0, False)  # 첫 번째 데이터는 비교할 이전 데이터가 없으므로 False
        return results

@ConditionRegistry.register("RSI 기준 확인")
class CheckRSICondition(Condition):
    config_fields = {
        "rsi_threshold": {"label": "RSI 기준값", "type": float, "default": 30.0, "ui_type": "line_edit"},
        "check_type": {"label": "비교 유형", "type": str, "default": "이하", "ui_type": "dropdown", "options": ["이상", "이하"]},
    }

    def __init__(self, rsi_threshold=30.0, check_type="이하", coin="KRW-BTC", interval="minute30"):
        super().__init__()
        self.obj_name = "RSI 기준 확인"
        self.rsi_threshold = rsi_threshold
        self.check_type = check_type
        self.coin = coin
        self.interval = interval
        self.name = f"RSI {rsi_threshold} {check_type} 확인"

    def check_condition(self) -> bool:
        df = pyupbit.get_ohlcv(self.coin, interval=self.interval, count=14)
        if df is None or df.empty:
            return False

        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        current_rsi = rsi.iloc[-1]
        return current_rsi >= self.rsi_threshold if self.check_type == "이상" else current_rsi <= self.rsi_threshold

    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 RSI 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        delta = historical_data["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        for index in range(len(historical_data)):
            if index < 14:
                # RSI를 계산할 데이터가 부족한 경우 False로 처리
                results.append(False)
                continue

            current_rsi = rsi.iloc[index]
            result = current_rsi >= self.rsi_threshold if self.check_type == "이상" else current_rsi <= self.rsi_threshold
            results.append(result)

        return results


@ConditionRegistry.register("볼린저밴드 돌파 확인")
class CheckBollingerBandCondition(Condition):
    config_fields = {
        "band_type": {"label": "밴드 유형", "type": str, "default": "상한 돌파", "ui_type": "dropdown", "options": ["상한 돌파", "하한 돌파"]},
        "period": {"label": "이동평균 기간", "type": int, "default": 20, "ui_type": "line_edit"},
        "std_dev": {"label": "표준편차 배수", "type": float, "default": 2.0, "ui_type": "line_edit"},
    }

    def __init__(self, band_type="상한 돌파", period=20, std_dev=2.0, coin="KRW-BTC", interval="minute30"):
        super().__init__()
        self.obj_name = "볼린저밴드 돌파 확인"
        self.band_type = band_type
        self.period = period
        self.std_dev = std_dev
        self.coin = coin
        self.name = f"볼린저밴드 {band_type} 확인"
        self.interval = interval

    def check_condition(self) -> bool:
        df = pyupbit.get_ohlcv(self.coin, interval=self.interval, count=self.period + 1)
        if df is None or df.empty or len(df) < self.period:
            return False

        moving_avg = df["close"].rolling(window=self.period).mean()
        std_dev = df["close"].rolling(window=self.period).std()
        upper_band = moving_avg + (std_dev * self.std_dev)
        lower_band = moving_avg - (std_dev * self.std_dev)
        current_price = df.iloc[-1]["close"]

        if self.band_type == "상한 돌파":
            return current_price > upper_band.iloc[-1]
        else:
            return current_price < lower_band.iloc[-1]

    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 볼린저 밴드 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        moving_avg = historical_data["close"].rolling(window=self.period).mean()
        std_dev = historical_data["close"].rolling(window=self.period).std()
        upper_band = moving_avg + (std_dev * self.std_dev)
        lower_band = moving_avg - (std_dev * self.std_dev)

        for index in range(len(historical_data)):
            if index < self.period:
                # 이동평균선을 계산할 데이터가 부족한 경우 False로 처리
                results.append(False)
                continue

            current_price = historical_data.iloc[index]["close"]

            if self.band_type == "상한 돌파":
                result = current_price > upper_band.iloc[index]
            elif self.band_type == "하한 돌파":
                result = current_price < lower_band.iloc[index]
            else:
                result = False

            results.append(result)

        return results


@ConditionRegistry.register("피보나치 되돌림 확인")
class CheckFibonacciRetracementCondition(Condition):
    config_fields = {
        "retracement_level": {
            "label": "피보나치 되돌림 비율",
            "type": float,
            "default": 0.618,
            "ui_type": "dropdown",
            "options": [str(x) for x in [0.236, 0.382, 0.5, 0.618, 0.786]],  # 🔥 문자열 변환!
        },
        "check_type": {
            "label": "확인 유형",
            "type": str,
            "default": "지지선 확인",
            "ui_type": "dropdown",
            "options": ["지지선 확인", "저항선 확인"],
        },
    }

    def __init__(self, retracement_level=0.618, check_type="지지선 확인", coin="KRW-BTC", interval="minute30"):
        super().__init__()
        self.obj_name = "피보나치 되돌림 확인"
        self.retracement_level = float(retracement_level)
        self.check_type = check_type
        self.coin = coin
        self.interval = interval
        self.name = f"피보나치 {retracement_level} {check_type}"

    def check_condition(self) -> bool:
        df = pyupbit.get_ohlcv(self.coin, interval=self.interval, count=100)
        if df is None or df.empty:
            return False

        high_price = df["high"].max()
        low_price = df["low"].min()
        retracement_price = low_price + (high_price - low_price) * self.retracement_level
        current_price = df.iloc[-1]["close"]

        if self.check_type == "지지선 확인":
            return current_price <= retracement_price
        else:
            return current_price >= retracement_price
        
    def backtest(self, historical_data) -> list:
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 피보나치 되돌림 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :return: list, 각 데이터 포인트에 대한 조건 평가 결과 (True/False)
        """
        results = []
        high_price = historical_data["high"].max()
        low_price = historical_data["low"].min()
        retracement_price = low_price + (high_price - low_price) * self.retracement_level

        for index, row in historical_data.iterrows():
            current_price = row["close"]

            if self.check_type == "지지선 확인":
                result = current_price <= retracement_price
            elif self.check_type == "저항선 확인":
                result = current_price >= retracement_price
            else:
                result = False

            results.append(result)

        return results


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
        if krwb is None:
            return "API 연결 실패"
        
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

    def backtest(self, historical_data, balance, holdings):
        # 마지막 데이터 가져오기
        last_row = historical_data.iloc[-1]
        current_price = last_row["close"]

        # 매수 금액 계산
        if self.amount.endswith("%"):
            percent = float(self.amount.strip('%')) / 100
            buy_amount = balance * percent
        else:
            buy_amount = float(self.amount)

        # 잔고 부족 시 매수 불가
        if buy_amount > balance or buy_amount <= 0:
            return [{
                "status": "잔고 부족",
                "balance": balance,
                "holdings": holdings,
                "buy_price": None
            }]

        # 매수 실행
        buy_quantity = buy_amount / current_price
        balance -= buy_amount
        holdings += buy_quantity
        buy_price = current_price

        # 매수 성공 결과 반환
        return [{
            "status": "매수 성공",
            "buy_price": buy_price,
            "buy_quantity": buy_quantity,
            "buy_amount": buy_amount,
            "balance": balance,
            "holdings": holdings
        }]


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

    def backtest(self, historical_data, balance, holdings):
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 가상 지정가 매도를 시뮬레이션합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :param balance: float, 현재 가상 잔고 (KRW)
        :param holdings: float, 현재 보유 수량 (코인)
        :return: list, 매도 결과 및 잔고/보유 수량 업데이트
        """
        results = []
        
        # 마지막 데이터 가져오기
        last_row = historical_data.iloc[-1]
        current_price = last_row["close"]

        # 지정가 매도 조건 확인
        if current_price >= self.price:
            # 매도 수량 계산
            sell_quantity = self.quantity

            # 보유 수량 부족 시 매도 불가
            if sell_quantity > holdings:
                results.append({
                    "status": "보유 수량 부족",
                    "balance": balance,
                    "holdings": holdings
                })

            # 매도 실행
            sell_amount = sell_quantity * self.price
            balance += sell_amount
            holdings -= sell_quantity
            results.append({
                "status": "매도 성공",
                "sell_price": self.price,
                "sell_quantity": sell_quantity,
                "sell_amount": sell_amount,
                "balance": balance,
                "holdings": holdings
            })
        else:
            # 매도 조건 미충족
            results.append({
                "status": "매도 조건 미충족",
                "balance": balance,
                "holdings": holdings
            })

        return results


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

    def backtest(self, historical_data, balance):
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 가상 지정가 매수를 시뮬레이션합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :param balance: float, 현재 가상 잔고
        :return: list, 매수 결과 및 잔고 업데이트
        """
        results = []
        
        # 마지막 데이터 가져오기
        last_row = historical_data.iloc[-1]
        current_price = last_row["close"]

        # 지정가 매수 조건 확인
        if current_price <= self.price:
            # 매수 금액 계산
            buy_amount = self.price * self.quantity

            # 잔고 부족 시 매수 불가
            if buy_amount > balance:
                results.append({"status": "잔고 부족", "balance": balance})

            # 매수 실행
            balance -= buy_amount
            results.append({
                "status": "매수 성공",
                "buy_price": self.price,
                "buy_quantity": self.quantity,
                "buy_amount": buy_amount,
                "balance": balance
            })
        else:
            # 매수 조건 미충족
            results.append({"status": "매수 조건 미충족", "balance": balance})

        return results

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

    def backtest(self, historical_data, balance, holdings):
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 가상 지정가 매도를 시뮬레이션합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :param balance: float, 현재 가상 잔고 (KRW)
        :param holdings: float, 현재 보유 수량 (코인)
        :return: list, 매도 결과 및 잔고/보유 수량 업데이트
        """
        results = []
        # 마지막 데이터 가져오기
        last_row = historical_data.iloc[-1]
        current_price = last_row["close"]
        

        # 지정가 매도 조건 확인
        if current_price >= self.price:
            # 매도 수량 계산
            sell_quantity = self.quantity

            # 보유 수량 부족 시 매도 불가
            if sell_quantity > holdings:
                results.append({"status": "보유 수량 부족", "balance": balance, "holdings": holdings})

            # 매도 실행
            sell_amount = sell_quantity * self.price
            balance += sell_amount
            holdings -= sell_quantity
            results.append({
                "status": "매도 성공",
                "sell_price": self.price,
                "sell_quantity": sell_quantity,
                "sell_amount": sell_amount,
                "balance": balance,
                "holdings": holdings
            })
        else:
            # 매도 조건 미충족
            results.append({"status": "매도 조건 미충족", "balance": balance, "holdings": holdings})

        return results


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
            return 0.0  # ✅ None 대신 0.0 반환

        balances = self.upbit.get_balances() or []  # ✅ None이면 빈 리스트 반환
        target_currency = self.coin.replace("KRW-", "")  # 예: "KRW-BTC" → "BTC"

        for b in balances:
            if b.get('currency') == target_currency:  # ✅ get() 사용하여 KeyError 방지
                return float(b.get('avg_buy_price', 0.0))  # ✅ KeyError 방지 + None이면 0.0 반환

        return 0.0  # ✅ None 대신 0.0 반환


    def run_action(self):
        self.buy_price = self.get_buy_price()
        
        if self.buy_price == 0.0:
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
    
    def backtest(self, historical_data, balance, holdings, buy_price):
        """
        백테스트를 위한 메서드. 마지막 데이터만 사용하여 손절 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :param balance: float, 현재 가상 잔고 (KRW)
        :param holdings: float, 현재 보유 수량 (코인)
        :param buy_price: float, 매수 가격
        :return: dict, 손절 결과 및 잔고/보유 수량 업데이트
        """
        # 마지막 데이터 가져오기
        last_row = historical_data.iloc[-1]
        current_price = last_row["close"]

        # buy_price가 None이면 손절 조건을 평가하지 않음
        if buy_price is None:
            return [{
                "status": "매수 가격 없음",
                "balance": balance,
                "holdings": holdings,
                "buy_price": buy_price
            }]

        # 손절가 계산
        if self.stop_loss_percent.endswith("%"):
            percent = float(self.stop_loss_percent.strip('%')) / 100
            stop_loss_price = buy_price * (1 + percent)
        else:
            stop_loss_price = float(self.stop_loss_percent)

        # 손절 조건 확인
        if current_price <= stop_loss_price:
            # 매도 수량 계산
            if self.quantity_percent.endswith("%"):
                percent = float(self.quantity_percent.strip('%')) / 100
                sell_quantity = holdings * percent
            else:
                sell_quantity = float(self.quantity_percent)

            # 보유 수량 부족 시 매도 불가
            if sell_quantity > holdings:
                return [{
                    "status": "보유 수량 부족",
                    "balance": balance,
                    "holdings": holdings,
                    "buy_price": buy_price
                }]

            # 매도 실행
            sell_amount = sell_quantity * current_price
            balance += sell_amount
            holdings -= sell_quantity
            profit = (current_price - buy_price) * sell_quantity

            return [{
                "status": "매도 성공",
                "sell_price": current_price,
                "sell_quantity": sell_quantity,
                "sell_amount": sell_amount,
                "balance": balance,
                "holdings": holdings,
                "buy_price": None,  # 손절 후 매수 가격 초기화
                "profit": profit
            }]

        # 손절 조건 미충족
        return [{
            "status": "손절 조건 미충족",
            "balance": balance,
            "holdings": holdings,
            "buy_price": buy_price
        }]

    
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
            return 0.0  # ✅ None 대신 0.0 반환

        balances = self.upbit.get_balances() or []  # ✅ None이면 빈 리스트 반환
        target_currency = self.coin.replace("KRW-", "")  # 예: "KRW-BTC" → "BTC"

        for b in balances:
            if b.get('currency') == target_currency:  # ✅ get() 사용하여 KeyError 방지
                return float(b.get('avg_buy_price', 0.0))  # ✅ KeyError 방지 + None이면 0.0 반환

        return 0.0  # ✅ None 대신 0.0 반환
            

    def run_action(self):
        self.buy_price = self.get_buy_price()
        
        if self.buy_price == 0.0:
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

    def backtest(self, historical_data, balance, holdings, buy_price):
        """
        백테스트를 위한 메서드. 마지막 데이터만 사용하여 익절 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :param balance: float, 현재 가상 잔고 (KRW)
        :param holdings: float, 현재 보유 수량 (코인)
        :param buy_price: float, 매수 가격
        :return: dict, 익절 결과 및 잔고/보유 수량 업데이트
        """
        # 마지막 데이터 가져오기
        last_row = historical_data.iloc[-1]
        current_price = last_row["close"]

        # buy_price가 None이면 익절 조건을 평가하지 않음
        if buy_price is None:
            return [{
                "status": "매수 가격 없음",
                "balance": balance,
                "holdings": holdings,
                "buy_price": buy_price
            }]

        # 익절가 계산
        if self.take_profit_percent.endswith("%"):
            percent = float(self.take_profit_percent.strip('%')) / 100
            take_profit_price = buy_price * (1 + percent)
        else:
            take_profit_price = float(self.take_profit_percent)

        # 익절 조건 확인
        if current_price >= take_profit_price:
            # 매도 수량 계산
            if self.quantity_percent.endswith("%"):
                percent = float(self.quantity_percent.strip('%')) / 100
                sell_quantity = holdings * percent
            else:
                sell_quantity = float(self.quantity_percent)

            # 보유 수량 부족 시 매도 불가
            if sell_quantity > holdings:
                return [{
                    "status": "보유 수량 부족",
                    "balance": balance,
                    "holdings": holdings,
                    "buy_price": buy_price
                }]

            # 매도 실행
            sell_amount = sell_quantity * current_price
            balance += sell_amount
            holdings -= sell_quantity
            profit = (current_price - buy_price) * sell_quantity

            return [{
                "status": "매도 성공",
                "sell_price": current_price,
                "sell_quantity": sell_quantity,
                "sell_amount": sell_amount,
                "balance": balance,
                "holdings": holdings,
                "buy_price": None,  # 익절 후 매수 가격 초기화
                "profit": profit
            }]

        # 익절 조건 미충족
        return [{
            "status": "익절 조건 미충족",
            "balance": balance,
            "holdings": holdings,
            "buy_price": buy_price
        }]


@ActionRegistry.register("분할매수 실행")
class DCABuyAction(Action):
    config_fields = {
        "buy_amount": {"label": "매수 금액 (KRW)", "type": float, "default": 10000.0, "ui_type": "line_edit"},
    }

    def __init__(self, upbit, buy_amount=10000.0, coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "분할매수 실행"
        self.upbit = upbit
        self.buy_amount = buy_amount
        self.coin = coin
        self.name = f"분할매수 실행: {buy_amount} KRW"

    def run_action(self):
        krw_balance = self.upbit.get_balance("KRW")
        if krw_balance < self.buy_amount:
            return "KRW 잔고 부족"

        order_result = self.upbit.buy_market_order(self.coin, self.buy_amount)
        if order_result:
            return f"분할매수 실행: {self.coin} - {self.buy_amount} KRW"
        else:
            return "분할매수 실패"

    def backtest(self, historical_data, balance, holdings):
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 분할 매수를 시뮬레이션합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :param balance: float, 현재 가상 잔고 (KRW)
        :return: list, 매수 결과 및 잔고 업데이트
        """
        results = []
        
        # 마지막 데이터 가져오기
        last_row = historical_data.iloc[-1]
        current_price = last_row["close"]

        # 매수 금액 확인
        if self.buy_amount > balance:
            results.append({
                "status": "잔고 부족",
                "balance": balance,
                "holdings": holdings
            })

        # 매수 실행
        buy_quantity = self.buy_amount / current_price
        balance -= self.buy_amount
        holdings += buy_quantity

        results.append({
            "status": "매수 성공",
            "buy_price": current_price,
            "buy_quantity": buy_quantity,
            "buy_amount": self.buy_amount,
            "balance": balance,
            "holdings": holdings
        })

        return results


@ActionRegistry.register("DTC 동적 분할매수")
class DTCBuyAction(Action):
    config_fields = {
        "base_buy_amount": {"label": "기본 매수 금액 (KRW)", "type": float, "default": 10000.0, "ui_type": "line_edit"},
        "volatility_adjustment": {"label": "변동성 조정 비율 (%)", "type": float, "default": 20.0, "ui_type": "line_edit"},
    }

    def __init__(self, upbit, base_buy_amount=10000.0, volatility_adjustment=20.0, coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "DTC 동적 분할매수"
        self.upbit = upbit
        self.base_buy_amount = base_buy_amount
        self.volatility_adjustment = volatility_adjustment
        self.coin = coin
        self.name = f"DTC 동적 분할매수: {base_buy_amount} KRW"

    def run_action(self):
        df = pyupbit.get_ohlcv(self.coin, interval="minute30", count=2)
        if df is None or df.empty or len(df) < 2:
            return "변동성 데이터를 가져올 수 없음"

        prev_close = df.iloc[-2]["close"]
        current_close = df.iloc[-1]["close"]
        price_change = abs(current_close - prev_close) / prev_close * 100

        adjusted_amount = self.base_buy_amount * (1 + (self.volatility_adjustment / 100 if price_change > 1 else -self.volatility_adjustment / 100))
        krw_balance = self.upbit.get_balance("KRW")
        if krw_balance < adjusted_amount:
            return "KRW 잔고 부족"

        order_result = self.upbit.buy_market_order(self.coin, adjusted_amount)
        return f"DTC 매수 실행: {self.coin} - {adjusted_amount:.2f} KRW" if order_result else "DTC 매수 실패"

    def backtest(self, historical_data, balance, holdings):
        """
        백테스트를 위한 메서드. 주어진 데이터셋에서 동적 분할 매수를 시뮬레이션합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :param balance: float, 현재 가상 잔고 (KRW)
        :return: list, 매수 결과 및 잔고 업데이트
        """
        results = []
        
        if len(historical_data) < 2:
            return [{
                "status": "데이터 부족",
                "balance": balance,
                "holdings": holdings
            }]
        
        # 마지막 데이터 가져오기
        index = -1
        last_row = historical_data.iloc[index]
        current_price = last_row["close"]        
        
        prev_close = historical_data.iloc[index - 1]["close"]
        current_close = historical_data.iloc[index]["close"]
        price_change = abs(current_close - prev_close) / prev_close * 100

        # 변동성에 따른 매수 금액 조정
        if price_change > 1:
            adjusted_amount = self.base_buy_amount * (1 + self.volatility_adjustment / 100)
        else:
            adjusted_amount = self.base_buy_amount * (1 - self.volatility_adjustment / 100)

        # 잔고 부족 시 매수 불가
        if adjusted_amount > balance:
            results.append({
                "status": "잔고 부족",
                "balance": balance,
                "holdings": holdings
            })

        # 매수 실행
        buy_quantity = adjusted_amount / current_close
        balance -= adjusted_amount
        holdings += buy_quantity

        results.append({
            "index": index,
            "status": "매수 성공",
            "buy_price": current_close,
            "buy_quantity": buy_quantity,
            "buy_amount": adjusted_amount,
            "balance": balance,
            "holdings": holdings
        })

        return results


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