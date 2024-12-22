import os
import random
import threading
import concurrent.futures
import requests
import time
import ctypes

from colorama import Fore, init
from sys import stdout

init(autoreset=True)

os.system("title INTRA-SCRAPING : Deceit 2")

print(f"""
  _____                                  _____                _ _   ___  
 / ____|                                |  __ \              (_) | |__ \ 
| (___   ___ _ __ __ _ _ __   ___ _ __  | |  | | ___  ___ ___ _| |_   ) |
 \___ \ / __| '__/ _` | '_ \ / _ \ '__| | |  | |/ _ \/ __/ _ \ | __| / / 
 ____) | (__| | | (_| | |_) |  __/ |    | |__| |  __/ (_|  __/ | |_ / /_ 
|_____/ \___|_|  \__,_| .__/ \___|_|    |_____/ \___|\___\___|_|\__|____|
                      | |                                                 
                      |_|                                                \n""", flush=True)

nombre = 0
valides = 0
invalides = 0
requete_count = 0

premier_utilisateur_ = int(input(f"\n{Fore.LIGHTMAGENTA_EX}Premier utilisateur (exemple : 1) -->{Fore.RESET} "))
dernier_utilisateur_ = int(input(f"\n{Fore.LIGHTMAGENTA_EX}Dernier utilisateur (exemple : 1000000) -->{Fore.RESET} "))
threads = int(input(f"\n{Fore.LIGHTMAGENTA_EX}Threads (exemple : 10) ->{Fore.RESET} "))

vitesse = input(f"""
{Fore.BLUE}[1] Ultra rapide (0.1s)
[2] Très Rapide (0.1 - 1s)
[3] Rapide (1 - 3s)
[4] Moyen (3 - 5s)
[5] Lent (5 - 10s)
[6] Très lent (10 - 30s)
[7] Aucun timeout

{Fore.MAGENTA}Temps max d'une requête ->{Fore.RESET} """)

if vitesse == "1":
    timeout1, timeout2 = 0.1, 0.1
elif vitesse == "2":
    timeout1, timeout2 = 0.1, 1
elif vitesse == "3":
    timeout1, timeout2 = 1, 3
elif vitesse == "4":
    timeout1, timeout2 = 3, 5
elif vitesse == "5":
    timeout1, timeout2 = 5, 10
elif vitesse == "6":
    timeout1, timeout2 = 10, 30
elif vitesse == "7":
    timeout1, timeout2 = None, None
else:
    print(f"\n{Fore.RED}[-] Mauvais choix !{Fore.RESET}")
    exit()

liste_proxies = []

