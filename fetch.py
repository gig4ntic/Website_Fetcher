import os
import subprocess
import sys

import requests
from bs4 import BeautifulSoup

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Installiere requests und beautifulsoup4, falls sie noch nicht installiert sind
install("requests")
install("beautifulsoup4")

# Define the URL and headers
url = "https://www.stall-frei.de/stall/baden-wuerttemberg/schwaigern/143025"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def get_free_stalls(url):
    try:
        response = requests.get(url, headers=headers)  # nur einmal aufrufen
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        stalls_element = soup.select_one('#divisions > table > tbody > tr > td:nth-child(3)')

        if stalls_element:
            free_stalls_str = stalls_element.text.strip()
            try:
                return int(free_stalls_str)
            except ValueError:
                print(f"Fehler: Konnte '{free_stalls_str}' nicht in eine Zahl umwandeln.")
                return None
        else:
            print("Element mit freien Stallplätzen nicht gefunden.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Seite: {e}")
        return None

if __name__ == "__main__":
    free_stalls = get_free_stalls(url)

    if free_stalls is not None:
        print(f"Freie Stallplätze: {free_stalls}")
        try:
            with open("freeplaces.txt", "w") as f:
                f.write(str(free_stalls))
        except OSError as e:
            print(f"Fehler beim Schreiben in Datei: {e}")
    else:
        print("Anzahl der freien Stallplätze konnte nicht abgerufen werden.")