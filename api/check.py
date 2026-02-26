import requests
import os

TELEGRAM_TOKEN = "8781910142:AAF-rPBKEhKkZHVCTQXEqTv2fVygkq71xW8"
CHAT_ID = "6151769961"
IMVU_USER_ID = "384994072"

def check_online():
    try:
        url = f"https://api.imvu.com/presence/presence-{IMVU_USER_ID}"
        r = requests.get(url, timeout=10)
        data = r.json()
        return data["denormalized"][url]["data"]["online"]
    except:
        return None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def handler(request):
    is_online = check_online()
    if is_online is True:
        send_telegram("🟢 conectado")
    elif is_online is False:
        send_telegram("🔴 desconectado")
    return {"statusCode": 200, "body": "ok"}