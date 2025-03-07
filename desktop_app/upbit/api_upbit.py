import pyupbit

class Upbit_api:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.user = self.create_user()
        
    def create_user(self):
        try:
            self.user = pyupbit.Upbit(self.access_key, self.secret_key)
        except:
            self.user = None
        
    def get_balance(self, ticker):
        try:
            return self.user.get_balance(ticker)
        except:
            return None
    
    def get_order(self):
        return self.user.get_order()
    
    def buy_market_order(self, ticker, cash):
        return self.user.buy_market_order(ticker, cash)
    
    def sell_market_order(self, ticker, volume):
        return self.user.sell_market_order(ticker, volume)
