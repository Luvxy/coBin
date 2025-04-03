import pyupbit
import requests

class Upbit_api:
    def __init__(self, access_key, secret_key, id, password):
        self.access_key = access_key
        self.secret_key = secret_key
        self.id = id
        self.password = password
        self.user = self.create_user()
        self.token = self.create_token()
        
    def create_token(self):
        """로그인 요청을 보내고 JWT 토큰을 반환합니다."""
        url = 'http://127.0.0.1:8000/api/token/'

        payload = {
            'username': self.id,
            'password': self.password,
        }

        try:
            response = requests.post(url, data=payload)
        except requests.exceptions.RequestException as e:
            print(f"HTTP 요청 실패: {e}")
            return None

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens['access']
            return access_token
        else:
            error_message = response.json().get('detail', '로그인 실패')
            print(f"로그인 실패: {error_message}")
            return None

    def refresh_token(self):
        return self.create_token()
        
    def get_valid_token(self):
        """유효한 토큰을 반환합니다. 만료된 경우 갱신합니다."""
        if not self.token:
            self.token = self.create_token()
        return self.token

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