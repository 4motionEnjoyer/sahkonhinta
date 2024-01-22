#!/bin/python
#
##################################################
#Sähkönhinta widgetti, tänään +-1 pvä
#By 4motionEnjoyer / Leevi S.
###################################################

##############
#Importit
##############
import random
import sys
import requests
import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from tkinter import *
from tkinter import messagebox
import threading
import time

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

##############
#Funktiot
##############

def kellonkyttäys():
    if datetime.datetime.now().time() > datetime.time(0,0, 0) and datetime.datetime.now().time() < datetime.time(14, 15, 00) and pvm_diff == 0:
        oikea_nappi["state"] = DISABLED
    else:
        oikea_nappi["state"] = NORMAL 


def varoitus_ikkuna():
#    päällimmäinen = Toplevel(root)
#    päällimmäinen.geometry("400x150")
#    päällimmäinen.title("Varoitus")
#    Label(päällimmäinen, text = "Jostain syystä dataa ei saatu. Nordpool julkaisee seuraavan päivän datat ~14:00")
    v_ikkuna = messagebox.showerror("Varoitus", "Sovellus ei saanut dataa netistä")
    if v_ikkuna == "No":
        exit()
    else:
        pass

def keksi_data():
    global pävät_tietue
    global pvm
    #päivät_tietue["ulos_tunnit"] = list(range(0,24))
    print (päivät_tietue["ulos_tunnit"])
 #   päivät_tietue["ulos_hinnat_eilen"] = []
  #  päivät_tietue["ulos_hinnat_tänään"] = []
   # päivät_tietue["ulos_hinnat_huomenna"] = []
    
#    ulos_tunnit = range(0, 24)
#    ulos_hinnat_eilen = []
#    ulos_hinnat_tänään = []
#    ulos_hinnat_huomenna = []


    while(len(päivät_tietue["ulos_hinnat_tänään"]) < 24):
        päivät_tietue["ulos_hinnat_eilen"].append(random.randrange(1, 30))
        päivät_tietue["ulos_hinnat_tänään"].append(random.randrange(1, 30))
        päivät_tietue["ulos_hinnat_huomenna"].append(random.randrange(1, 30))

    pvm = str(datetime.datetime.now() + datetime.timedelta(days=0)).split()[0]
    #return hinta_tietue


def hae_data():
    global päivät_tietue
    global pvm
    pvm = str(datetime.datetime.now() + datetime.timedelta(days=0)).split()[0]
    if db_lippu: print (päivät_tietue["ulos_tunnit"])

    api_url_eilen = "https://www.sahkohinta-api.fi/api/v1/kallis?tunnit=24&tulos=sarja&aikaraja=" + str(datetime.datetime.now() + datetime.timedelta(days=-1)).split()[0]
    api_url_tänään = "https://www.sahkohinta-api.fi/api/v1/kallis?tunnit=24&tulos=sarja&aikaraja=" +  str(datetime.datetime.now() + datetime.timedelta(days=0)).split()[0]
    api_url_huomenna = "https://www.sahkohinta-api.fi/api/v1/kallis?tunnit=24&tulos=sarja&aikaraja=" + str(datetime.datetime.now() + datetime.timedelta(days=1)).split()[0]

    vastaus_eilen = requests.get(api_url_eilen)
    vastaus_tänään = requests.get(api_url_tänään)
    vastaus_huomenna = requests.get(api_url_huomenna)

    binaari_eilen = vastaus_eilen.content
    binaari_tänään = vastaus_tänään.content
    binaari_huomenna = vastaus_huomenna.content

    try:
        ulos_json_eilen = json.loads(binaari_eilen)
        ulos_json_tänään = json.loads(binaari_tänään)
        if datetime.datetime.now().time() > datetime.time(14,15,0):
            ulos_json_huomenna = json.loads(binaari_huomenna)
        else:
            ulos_json_huomenna = "before14"
        ulos_list_eilen = list(ulos_json_eilen)
        ulos_list_tänään = list(ulos_json_tänään)
        ulos_list_huomenna = list(ulos_json_eilen)

        ulos_tunnit_eilen = []
        ulos_tunnit_tänään = []
        ulos_tunnit_huomenna = []


        ulos_hinnat_eilen = []
        ulos_hinnat_tänään = []
        ulos_hinnat_huomenna = []

        for tunti in ulos_list_eilen:
            als = str(tunti.get("aikaleima_suomi")) #als aikaleimasuomi
            als_trimmed = als.split("T")
            hinta = float(tunti.get("hinta"))
            ulos_tunnit_eilen.append(als_trimmed[1].split(":")[0])
            ulos_hinnat_eilen.append(hinta)
        päivät_tietue["ulos_hinnat_eilen"] = ulos_hinnat_eilen
        if db_lippu: print(päivät_tietue["ulos_hinnat_eilen"])
        
        for tunti in ulos_list_tänään:      #boilerplate, vois tehdä viisaamminki
            als = str(tunti.get("aikaleima_suomi")) #als aikaleimasuomi
            als_trimmed = als.split("T")
            hinta = float(tunti.get("hinta"))
            ulos_tunnit_tänään.append(als_trimmed[1].split(":")[0])
            ulos_hinnat_tänään.append(hinta)
        päivät_tietue["ulos_hinnat_tänään"] = ulos_hinnat_tänään
        if db_lippu: print(str(päivät_tietue["ulos_hinnat_tänään"]))

        for tunti in ulos_list_huomenna:
            als = str(tunti.get("aikaleima_suomi")) #als aikaleimasuomi
            als_trimmed = als.split("T")
            hinta = float(tunti.get("hinta"))
            ulos_tunnit_huomenna.append(als_trimmed[1].split(":")[0])
            ulos_hinnat_huomenna.append(hinta)
        päivät_tietue["ulos_hinnat_huomenna"] = ulos_hinnat_huomenna
        if db_lippu: print(str(päivät_tietue["ulos_hinnat_huomenna"]))
        

    except Exception as e:
        print("Joko käytit liikaa API kutsuja (60 tunnissa sallittu) tai huomisen dataa ei ole julkaistu, yleensä klo 14:00 eteenpäin. Alla tulkin sepustus")
        print("\n")
        print(str(e))
        print("\nYritä myödemmin uudelleen")
        aiempi_päivämäärä()
        varoitus_ikkuna()

    #print(ulos_hinnat)

    #return ulos_tunnit, ulos_hinnat_eilen, ulos_hinnat_tänään, ulos_hinnat_huomenna, pvm


