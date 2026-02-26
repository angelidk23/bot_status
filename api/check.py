import requests
from http.server import BaseHTTPRequestHandler

TELEGRAM_TOKEN = "8781910142:AAF-rPBKEhKkZHVCTQXEqTv2fVygkq71xW8"
CHAT_ID = "6151769961"
IMVU_USER_ID = "387851357"
JSONBIN_API_KEY = "$2a$10$LmYGxXIvdMcCrRbvxrzjsOsEmYdCL5inoTQRwUneaW3ueMrZU36qG"
JSONBIN_BIN_ID = "69a0b62943b1c97be9a17678"

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

def get_state():
    url = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}/latest"
    r = requests.get(url, headers={"X-Master-Key": JSONBIN_API_KEY})
    return r.json()["record"]["online"]

def save_state(state):
    url = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"
    requests.put(url, json={"online": state}, headers={
        "X-Master-Key": JSONBIN_API_KEY,
        "Content-Type": "application/json"
    })

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        is_online = check_online()
        was_online = get_state()

        if is_online is True and not was_online:
            send_telegram("🟢 Active")
            save_state(True)
        elif is_online is False and was_online:
            send_telegram("🔴 Inactive")
            save_state(False)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
