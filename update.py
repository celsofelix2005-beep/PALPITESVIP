import requests, json, re
from datetime import datetime
import pytz

API_KEY = "1378cb3e8b27d7ed496ce567fad82cb9"
LIGAS = [39, 140, 135, 78, 61, 94, 88, 71] # Adicionei mais ligas pra ter jogos

def pega_jogos(qtd):
    fuso = pytz.timezone('Africa/Maputo')
    hoje = datetime.now(fuso).strftime('%Y-%m-%d')
    jogos = []
    
    for liga in LIGAS:
        # season=2024 = temporada atual 2024/2025
        url = f"https://v3.football.api-sports.io/fixtures?date={hoje}&league={liga}&season=2024"
        try:
            r = requests.get(url, headers={'x-apisports-key': API_KEY}).json()
            for j in r['response']:
                if len(jogos) >= qtd: break
                hora = datetime.fromisoformat(j['fixture']['date']).astimezone(fuso).strftime('%H:%M')
                jogos.append({
                    "liga": f"{j['league']['name']} - {hora}",
                    "casa": j['teams']['home']['name'],
                    "fora": j['teams']['away']['name'],
                    "palpite": "Mais de 1.5 Golos",
                    "odd": "1.80"
                })
            if len(jogos) >= qtd: break
        except: continue
    return jogos

def main():
    fuso = pytz.timezone('Africa/Maputo')
    data = datetime.now(fuso).strftime('%d/%m/%Y %H:%M')
    
    # Pega jogos pra cada aba
    jogos_gratis = pega_jogos(3)    # 3 jogos grátis
    jogos_diario = pega_jogos(2)    # 2 jogos VIP Diário  
    jogos_semanal = pega_jogos(3)   # 3 jogos VIP Semanal
    
    # Se não achar jogo, mete aviso
    if not jogos_gratis: jogos_gratis = [{"liga": "Sem jogos", "casa": "---", "fora": "---", "palpite": "---", "odd": "---"}]
    if not jogos_diario: jogos_diario = [{"liga": "Sem jogos", "casa": "---", "fora": "---", "palpite": "---", "odd": "---"}]
    if not jogos_semanal: jogos_semanal = [{"liga": "Sem jogos", "casa": "---", "fora": "---", "palpite": "---", "odd": "---"}]
    
    with open('index.html', 'r', encoding='utf-8') as f: html = f.read()
    
    # Atualiza as 3 abas de uma vez
    html = re.sub(r'GRATIS:\s*\[.*?\]', f'GRATIS: {json.dumps(jogos_gratis, ensure_ascii=False)}', html, flags=re.DOTALL)
    html = re.sub(r'DIARIO:\s*\[.*?\]', f'DIARIO: {json.dumps(jogos_diario, ensure_ascii=False)}', html, flags=re.DOTALL)
    html = re.sub(r'SEMANAL:\s*\[.*?\]', f'SEMANAL: {json.dumps(jogos_semanal, ensure_ascii=False)}', html, flags=re.DOTALL)
    html = re.sub(r'UPDATE:".*?"', f'UPDATE:"{data}"', html)
    
    with open('index.html', 'w', encoding='utf-8') as f: f.write(html)
    print(f"OK: {len(jogos_gratis)} grátis, {len(jogos_diario)} diário, {len(jogos_semanal)} semanal")

if __name__ == "__main__": main()
