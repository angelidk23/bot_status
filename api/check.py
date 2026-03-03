import requests
import os

IMVU_USER_ID = "384994072"

def check_online():
    url = f"https://api.imvu.com/presence/presence-{IMVU_USER_ID}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data["denormalized"][url]["data"]["online"]

def send_telegram(message):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("CHAT_ID")

    if not token or not chat_id:
        print("Faltan variables de entorno")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    r = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": message
        },
        timeout=10
    )

    print("Telegram response:", r.text)

def handler(request):
    try:
        online = check_online()
        print("Estado IMVU:", online)

        if online:
            send_telegram("🟢 Active")
        else:
            send_telegram("🔴 Inactive")

        return {
            "statusCode": 200,
            "body": "ok"
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": "error"
        }
