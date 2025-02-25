import time
from colorama import Fore, Back, Style
import pyupbit
import time
import json
import datetime
import schedule
import os
import functions

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
upbit = pyupbit.Upbit(access_key, secret_key)

# print(pyupbit.get_current_price("KRW-BTC")) # 현재가격
# print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
# print(upbit.get_balance("KRW"))         # 보유 현금 조회
# print(upbit.get_balances())     # 전체 자산 조회
# print(upbit.buy_market_order("KRW-XRP", 100   00)) # 시장가 매수
# print(upbit.sell_market_order("KRW-XRP", 30)) # 시장가 매도
# print(upbit.get_order("KRW-LTC", state="done")) # 체결 내역 조회

# 사용자가 제외하고 싶은 코인 목록
excluded_tickers = ["KRW-BTC", "KRW-EOS", "KRW-XRP", "KRW-SHIB", "KRW-DOGE", "KRW-ALGO"]  # 예를 들어 비트코인, 이더리움, 리플 제외

market_value = None

def get_highest_trading_amount_coin():
    global market_value
    try:
        tickers = pyupbit.get_tickers(fiat="KRW")
        tickers = [ticker for ticker in tickers if ticker not in excluded_tickers]
        coin_data = []

        for ticker in tickers:
            data = pyupbit.get_ohlcv(ticker, interval="minute60", count=6)
            if data is not None:
                # 6시간 동안의 총 거래대금 계산
                trading_amount = (data['close'] * data['volume']).sum()
                # 가격 변동 계산
                price_change = ((data['close'].iloc[-1] - data['close'].iloc[0]) / data['close'].iloc[0]) * 100

                # 가격 하락이 5% 미만인 경우에만 목록에 추가
                if price_change >= -1:
                    coin_data.append((ticker, trading_amount))

        # 거래대금이 높은 순으로 정렬
        coin_data.sort(key=lambda x: x[1], reverse=True)

        if coin_data:
            top_coin = coin_data[0][0]
            market_value = top_coin  # 최고 거래대금 코인을 전역 변수에 저장
    except Exception as e:
        print("Error fetching or processing data:", e)

def wait_until_next_quarter():
    """
    Waits until the next quarter hour mark (:00, :15, :30, :45) based on the current time.
    """
    now = datetime.datetime.now()
    current_minute = now.minute
    current_second = now.second
    
    # Calculate how many minutes to wait until the next quarter
    if current_minute < 15:
        minutes_to_wait = 15 - current_minute
    elif current_minute < 30:
        minutes_to_wait = 30 - current_minute
    elif current_minute < 45:
        minutes_to_wait = 45 - current_minute
    else:
        minutes_to_wait = 60 - current_minute
    
    # Convert minutes to seconds and subtract the current seconds to synchronize to the exact quarter
    seconds_to_wait = minutes_to_wait * 60 - current_second
    
    # Wait for the calculated amount of seconds
    time.sleep(seconds_to_wait)

def save_trade_info(operation, details):
    """Saves trade information to a JSON file."""
    try:
        # Attempt to load existing data from the config.json file
        with open('config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, create a new dictionary
        config = {}

    # Append the new trade information
    if operation in config:
        config[operation].append(details)
    else:
        config[operation] = [details]

    # Write the updated configuration back to the file
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)


is_order = False # 주문 상태
traling_on = False # 트레일링 트리거
exit_price = None # 손절가
buy_price = None # 매수가
set_benefit = 0.7 # 이익 %
traling_benefit = 0.7 # 트레일링 스탑 이익 %
traling_stop = 0.7 # 트레일링 스탑 %
max_price = 0
stop = 0 # 손절 %
get_highest_trading_amount_coin()
# wait_until_next_quarter()
time.sleep(20)
market = market_value
print(f"거래 코인: {market}")

while True:
    data_list = pyupbit.get_ohlcv(market, interval="minute15", count=3)
    cash = upbit.get_balance("KRW")
    
    candle_0 = data_list.iloc[2]
    candle_1 = data_list.iloc[1]
    candle_2 = data_list.iloc[0]

    now_price = pyupbit.get_current_price(market)
    volume = upbit.get_balance(market)
    
    if is_order:
        benefit = 100*(now_price-buy_price)/buy_price
        print(f"현재 이익: {benefit},현재가: {now_price}, 손절가: {exit_price}, 구매가:{buy_price}")
        if exit_price >= now_price:
            print(f"매도합니다.")
            response = upbit.sell_market_order(market, volume)
            sell_uuid = response['uuid']
            save_trade_info("sell", {"market": market, "amount": volume, "response": response})
            is_order = False
            exit_price = None
            buy_price = None
            wait_until_next_quarter()
            time.sleep(30)
            
        if benefit >= set_benefit:
            print("traling on!")
            traling_start_price = now_price
            traling_benefit = benefit
            traling_on = True
            exit_price = None
            is_order = False
            stop = traling_benefit*traling_stop
            traling_market = market
            max_price = now_price
            
    elif traling_on:
        volume = upbit.get_balance(traling_market)
        print(f"현재 이익: {traling_benefit}%, 현재가: {now_price}, 손절%: {stop}, 구매가: {buy_price}")
        if traling_benefit == stop:
            response = upbit.sell_market_order("KRW-XRP", volume)
            traling_on = False
            print(Fore.RED + "트레일링 스탑. 매도합니다.")
            print(f"총 이익: {response}")
            Style.RESET_ALL
            save_trade_info("sell", {"market": market, "amount": volume, "response": response})
            wait_until_next_quarter()
            time.sleep(30)

        elif max_price < now_price:
            max_price = now_price
            stop = traling_benefit*traling_stop
            print(Fore.RED + "최고가 갱신 트레일링 스탑지점을 재설정 합니다.")
            Style.RESET_ALL
            
        traling_benefit = 100*(now_price-buy_price)/buy_price
    else:
        is_candle_2_negative = candle_2['close'] < candle_2['open']
        is_candle_1_positive = candle_1['close'] > candle_1['open']
        is_candle_0_exceeding =  candle_2['high'] > candle_1['high']
        is_now_noitive = now_price >= candle_1['high']

        if is_candle_2_negative and is_candle_1_positive and is_candle_0_exceeding and is_now_noitive:
            print("매수합니다.")
            cash = int(cash)-cash*0.0005
            response = upbit.buy_market_order(market, cash)
            print(response)

            buy_volume = upbit.get_balance(market)
            is_order = True
            exit_price = candle_1['low']
            save_trade_info("buy", {"market": market, "amount": cash, "response": response})
            buy_price = float(cash)/float(buy_volume)
        
        schedule.run_pending()
        
        if market_value != None:
            market = market_value
            print(f"거래 대상 코인을 변경합니다: {market}")
            market_value = None