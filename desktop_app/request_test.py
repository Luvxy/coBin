import requests

def fetch_user_info(token, id):
    """Django 서버로 요청을 보내 유저 정보를 가져옵니다."""
    url = f"http://127.0.0.1:8000/api/user/{id}"  # Django 서버의 API URL
    headers = {
        "Authorization": f"Bearer {token}"  # JWT 토큰을 헤더에 포함
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        user_data = result['user_data']
        return user_data
    else:
        print("유저 정보 요청 실패:", response.status_code, response.text)
        return None
    
def login_button_clicked(id, password):
    """로그인 요청을 보내고 JWT 토큰을 반환합니다."""
    url = 'http://127.0.0.1:8000/api/token/'
    
    payload = {
        'username': id,
        'password': password,
    }
    
    response = requests.post(url, data=payload)  # data를 사용

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access']
        refresh_token = tokens['refresh']
        return access_token
    else:
        print("로그인 실패:", response.json())
        return None

if __name__ == "__main__":
    id = "brunch"
    ps = "qaz4455!"
    token = login_button_clicked(id, ps)
    if token:
        user_data = fetch_user_info(token, id)
        print(user_data)