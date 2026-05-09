import requests, json, re
from datetime import datetime
import pytz

API_KEY = "1378cb3e8b27d7ed496ce567fad82cb9"
LIGAS = [39, 140, 135, 78, 61, 71, 128, 253, 262, 88] # Adicionei Eredivisie = 88

def pega_jogos(qtd):
    fuso = pytz.timezone('Africa/Maputo')
    hoje = datetime.now(fuso).strftime('%Y-%m-%d')
    jogos = []
    
    for liga in LIGAS:
        for season in [2024, 2025]:
            # AQUI TÁ O FIX: &timezone=Africa/Maputo
            url = f"https://v3.football.api-sports.io/fixtures?date={hoje}&league={liga}&season={season}&timezone=Africa/Maputo"
            try:
                r = requests.get(url, headers={'x-apisports-key': API_KEY}).json()
                if r.get('response'):
                    for j in r['response']:
                        if len(jogos) >= qtd: break
                        hora = datetime.fromisoformat(j['fixture']['date']).strftime('%H:%M')
                        jogos.append({
                            "liga": f"{j['league']['name']} - {hora}",
                            "casa": j['teams']['home']['name'],
                            "fora": j['teams']['away']['name'],
                            "palpite": "Mais de 1.5 Golos",
                            "odd": "1.80"
                        })
                    break
            except: continue
        if len(jogos) >= qtd: break
    
    return jogos if jogos else [{"liga": "Sem jogos hoje", "casa": "Volta", "fora": "amanhã", "palpite": "---", "odd": "---"}]

def main():
    fuso = pytz.timezone('Africa/Maputo')
    data = datetime.now(fuso).strftime('%d/%m/%Y %H:%M')
    
    jogos_gratis = pega_jogos(3)
    jogos_diario = pega_jogos(2)  
    jogos_semanal = pega_jogos(3)
    
    with open('index.html', 'r', encoding='utf-8') as f: html = f.read()
    
    html = re.sub(r'GRATIS:\s*\[.*?\]', f'GRATIS: {json.dumps(jogos_gratis, ensure_ascii=False)}', html, flags=re.DOTALL)
    html = re.sub(r'DIARIO:\s*\[.*?\]', f'DIARIO: {json.dumps(jogos_diario, ensure_ascii=False)}', html, flags=re.DOTALL)
    html = re.sub(r'SEMANAL:\s*\[.*?\]', f'SEMANAL: {json.dumps(jogos_semanal, ensure_ascii=False)}', html, flags=re.DOTALL)
    html = re.sub(r'UPDATE:".*?"', f'UPDATE:"{data}"', html)
    
    with open('index.html', 'w', encoding='utf-8') as f: f.write(html)
    print(f"OK: {len(jogos_gratis)} grátis, {len(jogos_diario)} diário, {len(jogos_semanal)} semanal")

if __name__ == "__main__": main()
