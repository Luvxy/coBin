import pyupbit
import time
from PySide6.QtCore import QObject

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