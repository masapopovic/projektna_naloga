import re
import json
import os
import html
from collections import OrderedDict



#with open('spletne_strani/igra_307.html', encoding='utf-8') as file:
#    prebrano = file.read()

vzorec_igre_na_svoji_spletni_strani = re.compile(
    r'<span b-12vzocx8j4 id="yourRatingShort">(?P<ocena>.*?)</span>.*?'
    r'data-gamekey="(?P<kljuc_igre>\d+?)".*?'             #če kaj ne dela preveri to
    r'<h1 b-12vzocx8j4>(?P<ime>.*?)</h1>.*?'
    r'<span b-n3m1sg1670>Release Date</span>.*?b-n3m1sg1670 class="cardDetails.*?">(?P<leto>.*?)<.*?'
    r'<span b-n3m1sg1670>Platform</span>.*?<a class="cardDetails" href=.*?">(?P<platforma>.*?)</a>.*?'
    r'<span b-n3m1sg1670>Max Players</span>.*?b-n3m1sg1670 class="cardDetails.*?">(?P<maks_st_igralcev>.*?)<.*?'   
    r'<h5 b-12vzocx8j4>Overview</h5>.*?<p b-12vzocx8j4>(?P<daljsi_opis>.*?)</p>.*?'
    r'<h5 b-12vzocx8j4>Genres</h5>\s*(?P<zanri>(?:<a href="[^"]*?">[^<]*?</a>\s*,?\s*)+).*?',
    flags=re.DOTALL
)

vzorec_razvijalcev = re.compile(r'<h5 b-12vzocx8j4>Developers</h5>.*?(?P<razvijalci>(?:<a href=".*?">.*?</a>,?\s*)+).*?',
                                flags=re.DOTALL)
vzorec_razvijalca = re.compile(r'<a href=".*?/(?P<kljuc_razvijalca>\d+?)-.*?">(?P<razvijalec>.*?)</a>',
                                              flags=re.DOTALL)
vzorec_zaloznikov = re.compile(r'''<h5 b-12vzocx8j4>Publishers</h5>.*?(?P<zalozniki>(?:<a href=".*?">.*?</a>\s*,?\s*|<p b-12vzocx8j4 class="no-info">No information available</p>\s*)+).*?''',
                                 flags=re.DOTALL)
vzorec_zaloznika = re.compile(r'<a href=".*?/(?P<kljuc_zaloznika>\d+?)-.*?">(?P<zaloznik>.*?)</a>',
                                              flags=re.DOTALL)

#print(re.findall(vzorec_zaloznikov, prebrano))


def pocisti_znake(besedilo):
    return besedilo.replace('\r\n\r\n', ' ')

def uredi_zanre(seznam):
    zanri = []
    vzorec = re.compile(r'<a href=".*?">(.*?)</a>',
                                              flags=re.DOTALL)
    for el in vzorec.findall(seznam):
        zanri.append(html.unescape(el))
    return zanri
  

 
def podatki_igre(vsebina):
    igra = vzorec_igre_na_svoji_spletni_strani.search(vsebina).groupdict()
    igra['ime'] = html.unescape((igra['ime']))
    igra['kljuc_igre'] = int(igra['kljuc_igre'])
    igra['zanri'] = uredi_zanre(igra['zanri'])
    if igra['leto'] not in (None, 'No information available'):
        igra['leto'] = int(igra['leto'][-4:]) 
    if igra['ocena'] not in ('None', ''):
        igra['ocena'] = round(float(igra['ocena']), 2)
    igra['maks_st_igralcev'] = int(igra['maks_st_igralcev']) if igra['maks_st_igralcev'] != 'No information available' else None
    igra['daljsi_opis'] = pocisti_znake(html.unescape((igra['daljsi_opis'].strip())))
    
    #ker se pri zaloznikih in razvijalcih nekateri ključi ponavljajo bom razvijalcem dodala začetne stevke 666, zaloznikom pa 555

    razvijalci = str(vzorec_razvijalcev.findall(vsebina))[2:-1].split(',')
    igra['razvijalci'] = []
    for el in razvijalci:
        razvijalec = vzorec_razvijalca.search(el).groupdict()
        razvijalec['razvijalec'] = html.unescape((razvijalec['razvijalec']))
        razvijalec['kljuc_razvijalca'] = int('666' + razvijalec['kljuc_razvijalca'])
        igra['razvijalci'].append(razvijalec)
    
    zalozniki = str(vzorec_zaloznikov.findall(vsebina))[2:-1].split(',')
    igra['zalozniki'] = []
    for el in zalozniki:
        ujemanje = vzorec_zaloznika.search(el)         
        if ujemanje:
            zaloznik = ujemanje.groupdict()  
            zaloznik['zaloznik'] = html.unescape((zaloznik['zaloznik']))
            zaloznik['kljuc_zaloznika'] = int('555' + zaloznik['kljuc_zaloznika'])
            igra['zalozniki'].append(zaloznik)
    

    igra = OrderedDict(
        ime=igra["ime"],
        kljuc_igre=igra["kljuc_igre"],
        ocena=igra["ocena"],
        leto=igra["leto"],
        platforma=igra["platforma"],
        maks_st_igralcev=igra["maks_st_igralcev"],
        zanri=igra["zanri"],
        razvijalci=igra["razvijalci"],
        zalozniki=igra["zalozniki"],
        daljsi_opis=igra["daljsi_opis"]
    )
    
    return dict(igra)
