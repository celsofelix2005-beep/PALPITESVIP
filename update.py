import requests, json, re
from datetime import datetime
import pytz

API_KEY = "1378cb3e8b27d7ed496ce567fad82cb9"
LIGAS = [39, 140, 135, 78, 61] 

def main():
    fuso = pytz.timezone('Africa/Maputo')
    hoje = datetime.now(fuso).strftime('%Y-%m-%d')
    jogos = []
    
    for liga in LIGAS:
        url = f"https://v3.football.api-sports.io/fixtures?date={hoje}&league={liga}&season=2025"
        r = requests.get(url, headers={'x-apisports-key': API_KEY}).json()
        for j in r['response']:
            if len(jogos) >= 3: break
            hora = datetime.fromisoformat(j['fixture']['date']).astimezone(fuso).strftime('%H:%M')
            jogos.append({
                "liga": f"{j['league']['name']} - {hora}",
                "casa": j['teams']['home']['name'],
                "fora": j['teams']['away']['name'],
                "palpite": "Mais de 1.5 Golos",
                "odd": "1.80"
            })
    
    data = datetime.now(fuso).strftime('%d/%m/%Y %H:%M')
    
    with open('index.html', 'r', encoding='utf-8') as f: html = f.read()
    
    novo_gratis = json.dumps(jogos, ensure_ascii=False)
    html = re.sub(r'GRATIS:\s*\[.*?\]', f'GRATIS: {novo_gratis}', html, flags=re.DOTALL)
    html = re.sub(r'UPDATE:".*?"', f'UPDATE:"{data}"', html)
    
    with open('index.html', 'w', encoding='utf-8') as f: f.write(html)
    print(f"Atualizado com {len(jogos)} jogos")

if __name__ == "__main__": main()
