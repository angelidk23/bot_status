import requests
from http.server import BaseHTTPRequestHandler

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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        is_online = check_online()
        if is_online is True:
            send_telegram("🟢 active")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
