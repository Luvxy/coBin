import requests

def send_webhook(url, payload):
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Webhook sent successfully!")
        else:
            print(f"Failed to send webhook. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    webhook_url = "http://192.168.0.2:5000/webhook"  # Replace with your webhook URL
    data = {
        "message": "Hello, this is a test webhook!",
        "status": "success"
    }
    send_webhook(webhook_url, data)