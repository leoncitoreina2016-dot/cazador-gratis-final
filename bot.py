import requests
import os
import time

URL = "https://discord.com/api/webhooks/1496905068853727284/K135vEMDy6eKfnMbzPxEWxXQ5qA3oAXz_7KRLeH5ETEOpclyKoJotq_auVnopyHbL1I-"
DB_FILE = "enviados.txt"

def enviar(titulo, tienda, link):
    # Leer memoria
    if not os.path.exists(DB_FILE): open(DB_FILE, "w").close()
    with open(DB_FILE, "r") as f:
        enviados = f.read().splitlines()
    
    if titulo in enviados: return # Si ya se envió, ignorar

    payload = {"content": f"🚨 **¡NUEVA CAZA!** ({tienda})\n**{titulo}**\n{link}"}
    r = requests.post(URL, json=payload)
    
    if r.status_code == 204:
        with open(DB_FILE, "a") as f:
            f.write(titulo + "\n")

def buscar():
    # EpicDB
    try:
        r = requests.get("https://epicdb.org/api/offers?sort=updated_at&order=desc", headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).json()
        for o in r.get('data', []):
            if any(c.get('name').lower() == 'freegames' for c in o.get('categories', [])):
                enviar(o.get('title'), "EPICDB", f"https://epicdb.org/offers/{o.get('id')}")
    except: pass

    # Steam
    try:
        s = requests.get("https://store.steampowered.com/api/featuredcategories", timeout=10).json()
        for i in s.get('specials', {}).get('items', []):
            if i.get('discount_percent') == 100:
                enviar(i.get('name'), "STEAM", f"https://store.steampowered.com/app/{i.get('id')}")
    except: pass

if __name__ == "__main__":
    # Bucle de 4 minutos (un escaneo cada 30 segundos)
    for vuelta in range(8):
        buscar()
        if vuelta < 7: time.sleep(30)
