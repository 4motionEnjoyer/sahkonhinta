#
#Sähkönhinta widgetti, aina tälle päivälle
#By 4motionEnjoyer / Leevi S.
#

import requests
import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


def luo_graafi(eri_päivä = 0):
    if eri_päivä != 0:
        kloaika = str(datetime.datetime.now() + datetime.timedelta(days=eri_päivä))
    else: 
        kloaika = str(datetime.datetime.now())
    
    pvm = kloaika.split()[0]

        
    api_url = "https://www.sahkohinta-api.fi/api/v1/kallis?tunnit=24&tulos=sarja&aikaraja=" + pvm

    vastaus = requests.get(api_url)
    binaari = vastaus.content
    ulos_json = json.loads(binaari)

    ulos_list = list(ulos_json)

    ulos_tunnit = []
    ulos_hinnat = []
    for tunti in ulos_list:
        als = str(tunti.get("aikaleima_suomi")) #als aikaleimasuomi
        als_trimmed = als.split("T")
        hinta = float(tunti.get("hinta"))
        ulos_tunnit.append(als_trimmed[1].split(":")[0])
        ulos_hinnat.append(hinta)


    plt.bar(ulos_tunnit, ulos_hinnat)
    plt.xlabel("Kellonaika")
    plt.ylabel("Hinta [snt/kWh]")
    plt.title("Sähkön hinta " + pvm)
    return plt, pvm
    #plt.show()

def main():
    plot, pvm = luo_graafi()
    plot.show()

    exit()
    
main()

