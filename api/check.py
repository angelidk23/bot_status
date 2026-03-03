import requests
import os
from http.server import BaseHTTPRequestHandler

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
IMVU_USER_ID = "388423457"

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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        is_online = check_online()
        print(f"IMVU status: {is_online}")
        if is_online is True:
            send_telegram("🟢 Active")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
