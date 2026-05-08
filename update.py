import requests, json
from datetime import datetime
import pytz

API_KEY = "1378cb3e8b27d7ed496ce567fad82cb9" # Tua key
LIGAS = [39, 140, 135, 78, 61] # Premier, LaLiga, SerieA, Bundesliga, Ligue1

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
            jogos.append(f"""
            <div class='jogo'>
                <b>{hora} - {j['league']['name']}</b><br>
                {j['teams']['home']['name']} vs {j['teams']['away']['name']}<br>
                Palpite: Mais de 1.5 gols
            </div><hr>""")
    
    html_jogos = "".join(jogos) if jogos else "<p><b>Sem jogos hoje nas principais ligas.</b></p>"
    data = datetime.now(fuso).strftime('%d/%m/%Y %H:%M')
    
    with open('index.html', 'r', encoding='utf-8') as f: html = f.read()
    html = html.replace('', f'{html_jogos}')
    html = html.replace('', f'Atualizado: {data}')
    with open('index.html', 'w', encoding='utf-8') as f: f.write(html)
    print(f"Atualizado com {len(jogos)} jogos")

if __name__ == "__main__": main()
