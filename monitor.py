import requests
import time
import os

TELEGRAM_TOKEN = "8781910142:AAF-rPBKEhKkZHVCTQXEqTv2fVygkq71xW8"
CHAT_ID = "6151769961"
IMVU_USER_ID = "384994072"
CHECK_INTERVAL = 60  # segundos entre cada chequeo

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

def main():
    print("🟢 Monitor iniciado...")
    send_telegram("✅ Monitor de IMVU iniciado. Te avisaré cuando 𝓛𝓲𝓻𝓪 se conecte.")
    
    was_online = False

    while True:
        is_online = check_online()

        if is_online is True and not was_online:
            send_telegram("🟢 ¡𝓛𝓲𝓻𝓪 acaba de conectarse en IMVU!")
            was_online = True
        elif is_online is False and was_online:
            send_telegram("🔴 𝓛𝓲𝓻𝓪 se ha desconectado de IMVU.")
            was_online = False

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
