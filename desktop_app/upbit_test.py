import pyupbit
from upbit.api_upbit import Upbit_api

a = "0L6LOtuovTfT3Anjptj1NdB8zMHhxKhzsshNLogy"
s = "BbCTt8blhRLcUNoapxvUSMiI45QdaMgswUQ0WqvU"

upbit = Upbit_api(a,s)
upbit.create_user()

order = upbit.get_order("KRW-BTC", state="done", limit=1)
balance = float(upbit.get_balance("KRW")) * 0.9995
print(balance)
upbit.buy_market_order("KRW-BTC", cash=balance)


print(order)

coin = "KRW-BTC"

balances = upbit.get_balances()  # ✅ 전체 잔고 조회
for b in balances:
    if b['currency'] == coin.replace("KRW-", ""):
        dklj = float(b['avg_buy_price'])# 예: "KRW-BTC" → "BTC"

print(dklj)
