import pyupbit

class Upbit_api:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        
    def save_api_keys(self):
        try:
            with open("api_keys.txt", "w") as f:
                f.write(f"{self.access_key}\n{self.secret_key}")
            
            return True
        
        except Exception as e:
            return False
            
    def load_api_keys(self):
        try:
            with open("api_keys.txt", "r") as f:
                keys = f.readlines()
                self.access_key = keys[0].strip()
                self.secret_key = keys[1].strip()
            
            return self.access_key, self.secret_key
        
        except Exception as e:
            return None, None