def aiempi_päivämäärä():
    global pvm_diff
    pvm_diff -= 1
    if (pvm_diff == -1):
        vasen_nappi["state"] = DISABLED
    if (pvm_diff < 1):
        oikea_nappi["state"] = NORMAL

    piirturi()


def seuraava_päivämäärä():
    global pvm_diff
    global keksi_lippu
    global db_lippu
    if keksi_lippu and db_lippu:    #testing purposes
        varoitus_ikkuna()
    else:
        pvm_diff += 1
        if (pvm_diff == 1):
            oikea_nappi["state"] = DISABLED
        if (pvm_diff < 1):
            vasen_nappi["state"] = NORMAL
        kellonkyttäys() 
        piirturi()


#def piirturi(eri_päivä = 0):
def piirturi(): 
    global keksi_lippu
    global pvm_diff
    global pvm
    global päivät_tietue

    #global ulos_hinnat_eilen, ulos_hinnat_tänään, ulos_hinnat_huomenna
#    if not keksi_lippu:
#        ulos_tunnit, ulos_hinnat, pvm = hae_data(eri_päivä)  
#         ulos_tunnit, ulos_hinnat_eilen, ulos_hinnat_tänään, ulos_hinnat_huomenna = hae_data() 
#       pass 
#else:
#        ulos_tietue = keksi_data()

    teksti.delete("1.0", END)
    teksti.insert("end", str(datetime.datetime.now().date() + datetime.timedelta(days = pvm_diff)) + " sähkön hinta")

    global figure
    figure.clear()

    axes = figure.add_subplot()
    match pvm_diff:
        case -1:
            ulos_hinnat = päivät_tietue["ulos_hinnat_eilen"]
            if db_lippu: print("case -1")
        case 0:
            ulos_hinnat = päivät_tietue["ulos_hinnat_tänään"]
            if db_lippu: print("case 0")
        case 1:
            ulos_hinnat = päivät_tietue["ulos_hinnat_huomenna"]
            if db_lippu: print("case + 1")

    if db_lippu:
        print("tyyppi " + str(type(päivät_tietue["ulos_hinnat_eilen"])) + " pituus" + str(len(päivät_tietue["ulos_hinnat_eilen"])))
        print("tyyppi " + str(type(ulos_hinnat)) + " pituus " + str(len(ulos_hinnat)))
        print("ulos_hinnat_eilen on: " + str(päivät_tietue["ulos_hinnat_eilen"]))
        print("ulos_hinnat_tänää on: " + str(päivät_tietue["ulos_hinnat_tänään"]))
        print("ulos_hinnat_huome on: " + str(päivät_tietue["ulos_hinnat_huomenna"]))
    axes.bar(päivät_tietue["ulos_tunnit"], ulos_hinnat)
    axes.set_xlabel("Tunnit")
    axes.set_ylabel("Hinta [snt/kWh]")
    figure.canvas.draw_idle()
    figure_canvas.get_tk_widget().pack(side= "bottom", fill= "both", expand=1) 


def sulku():
    root.destroy()
    exit()

def argumenttiparsija():
    argumentit = []
    for argumentti in sys.argv:
        argumentit.append(argumentti)
    return argumentit, len(argumentit)


def main():
    argumentit, alkm = argumenttiparsija()
    global päivät_tietue
    
    kellonkyttäys()

    if "db" in argumentit:
        global db_lippu 
        db_lippu = True
    if "offline" in argumentit:
#        ulos_tunnit, ulos_hinnat, pvm = keksi_data()
        global keksi_lippu
        keksi_lippu = True
        keksi_data()
    else:
        hae_data()

    piirturi()
    root.mainloop()

####################
#Globaalit muuttujat
####################

päivät_tietue = {}

päivät_tietue["ulos_tunnit"] = [] 
päivät_tietue["ulos_tunnit"] = list(range(0,24))
päivät_tietue["ulos_hinnat_eilen"] = []
päivät_tietue["ulos_hinnat_tänään"] = []
päivät_tietue["ulos_hinnat_huomenna"] = []

#ulos_hinnat_eilen = []
#ulos_hinnat_tänään = []
#ulos_hinnat_huomenna = []

db_lippu = False
keksi_lippu = False
pvm = str(datetime.datetime.now()).split()[0]
pvm_diff = 0
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
