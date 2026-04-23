import requests
import time

# TU WEBHOOK
URL = "https://discord.com/api/webhooks/1496905068853727284/K135vEMDy6eKfnMbzPxEWxXQ5qA3oAXz_7KRLeH5ETEOpclyKoJotq_auVnopyHbL1I-"

def enviar(titulo, tienda, link):
    payload = {
        "content": f"🚨 **¡CAZADO AL INSTANTE!** en {tienda}\n**{titulo}**\n{link}"
    }
    requests.post(URL, json=payload)

def buscar():
    # EpicDB (Base de datos)
    try:
        r = requests.get("https://epicdb.org/api/offers?sort=updated_at&order=desc", headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).json()
        for o in r.get('data', []):
            if any(c.get('name').lower() == 'freegames' for c in o.get('categories', [])):
                enviar(o.get('title'), "EPICDB", f"https://epicdb.org/offers/{o.get('id')}")
                return # Avisa de uno y para
    except: pass

    # Steam (Ofertas 100%)
    try:
        s = requests.get("https://store.steampowered.com/api/featuredcategories", timeout=10).json()
        for i in s.get('specials', {}).get('items', []):
            if i.get('discount_percent') == 100:
                enviar(i.get('name'), "STEAM", f"https://store.steampowered.com/app/{i.get('id')}")
                return
    except: pass

if __name__ == "__main__":
    # AQUÍ ESTÁ EL TRUCO:
    # Hace 8 escaneos (cada 30 seg) = 4 minutos de vigilancia total.
    # Luego el bot se apaga y GitHub lo vuelve a encender al minuto siguiente.
    for vuelta in range(8):
        print(f"Escaneando... Vuelta {vuelta + 1} de 8")
        buscar()
        if vuelta < 7: # Espera 30 segundos para la siguiente vuelta
            time.sleep(30)
