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
vzorec_izdajateljev = re.compile(r'''<h5 b-12vzocx8j4>Publishers</h5>.*?(?P<izdajatelji>(?:<a href=".*?">.*?</a>\s*,?\s*|<p b-12vzocx8j4 class="no-info">No information available</p>\s*)+).*?''',
                                 flags=re.DOTALL)
vzorec_izdajatelja = re.compile(r'<a href=".*?/(?P<kljuc_izdajatelja>\d+?)-.*?">(?P<izdajatelj>.*?)</a>',
                                              flags=re.DOTALL)

#print(re.findall(vzorec_izdajateljev, prebrano))


def pocisti_znake(besedilo):
    return besedilo.replace('\r\n\r\n', ' ')

def uredi_zanre(seznam):
    zanri = []
    vzorec = re.compile(r'<a href=".*?">(.*?)</a>',
                                              flags=re.DOTALL)
    for el in vzorec.findall(seznam):
        zanri.append(el)
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
    
    #ker se pri izdajateljih in razvijalcih nekateri ključi ponavljajo bom razvijalcem dodala začetne stevke 666, izdajateljem pa 555

    razvijalci = str(vzorec_razvijalcev.findall(vsebina))[2:-1].split(',')
    igra['razvijalci'] = []
    for el in razvijalci:
        razvijalec = vzorec_razvijalca.search(el).groupdict()
        razvijalec['razvijalec'] = html.unescape((razvijalec['razvijalec']))
        razvijalec['kljuc_razvijalca'] = int('666' + razvijalec['kljuc_razvijalca'])
        igra['razvijalci'].append(razvijalec)
    
    izdajatelji = str(vzorec_izdajateljev.findall(vsebina))[2:-1].split(',')
    igra['izdajatelji'] = []
    for el in izdajatelji:
        ujemanje = vzorec_izdajatelja.search(el)         
        if ujemanje:
            izdajatelj = ujemanje.groupdict()  
            izdajatelj['izdajatelj'] = html.unescape((izdajatelj['izdajatelj']))
            izdajatelj['kljuc_izdajatelja'] = int('555' + izdajatelj['kljuc_izdajatelja'])
            igra['izdajatelji'].append(izdajatelj)
    

    igra = OrderedDict(
        ime=igra["ime"],
        kljuc_igre=igra["kljuc_igre"],
        ocena=igra["ocena"],
        leto=igra["leto"],
        platforma=igra["platforma"],
        maks_st_igralcev=igra["maks_st_igralcev"],
        zanri=igra["zanri"],
        razvijalci=igra["razvijalci"],
        izdajatelji=igra["izdajatelji"],
        daljsi_opis=igra["daljsi_opis"]
    )
    
    return dict(igra)
