import requests

# TU WEBHOOK
URL = "https://discord.com/api/webhooks/1496905068853727284/K135vEMDy6eKfnMbzPxEWxXQ5qA3oAXz_7KRLeH5ETEOpclyKoJotq_auVnopyHbL1I-"

def enviar(titulo, tienda, link):
    payload = {
        "content": f"🚨 **NUEVO JUEGO EN {tienda}**\n**{titulo}**\n{link}"
    }
    requests.post(URL, json=payload)

def buscar():
    # EpicDB
    try:
        r = requests.get("https://epicdb.org/api/offers?sort=updated_at&order=desc", headers={'User-Agent': 'Mozilla/5.0'}).json()
        for o in r.get('data', []):
            if any(c.get('name').lower() == 'freegames' for c in o.get('categories', [])):
                enviar(o.get('title'), "EPICDB", f"https://epicdb.org/offers/{o.get('id')}")
                break 
    except: pass

    # Steam
    try:
        s = requests.get("https://store.steampowered.com/api/featuredcategories").json()
        for i in s.get('specials', {}).get('items', []):
            if i.get('discount_percent') == 100:
                enviar(i.get('name'), "STEAM", f"https://store.steampowered.com/app/{i.get('id')}")
                break
    except: pass

if __name__ == "__main__":
    buscar()
