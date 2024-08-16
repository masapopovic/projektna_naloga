import json
import csv

from uredi_tabele import *

zapisi_json(igre, 'json_in_csv_datoteke/glavno_igre.json')
zapisi_csv(igre, ["ime", "kljuc_igre", "ocena", "leto", "platforma", "maks_st_igralcev", "zanri", "razvijalci", "izdajatelji", "daljsi_opis"], 'json_in_csv_datoteke/glavno_igre.csv')


zapisi_json(vse_igre, 'json_in_csv_datoteke/igre.json')
zapisi_csv(vse_igre, ["ime", "kljuc_igre", "ocena", "leto", "platforma", "maks_st_igralcev", "daljsi_opis"], 'json_in_csv_datoteke/igre.csv')

zapisi_json(zanri, 'json_in_csv_datoteke/zanri_iger.json')
zapisi_json(razvijalci, 'json_in_csv_datoteke/razvijalci_iger.json')
zapisi_json(izdajatelji, 'json_in_csv_datoteke/izdajatelji_iger.json')

       
zapisi_csv(zanri, ["kljuc_igre", "zanr"], 'json_in_csv_datoteke/zanri_iger.csv')
zapisi_csv(razvijalci, ["kljuc_igre", "kljuc_razvijalca", "razvijalec"], 'json_in_csv_datoteke/razvijalci_iger.csv')
zapisi_csv(izdajatelji, ["kljuc_igre","kljuc_izdajatelja", "izdajatelj"], 'json_in_csv_datoteke/izdajatelji_iger.csv')

