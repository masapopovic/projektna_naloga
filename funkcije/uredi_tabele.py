import re
import os
import requests
import sys

from orodja import *
from iskanje_vzorcev import *



def uredi_igre_v_glavno_tabelo():
    igre = []
    for st in range(1, 2001): 
        with open(f'spletne_strani/igra_{st}.html', encoding='utf-8') as dat:
            besedilo = dat.read()
            igra = podatki_igre(besedilo)
            igre.append(igra)
    return igre
igre = uredi_igre_v_glavno_tabelo()
#print(igre)


def uredi_igre_v_manjso_tabelo(st):
    vse_igre = []
    for st in range(1, st): 
        with open(f'spletne_strani/igra_{st}.html', encoding='utf-8') as dat:
            tekst = dat.read()
            igra = podatki_igre(tekst)
            del igra['zanri'], igra['razvijalci'], igra['zalozniki']
            vse_igre.append(igra)
    vse_igre.sort(key=lambda igra: igra['kljuc_igre'])
    return vse_igre

vse_igre = uredi_igre_v_manjso_tabelo(2001)

#print(vse_igre)


def uredi_gnezdene_podatke_v_tabele(igre):
    zanri, razvijalci, zalozniki = [],[],[]
    for igra in igre:
        for zanr in igra['zanri']:
            zanri.append({'kljuc_igre': igra['kljuc_igre'], 'zanr': zanr})
        for razvijalec in igra['razvijalci']:
            razvijalci.append({
                'kljuc_igre': igra['kljuc_igre'], 
                'kljuc_razvijalca': razvijalec['kljuc_razvijalca'],
                'razvijalec': razvijalec['razvijalec']
                })
        for zaloznik in igra['zalozniki']:
            zalozniki.append({
                    'kljuc_igre': igra['kljuc_igre'], 
                    'kljuc_zaloznika': zaloznik['kljuc_zaloznika'],
                    'zaloznik': zaloznik['zaloznik']
                    })
    zanri.sort(key=lambda zanr: zanr['zanr'])
    razvijalci.sort(key=lambda razvijalec: razvijalec['kljuc_razvijalca'])  
    zalozniki.sort(key=lambda zaloznik: zaloznik['kljuc_zaloznika'])  
    return zanri, razvijalci, zalozniki

                  
zanri, razvijalci, zalozniki = uredi_gnezdene_podatke_v_tabele(igre)