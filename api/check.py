import requests
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
IMVU_USER_ID = "384994072"

def handler(request):
    try:
        # verificar IMVU
        url = f"https://api.imvu.com/presence/presence-{IMVU_USER_ID}"
        r = requests.get(url, timeout=10)
        data = r.json()
        online = data["denormalized"][url]["data"]["online"]

        # enviar telegram
        msg = "🟢 Active" if online else "🔴 Inactive"

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )

        return {"statusCode": 200, "body": "ok"}

    except Exception as e:
        print("Error:", e)
        return {"statusCode": 500, "body": "error"}
