import requests

url = "http://127.0.0.1:8000/api/user/update_consumed_points/"
headers = {
    "Authorization": "Bearer <JWT_TOKEN>",  # 올바른 JWT 토큰
    "Content-Type": "application/json"
}
data = {
    "consumed_point1": 10,
    "consumed_point2": 5
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print("포인트 업데이트 성공:", response.json())
else:
    print("포인트 업데이트 실패:", response.status_code, response.text)