from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json  # JSON 페이로드를 파싱
        print("Received webhook data:", data)  # 받은 웹훅 데이터를 출력
        # 데이터를 필요한 대로 처리
        return jsonify({"status": "success", "message": "Webhook received"}), 200  # 성공 응답 반환
    else:
        return jsonify({"status": "error", "message": "Invalid method"}), 405  # 잘못된 메서드 응답 반환

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 애플리케이션 실행 (모든 IP에서 접근 가능, 포트 5000)