liste_proxies_socks5 = [
    "be-bru-wg-socks5-103.relays.mullvad.net:1080",
    "be-bru-wg-socks5-101.relays.mullvad.net:1080",
    "fr-par-wg-socks5-004.relays.mullvad.net:1080",
    "fr-mrs-wg-socks5-001.relays.mullvad.net:1080",
    "fr-par-wg-socks5-002.relays.mullvad.net:1080",
    "fr-par-wg-socks5-005.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-001.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-404.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-202.relays.mullvad.net:1080",
    "de-ber-wg-socks5-003.relays.mullvad.net:1080",
    "de-ber-wg-socks5-002.relays.mullvad.net:1080",
    "de-dus-wg-socks5-001.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-501.relays.mullvad.net:1080",
    "de-fra-wg-socks5-004.relays.mullvad.net:1080",
    "fr-par-wg-socks5-101.relays.mullvad.net:1080",
    "fr-par-wg-socks5-102.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-002.relays.mullvad.net:1080",
    "de-dus-wg-socks5-002.relays.mullvad.net:1080",
    "fr-par-wg-socks5-001.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-505.relays.mullvad.net:1080",
    "de-ber-wg-socks5-005.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-201.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-503.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-506.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-003.relays.mullvad.net:1080",
    "de-fra-wg-socks5-001.relays.mullvad.net:1080",
    "de-fra-wg-socks5-006.relays.mullvad.net:1080",
    "de-fra-wg-socks5-008.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-401.relays.mullvad.net:1080",
    "de-dus-wg-socks5-003.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-004.relays.mullvad.net:1080",
    "de-fra-wg-socks5-005.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-502.relays.mullvad.net:1080",
    "de-fra-wg-socks5-101.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-507.relays.mullvad.net:1080",
    "de-fra-wg-socks5-103.relays.mullvad.net:1080",
    "us-nyc-wg-socks5-605.relays.mullvad.net:1080",
    "de-fra-wg-socks5-403.relays.mullvad.net:1080",
    "de-fra-wg-socks5-402.relays.mullvad.net:1080",
    "be-bru-wg-socks5-102.relays.mullvad.net:1080",
    "de-fra-wg-socks5-304.relays.mullvad.net:1080",
    "de-fra-wg-socks5-302.relays.mullvad.net:1080",
    "de-fra-wg-socks5-401.relays.mullvad.net:1080",
    "de-fra-wg-socks5-301.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-403.relays.mullvad.net:1080",
    "de-fra-wg-socks5-007.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-504.relays.mullvad.net:1080",
    "fr-par-wg-socks5-003.relays.mullvad.net:1080",
    "de-fra-wg-socks5-303.relays.mullvad.net:1080",
    "at-vie-wg-socks5-001.relays.mullvad.net:1080",
    "be-bru-wg-socks5-101.relays.mullvad.net:1080",
    "at-vie-wg-socks5-003.relays.mullvad.net:1080",
    "bg-sof-wg-socks5-002.relays.mullvad.net:1080",
    "fr-par-wg-socks5-004.relays.mullvad.net:1080",
    "ca-mtr-wg-socks5-001.relays.mullvad.net:1080",
    "ca-mtr-wg-socks5-003.relays.mullvad.net:1080",
    "sk-bts-wg-socks5-001.relays.mullvad.net:1080",
    "fi-hel-wg-socks5-103.relays.mullvad.net:1080",
    "rs-beg-wg-socks5-102.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-001.relays.mullvad.net:1080",
    "ca-tor-wg-socks5-001.relays.mullvad.net:1080",
    "au-adl-wg-socks5-302.relays.mullvad.net:1080",
    "se-mma-wg-socks5-002.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-404.relays.mullvad.net:1080",
    "de-ber-wg-socks5-002.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-202.relays.mullvad.net:1080",
    "ro-buh-wg-socks5-002.relays.mullvad.net:1080",
    "se-mma-wg-socks5-102.relays.mullvad.net:1080",
    "se-mma-wg-socks5-003.relays.mullvad.net:1080",
    "no-osl-wg-socks5-002.relays.mullvad.net:1080",
    "se-got-wg-socks5-101.relays.mullvad.net:1080",
    "au-syd-wg-socks5-002.relays.mullvad.net:1080",
    "fr-par-wg-socks5-102.relays.mullvad.net:1080",
    "de-fra-wg-socks5-004.relays.mullvad.net:1080",
    "ca-tor-wg-socks5-102.relays.mullvad.net:1080",
    "ca-tor-wg-socks5-105.relays.mullvad.net:1080",
    "au-bne-wg-socks5-302.relays.mullvad.net:1080",
    "no-svg-wg-socks5-001.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-002.relays.mullvad.net:1080",
    "de-dus-wg-socks5-002.relays.mullvad.net:1080",
    "fi-hel-wg-socks5-102.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-505.relays.mullvad.net:1080",
    "au-syd-wg-socks5-001.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-201.relays.mullvad.net:1080",
    "se-sto-wg-socks5-005.relays.mullvad.net:1080",
    "de-ber-wg-socks5-005.relays.mullvad.net:1080",
    "mk-skp-wg-socks5-001.relays.mullvad.net:1080",
    "pl-waw-wg-socks5-102.relays.mullvad.net:1080",
    "se-sto-wg-socks5-009.relays.mullvad.net:1080",
    "ca-tor-wg-socks5-103.relays.mullvad.net:1080",
    "ee-tll-wg-socks5-002.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-503.relays.mullvad.net:1080",
    "lu-lux-wg-socks5-001.relays.mullvad.net:1080",
    "se-sto-wg-socks5-004.relays.mullvad.net:1080",
    "se-got-wg-socks5-003.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-003.relays.mullvad.net:1080",
    "us-uyk-wg-socks5-102.relays.mullvad.net:1080",
    "hr-zag-wg-socks5-001.relays.mullvad.net:1080",
    "fi-hel-wg-socks5-001.relays.mullvad.net:1080",
    "de-fra-wg-socks5-001.relays.mullvad.net:1080",
    "de-fra-wg-socks5-008.relays.mullvad.net:1080",
    "no-svg-wg-socks5-003.relays.mullvad.net:1080",
    "de-dus-wg-socks5-003.relays.mullvad.net:1080",
    "ca-tor-wg-socks5-104.relays.mullvad.net:1080",
    "se-sto-wg-socks5-001.relays.mullvad.net:1080",
    "pl-waw-wg-socks5-101.relays.mullvad.net:1080",
    "se-sto-wg-socks5-002.relays.mullvad.net:1080",
    "no-osl-wg-socks5-004.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-004.relays.mullvad.net:1080",
    "pl-waw-wg-socks5-201.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-502.relays.mullvad.net:1080",
    "se-sto-wg-socks5-012.relays.mullvad.net:1080",
    "de-fra-wg-socks5-101.relays.mullvad.net:1080",
    "gb-lon-wg-socks5-302.relays.mullvad.net:1080",
    "ee-tll-wg-socks5-003.relays.mullvad.net:1080",
    "nl-ams-wg-socks5-005.relays.mullvad.net:1080",
    "no-osl-wg-socks5-001.relays.mullvad.net:1080",
    "pt-lis-wg-socks5-101.relays.mullvad.net:1080",
    "gb-lon-wg-socks5-001.relays.mullvad.net:1080",
    "gb-lon-wg-socks5-004.relays.mullvad.net:1080",
    "br-sao-wg-socks5-001.relays.mullvad.net:1080",
    "hr-zag-wg-socks5-002.relays.mullvad.net:1080",
    "nl-ams-wg-socks5-201.relays.mullvad.net:1080",
    "no-svg-wg-socks5-002.relays.mullvad.net:1080",
    "ua-iev-wg-socks5-002.relays.mullvad.net:1080",
    "gb-mnc-wg-socks5-007.relays.mullvad.net:1080",
    "nl-ams-wg-socks5-006.relays.mullvad.net:1080",
    "us-rag-wg-socks5-105.relays.mullvad.net:1080",
    "cz-prg-wg-socks5-102.relays.mullvad.net:1080",
    "us-uyk-wg-socks5-103.relays.mullvad.net:1080",
    "de-fra-wg-socks5-106.relays.mullvad.net:1080",
    "gb-mnc-wg-socks5-005.relays.mullvad.net:1080",
    "us-nyc-wg-socks5-503.relays.mullvad.net:1080",
    "gb-mnc-wg-socks5-006.relays.mullvad.net:1080",
    "us-qas-wg-socks5-002.relays.mullvad.net:1080",
    "se-sto-wg-socks5-011.relays.mullvad.net:1080",
    "gb-lon-wg-socks5-203.relays.mullvad.net:1080",
    "ch-zrh-wg-socks5-507.relays.mullvad.net:1080",
    "us-atl-wg-socks5-202.relays.mullvad.net:1080",
    "us-rag-wg-socks5-102.relays.mullvad.net:1080",
    "us-chi-wg-socks5-002.relays.mullvad.net:1080",
    "de-fra-wg-socks5-103.relays.mullvad.net:1080",
    "us-nyc-wg-socks5-605.relays.mullvad.net:1080",
    "ro-buh-wg-socks5-001.relays.mullvad.net:1080",
]

