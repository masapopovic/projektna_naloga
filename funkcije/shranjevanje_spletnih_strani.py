import requests
import re
import os
import requests
import sys

from orodja import pripravi_imenik, shrani_spletno_stran

#zajela bom prvih 20 strani tistih iger, ki imajo ESRB = MATURE

st_strani = 20
for stran in range(1, st_strani + 1):
    url = f"https://gamesdb.launchbox-app.com/games/results/%7C{stran}?esrb=mature"
    odziv = requests.get(url)
    if odziv.status_code == 200:
        print(url)
        with open(f"spletne_strani/stran-{stran}.html", "w", encoding='utf-8') as f:
            f.write(odziv.text)
    else:
        print("Prišlo je do napake")
        

def odpri_spletne_strani(st_strani):
    for stran in range(1, st_strani + 1):
        with open(f'spletne_strani/stran-{stran}.html', 'r', encoding='utf-8') as dat:
            prebrano = dat.read()   
        for igra in re.finditer(r'<a class="list-item link-no-underline" href="(?P<povezava>/games/details/\d+?-.*?)">', prebrano):
            yield igra.group('povezava')

import time
def oblikuj_spletne_strani(st_strani):
    stevec = 1
    for del_url in odpri_spletne_strani(st_strani):
        url = f'https://gamesdb.launchbox-app.com{del_url}'
        shrani_kot = f'spletne_strani/igra_{stevec}.html'
        shrani_spletno_stran(url, shrani_kot)
        stevec += 1
        #time.sleep(1)

oblikuj_spletne_strani(20)
