import requests
from http.server import BaseHTTPRequestHandler

TELEGRAM_TOKEN = "8762477883:AAGdSH163PHITDv4gX_4Rn5mc3TNr-RxZyM"
CHAT_ID = "6151769961"
IMVU_USER_ID = "384994072"
JSONBIN_API_KEY = "$2a$10$LmYGxXIvdMcCrRbvxrzjsOsEmYdCL5inoTQRwUneaW3ueMrZU36qG"
JSONBIN_BIN_ID = "69a0b62943b1c97be9a17678"

def check_online():
    try:
        url = f"https://api.imvu.com/presence/presence-{IMVU_USER_ID}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Cookie": "osCsid=24d982de49a25efd352d6904c10e885a"
        }
        r = requests.get(url, headers=headers, timeout=10)
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
        print(f"IMVU status: {is_online} | Estado guardado: {was_online}")
        if is_online is True and not was_online:
            print("-> Enviando notificacion: online")
            send_telegram("🟢 Active")
            save_state(True)
        elif is_online is False and was_online:
            print("-> Enviando notificacion: offline")
            send_telegram("🔴 Inactive")
            save_state(False)
        else:
            print("-> Sin cambio de estado")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