def fetch_proxies():
    global liste_proxies
    try:
        print(f"\n{Fore.GREEN}[+] {Fore.WHITE}{len(liste_proxies_socks5)}{Fore.GREEN} nouveaux proxies SOCKS5 récupérés{Fore.RESET}")
        liste_proxies = liste_proxies_socks5
    except Exception as e:
        print(f"\n{Fore.RED}[-] Erreur lors de la récupération des proxies: {e}{Fore.RESET}")

fetch_proxies()

format_ = input(f"""
{Fore.BLUE}[1] TXT
{Fore.BLUE}[2] JSON
{Fore.BLUE}[3] CSV

{Fore.LIGHTMAGENTA_EX}Entrez votre choix -->{Fore.RESET} """)
if format_ == "1":
    format = "txt"
elif format_ == "2":
    format = "json"
elif format_ == "3":
    format = "csv"
else:
    print(f"{Fore.RED}[-] Mauvais choix.{Fore.RESET}")
    exit()

print("")

def scraper_deceit2_(user_id):
    global nombre, valides, invalides, timeout1, timeout2, liste_proxies, format, requete_count

    nombre += 1
    timeout_ = random.uniform(timeout1, timeout2)
    try:
        proxy = random.choice(liste_proxies)
        proxies = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}

        requete = requests.get(f'https://live.deceit.gg/stats?userId={user_id}', proxies=proxies, timeout=timeout_)

        if requete.status_code == 200:
            data = requete.json()
            pseudo = data.get('name', 'N/A').replace("|", "").replace("\\", "\\\\").replace('"', "'")
            id_utilisateur = data.get('userId', 'N/A')
            niveau = data.get('level', 'N/A')
            tickets = data.get('tickets', 'N/A')
            reputation = data.get('reputation', 'N/A')
            temps_de_jeu = data.get('stats', {}).get('time_played_in_game', 'N/A')
            parties = data.get('stats', {}).get('games_played', 'N/A')
            parties_inn = data.get('stats', {}).get('games_as_innocent', 'N/A')
            parties_inf = data.get('stats', {}).get('games_as_infected', 'N/A')
            evasions = data.get('stats', {}).get('escapes', 'N/A')

            if format == "txt":
                utilisateur_data = f"Username : {pseudo} | ID : {id_utilisateur} | Level : {niveau} | Tickets : {tickets} | Reputation : {reputation} | Time Played : {temps_de_jeu} | Games Played : {parties} | Games As Innocent : {parties_inn} | Games As Infected : {parties_inf} | Escapes : {evasions}"
            elif format == "json":
                utilisateur_data = f'{{"userId": {id_utilisateur}, "name": "{pseudo}", "level": {niveau}, "tickets": {tickets}, "reputation": {reputation}, "timePlayed": {temps_de_jeu}, "gamesPlayed": {parties}, "gameAsInnocent": {parties_inn}, "gamesAsInfected": {parties_inf}, "escapes": {evasions}}},'
            elif format == "csv":
                utilisateur_data = f"{pseudo},{id_utilisateur},{niveau},{tickets},{reputation},{temps_de_jeu},{parties},{parties_inn},{parties_inf},{evasions}"
            
            utilisateurs.append(utilisateur_data)
            stdout.write(f"\r{Fore.GREEN}[{Fore.WHITE}Nombre : {nombre}{Fore.GREEN}] {Fore.WHITE}> {Fore.GREEN}[{Fore.WHITE}Pseudo : {pseudo} ({user_id}){Fore.GREEN}] {Fore.WHITE}> {Fore.GREEN}[{Fore.WHITE}Status : enregistré{Fore.GREEN}]{Fore.RESET}")
            valides += 1

        elif requete.status_code == 429:
            stdout.write(f"\r{Fore.RED}[{Fore.WHITE}Nombre : {nombre}{Fore.RED}] {Fore.WHITE}> {Fore.RED}[{Fore.WHITE}Erreur 429 : Trop de requêtes. Changement de proxy...{Fore.RED}]{Fore.RESET}")
            time.sleep(5)
            proxy = random.choice(liste_proxies)
            proxies = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
            return scraper_deceit2_(user_id) 
    
        else:
            stdout.write(f"\r{Fore.YELLOW}[{Fore.WHITE}Nombre : {nombre}{Fore.YELLOW}] {Fore.WHITE}> {Fore.YELLOW}[{Fore.WHITE}Status : {requete.status_code}{Fore.YELLOW}]{Fore.RESET}")
            invalides += 1

        requete_count += 1
        if requete_count >= 10000:
            stdout.write(f"\r{Fore.YELLOW}[{Fore.WHITE}Nombre : {nombre}{Fore.YELLOW}] {Fore.WHITE}> {Fore.YELLOW}[{Fore.WHITE}10000 requêtes effectuées, changement de proxy...{Fore.YELLOW}]{Fore.RESET}")
            requete_count = 0
            proxy = random.choice(liste_proxies)
            proxies = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}

        stdout.flush()
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        pass

    except TimeoutError:
        stdout.write(f"\r{Fore.YELLOW}[{Fore.WHITE}Nombre : {nombre}{Fore.YELLOW}] {Fore.WHITE}> {Fore.YELLOW}[{Fore.WHITE}Timeout dépassé{Fore.YELLOW}]{Fore.RESET}")
        stdout.flush()
        invalides += 1
    except Exception as e:
        stdout.write(f"\r{Fore.RED}[{Fore.WHITE}Nombre : {nombre}{Fore.RED}] {Fore.WHITE}> {Fore.RED}[{Fore.WHITE}Erreur : {e}{Fore.RED}]{Fore.RESET}")
        stdout.flush()
        invalides += 1

    ctypes.windll.kernel32.SetConsoleTitleW(f"Nombre : {nombre} | Valides : {valides} | Invalides : {invalides} | Proxy : {proxy}")

def sauvegarder_utilisateurs():
    output_path = f'users.{format}'
    directory = os.path.dirname(output_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(output_path, 'a', encoding='utf-8') as file:
        file.write("\n".join(utilisateurs))

    utilisateurs.clear()
    print(f"\n\n{Fore.GREEN}[+] Données sauvegardées temporairement dans -> {Fore.RESET}{output_path}")

def scraper_deceit2():
    global utilisateurs
    utilisateurs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scraper_deceit2_, user_id): user_id for user_id in range(premier_utilisateur_, dernier_utilisateur_ + 1)}
        for future in concurrent.futures.as_completed(futures):
            user_id = futures[future]
            try:
                future.result()
            except Exception as exc:
                print(f"\n{Fore.RED}[-] Erreur : {Fore.RESET}{exc}\n\n")

            if nombre % 10000 == 0:
                fetch_proxies()
                sauvegarder_utilisateurs()

    sauvegarder_utilisateurs()
    print(f"\n\n{Fore.GREEN}[+] Données enregistrées dans -> {Fore.RESET}users.{format}")

scraper_deceit2()
