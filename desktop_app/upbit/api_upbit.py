import pyupbit
import requests

class Upbit_api:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def create_user(self):
        try:
            self.user = pyupbit.Upbit(self.access_key, self.secret_key)
        except:
            self.user = None
        
    def get_balances(self):
        try:
            return self.user.get_balances()
        except:
            return None
    
    def get_balance(self, ticker):
        try:
            return self.user.get_balance(ticker)
        except:
            return None
    
    def get_order(self, ticker, state="done", limit=10):
        return self.user.get_order(ticker, state=state, limit=limit)
    
    def buy_market_order(self, ticker, cash):
        return self.user.buy_market_order(ticker, cash)
    
    def sell_market_order(self, ticker, volume):
        return self.user.sell_market_order(ticker, volume)
    
    def buy_limit_order(self, ticker, price, volume):
        return self.user.buy_limit_order(ticker, price, volume)

    def sell_limit_order(self, ticker, price, volume):
        return self.user.sell_limit_order(ticker, price, volume)

    def get_avg_buy_price(self, ticker):
        return self.user.get_avg_buy_price(ticker)
    
    def get_current_price(self, ticker):
        return pyupbit.get_current_price(ticker)