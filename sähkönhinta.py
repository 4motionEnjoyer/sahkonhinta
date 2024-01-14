#!/bin/python
#
##################################################
#Sähkönhinta widgetti, tänään +-1 pvä
#By 4motionEnjoyer / Leevi S.
###################################################

##############
#Importit
##############
import requests
import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from tkinter import *

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

##############
#Funktiot
##############

def luo_graafi(eri_päivä = 0):
    if eri_päivä != 0:
        kloaika = str(datetime.datetime.now() + datetime.timedelta(days=eri_päivä))
    else: 
        kloaika = str(datetime.datetime.now())
    
    pvm = kloaika.split()[0]

    #print(pvm)
  
    api_url = "https://www.sahkohinta-api.fi/api/v1/kallis?tunnit=24&tulos=sarja&aikaraja=" + pvm

    vastaus = requests.get(api_url)
    binaari = vastaus.content
    try:
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

    except Exception as e:
        print("Joko käytit liikaa API kutsuja (60 tunnissa sallittu) tai huomisen dataa ei ole julkaistu, yleensä klo 14:00 eteenpäin. Alla tulkin sepustus")
        print("\n")
        print(str(e))
        print("\nYritä myödemmin uudelleen")
        aiempi_päivämäärä()
    
    
 

    #print(ulos_hinnat)

    return ulos_tunnit, ulos_hinnat, pvm


def aiempi_päivämäärä():
    global mikäpvä
    mikäpvä -= 1
    if (mikäpvä == -1):
        vasen_nappi["state"] = DISABLED
    if (mikäpvä < 1):
        oikea_nappi["state"] = NORMAL
    eri_päivä = mikäpvä
    piirturi(eri_päivä)


def seuraava_päivämäärä():
    global mikäpvä
    mikäpvä += 1
    if (mikäpvä == 1):
        oikea_nappi["state"] = DISABLED
    if (mikäpvä < 1):
        vasen_nappi["state"] = NORMAL
    eri_päivä = mikäpvä
    piirturi(eri_päivä)


def piirturi(eri_päivä = 0):
    ulos_tunnit, ulos_hinnat, pvm = luo_graafi(eri_päivä)  
    teksti.delete("1.0", END)
    teksti.insert("end", pvm + " sähkön hinta")

    global figure
    figure.clear()

    axes = figure.add_subplot()
    axes.bar(ulos_tunnit, ulos_hinnat)
    axes.set_xlabel("Tunnit")
    axes.set_ylabel("Hinta [snt/kWh]")
    figure.canvas.draw_idle()
    figure_canvas.get_tk_widget().pack(side= "bottom", fill= "both", expand=1) 


def sulku():
    root.destroy()
    exit()


def main():
    ulos_tunnit, ulos_hinnat, pvm = luo_graafi()
    piirturi()
    root.mainloop()

####################
#Globaalit muuttujat
####################

pvm = str(datetime.datetime.now()).split()[0]
root = Tk()

#mpl canvas asetukset
figure = Figure(figsize=(6, 4), dpi=100)
figure_canvas = FigureCanvasTkAgg(figure, root)

# Ikkunan asetukset
root.geometry('800x450') 
root.title("Sähkön hinta")
root.protocol("WM_DELETE_WINDOW", sulku)

# UI olioiden luonti
vasen_nappi = Button(root, text = "<", bd= "5", command = aiempi_päivämäärä)
oikea_nappi = Button(root, text = ">", bd= "5", command = seuraava_päivämäärä)
teksti = Text(root, height = 1, width = 40)
vasen_nappi.pack(side = "left")
oikea_nappi.pack(side = "right")
teksti.pack(side = "top")
teksti.insert("end", pvm + " sähkön hinta")

mikäpvä = 0
    
#Voidaan ajaa vain suoraan invokoituna
if __name__ == "__main__": 
    main()
else:
    exit()
