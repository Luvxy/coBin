import pyupbit
from PySide6.QtCore import QObject

SURVER_URL = "127.0.0.1:8000"

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
        
        if not self.amount.replace('%', '').isdigit():
            return "잘못된 매수 금액 형식"
        
        if self.amount.endswith("%"):  # % 입력 처리
            percent = float(self.amount.strip('%')) / 100
            order_amount = balance * percent
        else:
            order_amount = float(self.amount)
        
        if order_amount > balance:
            return "보유 KRW 부족"
        
        order_result = self.upbit.buy_market_order(self.coin, order_amount)
        return f"시장가 매수 실행: {self.coin} - {order_amount:.2f} KRW" if order_result else "매수 실패"

    def backtest(self, historical_data, balance, holdings, buy_price):
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
        if not self.quantity.replace('%', '').isdigit():
            return "잘못된 매도 수량 형식"
        if self.quantity.endswith("%"):  # % 입력 처리
            percent = float(self.quantity.strip('%')) / 100
            order_quantity = balance * percent
        else:
            order_quantity = float(self.quantity)
        
        if order_quantity > balance:
            return "보유 수량 부족"
        
        order_result = self.upbit.sell_market_order(self.coin, order_quantity)
        return f"시장가 매도 실행: {self.coin} - {order_quantity:.6f}개" if order_result else "매도 실패"

    def backtest(self, historical_data, balance, holdings, buy_price):
        """
        백테스트를 위한 메서드. 시장가 매도를 시뮬레이션합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :param balance: float, 현재 가상 잔고 (KRW)
        :param holdings: float, 현재 보유 수량 (코인)
        :return: list, 매도 결과 및 잔고/보유 수량 업데이트
        """
        results = []
        
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

        # 매도 수량 계산
        if self.quantity.endswith("%"):
            percent = float(self.quantity.strip('%')) / 100
            sell_quantity = holdings * percent
        else:
            sell_quantity = float(self.quantity)

        # 보유 수량 부족 시 매도 불가
        if sell_quantity > holdings:
            results.append({
                "status": "보유 수량 부족",
                "balance": balance,
                "holdings": holdings
            })
            return results

        # 매도 실행
        sell_amount = sell_quantity * current_price
        balance += sell_amount
        holdings -= sell_quantity
        profit = (current_price - buy_price) * sell_quantity
        
        results.append({
            "status": "매도 성공",
            "sell_price": current_price,
            "sell_quantity": sell_quantity,
            "sell_amount": sell_amount,
            "balance": balance,
            "holdings": holdings,
            "profit": profit
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
        if self.price <= 0 or self.quantity <= 0:
            return "잘못된 매수 가격 또는 수량"
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
        if self.price <= 0 or self.quantity <= 0:
            return "잘못된 매도 가격 또는 수량"
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
        
        if not self.stop_loss_percent.replace('%', '').lstrip('-').isdigit():
            return "잘못된 손절 기준 수익률 형식"
        
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
        
        if not self.take_profit_percent.replace('%', '').isdigit():
            return "잘못된 익절 기준 수익률 형식"
        
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

@ActionRegistry.register("블록 활성화/비활성화")
class ToggleBlockAction(Action):
    config_fields = {
        "block_index": {"label": "블록 번호 (1~4)", "type": int, "default": 1, "ui_type": "line_edit"},
        "enable": {"label": "활성화 여부", "type": bool, "default": True, "ui_type": "checkbox"},
    }

    def __init__(self, upbit=None, block_index=1, enable=True):
        super().__init__()
        self.obj_name = "블록 활성화/비활성화"
        self.block_index = block_index
        self.enable = enable
        self.name = f"블록 {block_index} {'활성화' if enable else '비활성화'}"

    def run_action(self, blocks):
        """
        선택한 블록을 활성화 또는 비활성화합니다.
        :param blocks: list, 현재 활성화된 블록 리스트
        """
        if not (1 <= self.block_index <= len(blocks)):
            return f"블록 {self.block_index}은(는) 존재하지 않습니다."

        block = blocks[self.block_index - 1]
        if self.enable:
            block.start()  # 블록 활성화
            return f"블록 {self.block_index}이(가) 활성화되었습니다."
        else:
            block.stop()  # 블록 비활성화
            return f"블록 {self.block_index}이(가) 비활성화되었습니다."

    def backtest(self, historical_data, balance, holdings):
        """
        백테스트에서는 블록 활성화/비활성화가 의미가 없으므로 빈 결과 반환.
        """
        return [{
            "status": "백테스트에서 블록 활성화/비활성화는 지원되지 않습니다.",
            "balance": balance,
            "holdings": holdings
        }]


@ActionRegistry.register("트레일링 스탑")
class TrailingStopAction(Action):
    config_fields = {
        "trailing_percent": {"label": "트레일링 비율 (%)", "type": float, "default": 5.0, "ui_type": "line_edit"},
        "quantity_percent": {"label": "판매 수량 (%)", "type": str, "default": "100%", "ui_type": "line_edit"},
    }

    def __init__(self, upbit, trailing_percent=5.0, quantity_percent="100%", coin="KRW-BTC"):
        super().__init__()
        self.obj_name = "트레일링 스탑"
        self.upbit = upbit
        self.trailing_percent = trailing_percent
        self.quantity_percent = quantity_percent
        self.coin = coin
        self.highest_price = 0.0  # 트레일링 스탑 기준이 되는 최고가
        self.name = f"트레일링 스탑: {trailing_percent}%"
        self.buy_price = self.get_buy_price()

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
        
        if self.trailing_percent <= 0:
            return "잘못된 트레일링 비율"
        if self.highest_price == 0:
            self.highest_price = self.buy_price        
        
        if self.buy_price == 0.0:
            return "매수가격을 가져올 수 없음"
        
        current_price = pyupbit.get_current_price(self.coin)
        if current_price is None:
            return "현재 가격을 가져올 수 없음"

        # 최고가 갱신
        if current_price > self.highest_price:
            self.highest_price = current_price

        # 트레일링 스탑 가격 계산
        trailing_stop_price = self.highest_price * (1 - self.trailing_percent / 100)

        # 현재 가격이 트레일링 스탑 가격 이하로 떨어졌는지 확인
        if current_price <= trailing_stop_price:
            balance = self.upbit.get_balance(self.coin)
            if self.quantity_percent.endswith("%"):
                percent = float(self.quantity_percent.strip('%')) / 100
                sell_quantity = balance * percent
            else:
                sell_quantity = float(self.quantity_percent)

            if sell_quantity > balance:
                return "보유 수량 부족"

            order_result = self.upbit.sell_market_order(self.coin, sell_quantity)
            return f"트레일링 스탑 실행: {self.coin} - {sell_quantity:.6f}개 @ {current_price} KRW" if order_result else "트레일링 스탑 실패"

        return f"트레일링 스탑 조건 미충족: 현재가 {current_price} KRW, 트레일링 스탑가 {trailing_stop_price} KRW"

    def backtest(self, historical_data, balance, holdings, buy_price):
        """
        백테스트를 위한 메서드. 트레일링 스탑 조건을 평가합니다.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :param balance: float, 현재 가상 잔고 (KRW)
        :param holdings: float, 현재 보유 수량 (코인)
        :param buy_price: float, 매수 가격
        :return: list, 매도 결과 및 잔고/보유 수량 업데이트
        """
        results = []
        self.highest_price = buy_price  # 초기 최고가는 매수 가격으로 설정
        
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


        # 최고가 갱신
        if current_price > self.highest_price:
            self.highest_price = current_price

        # 트레일링 스탑 가격 계산
        trailing_stop_price = self.highest_price * (1 - self.trailing_percent / 100)

        # 트레일링 스탑 조건 확인
        if current_price <= trailing_stop_price:
            # 매도 수량 계산
            if self.quantity_percent.endswith("%"):
                percent = float(self.quantity_percent.strip('%')) / 100
                sell_quantity = holdings * percent
            else:
                sell_quantity = float(self.quantity_percent)

            # 보유 수량 부족 시 매도 불가
            if sell_quantity > holdings:
                results.append({
                    "status": "보유 수량 부족",
                    "balance": balance,
                    "holdings": holdings,
                    "buy_price": buy_price
                })
                return results

            # 매도 실행
            sell_amount = sell_quantity * current_price
            balance += sell_amount
            holdings -= sell_quantity
            profit = (current_price - buy_price) * sell_quantity

            results.append({
                "status": "매도 성공",
                "sell_price": current_price,
                "sell_quantity": sell_quantity,
                "sell_amount": sell_amount,
                "balance": balance,
                "holdings": holdings,
                "buy_price": None,  # 매도 후 매수 가격 초기화
                "profit": profit
            })
            return results

        # 조건 미충족
        results.append({
            "status": "트레일링 스탑 조건 미충족",
            "balance": balance,
            "holdings": holdings,
            "buy_price": buy_price
        })

        return results

@ActionRegistry.register("이메일 전송")
class EmailAction(Action):
    config_fields = {
        "recipient": {"label": "받는 사람 이메일", "type": str, "default": "", "ui_type": "line_edit"},
        "subject": {"label": "이메일 제목", "type": str, "default": "", "ui_type": "line_edit"},
        "message": {"label": "이메일 내용", "type": str, "default": "", "ui_type": "text_edit"},
    }

    def __init__(self, upbit, recipient="", subject="", message=""):
        super().__init__()
        self.obj_name = "이메일 전송"
        self.recipient = recipient
        self.subject = subject
        self.message = message
        self.upbit = upbit
        self.name = f"이메일 전송: {recipient}"
        
    def run_action(self):
        """
        서버로 이메일 전송 요청을 보냅니다.
        """
        import requests

        if not self.recipient or not self.subject or not self.message:
            return "이메일 정보가 부족합니다"

        # 서버의 이메일 전송 API URL
        api_url = f"http://{SURVER_URL}/api/email/send/"

        # 요청 데이터
        payload = {
            "recipient": self.recipient,
            "subject": self.subject,
            "message": self.message
        }

        try:
            # POST 요청으로 이메일 전송
            response = requests.post(api_url, json=payload)

            # 응답 처리
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    return f"이메일 전송 성공: {self.recipient}"
                else:
                    return f"이메일 전송 실패: {result.get('message', '알 수 없는 오류')}"
            else:
                return f"이메일 전송 실패: 서버 오류 (HTTP {response.status_code})"
        except Exception as e:
            return f"이메일 전송 실패: {str(e)}"
    
    def backtest(self, historical_data, balance, holdings):
        """
        백테스트를 위한 메서드. 이메일 전송은 백테스트에서 의미가 없으므로 빈 결과 반환.
        :param historical_data: DataFrame, 과거 데이터를 포함한 DataFrame
        :param balance: float, 현재 가상 잔고 (KRW)
        :param holdings: float, 현재 보유 수량 (코인)
        :return: list, 빈 결과
        """
        return [{
            "status": "백테스트에서 이메일 전송은 지원되지 않습니다.",
            "balance": balance,
            "holdings": holdings
        }]