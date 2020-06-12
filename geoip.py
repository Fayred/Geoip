#coding:utf-8

import requests
import getopt
import sys
import bs4
import webbrowser

url="https://whatismyipaddress.com/ip/"

def WhatIsMyIp(addrIp, url):
    r=requests.get(url+addrIp)
    soup = bs4.BeautifulSoup(r.content.decode(), "html.parser")
    dicoInformations = {}
    for i in soup.find_all("tr")[:-1]:
        s=i.text.split(":", 1)
        k, v=s[0], s[1]
        dicoInformations.update({k:v})
    for i in dicoInformations.items():
        print(" : ".join(i))
        
    return dicoInformations

def OpenMap(dicoInformations):
    try:
        latMap = dicoInformations.get("Latitude").split()[0]
        longMap = dicoInformations.get("Longitude").split()[0]
        webbrowser.open("https://www.google.com/maps/search/"+latMap+","+longMap)
    except AttributeError:
        print("[+] Erreur [MAP], manque d'information(s) précise pour afficher la position de la machine.")

try:
    opt, a = getopt.getopt(sys.argv[1:], "", ["ip=", "map", "help"])
except getopt.GetoptError:
    print("[-] Paramètre(s) inconnu.")
    exit(1)

Ip = False
Map = False

for o in opt:
    if o[0] == "--help":
        print("""
[HELP]
  --help : page d'aide
  --ip=<addr_ip> : indique l'addresse ip de la machine à géolocaliser
  --map : affiche l'emplacement de manière 'non exacte' de la machine contenant l'addr ip
        """)
        exit(0)
    if o[0] == "--ip":
        addrIp = o[1]
        Ip = True
    if o[0] == "--map":
        Map = True

try:
    if Ip == True:
        info = WhatIsMyIp(addrIp, url)
    if Map == True:
        OpenMap(info)
except (IndexError, NameError):
    print("[-] Erreur avec les paramètres.")