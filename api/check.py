import requests

TELEGRAM_TOKEN = "TU_TOKEN"
CHAT_ID = "TU_CHAT_ID"
IMVU_USER_ID = "384994072"

def check_online():
    url = f"https://api.imvu.com/presence/presence-{IMVU_USER_ID}"
    r = requests.get(url, timeout=10)
    data = r.json()
    return data["denormalized"][url]["data"]["online"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })
    print("Telegram response:", r.text)

def handler(request):
    try:
        is_online = check_online()
        print("Estado IMVU:", is_online)

        if is_online:
            send_telegram("🟢 Active")
        else:
            send_telegram("🔴 Inactive")

        return {
            "statusCode": 200,
            "body": "ok"
        }

    except Exception as e:
        print("Error:", e)
        return {
            "statusCode": 500,
            "body": "error"
        }
