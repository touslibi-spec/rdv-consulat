import time
import requests
import subprocess
from datetime import datetime

# Configuration Telegram
TELEGRAM_TOKEN   = "8644728406:AAGU0sLn2NLjl57yPtfR3D0-2Wz2FJ9O7m8"
TELEGRAM_CHAT_ID = "6292977016"

URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/2da8fb6f4ac7361929959598a1e5b1e45"
INTERVALLE = 180

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

def verifier():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=15)
        texte = r.text.lower()
        if "seleccione" in texte or "fecha disponible" in texte or "hora" in texte:
            return True
        return False
    except:
        return False

def envoyer_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        })
        print("Telegram envoye !")
    except Exception as e:
        print(f"Erreur Telegram : {e}")

def alerter():
    subprocess.run(["osascript", "-e",
        'display notification "Un creneau est disponible ! Allez vite reserver !" with title "RENDEZ-VOUS DISPONIBLE !" sound name "Glass"'])
    envoyer_telegram(
        "RENDEZ-VOUS DISPONIBLE !\n\n"
        "Un creneau est disponible au Consulat d Espagne a Oran !\n\n"
        "Allez vite reserver :\n"
        "https://www.citaconsular.es/es/hosteds/widgetdefault/2da8fb6f4ac7361929959598a1e5b1e45"
    )
    subprocess.run(["open", URL])

print("Surveillance demarree - Consulat d Espagne a Oran")
print(f"Verification toutes les {INTERVALLE // 60} minutes")
print("Ctrl+C pour arreter\n")

i = 1
while True:
    heure = datetime.now().strftime("%H:%M:%S")
    print(f"[{i}] {heure} - Verification...", end=" ", flush=True)
    if verifier():
        print("CRENEAU TROUVE !")
        alerter()
        break
    else:
        print("Pas encore disponible.")
    i += 1
    time.sleep(INTERVALLE)
