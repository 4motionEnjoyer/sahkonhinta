#!/usr/bin/python3
# Asennusskripti sähkönhinta.py lle.
# Tsekkaa järjestelmän ja kysyy tyhmiä
# 

from sys import platform
import sys
import subprocess
import shutil
import os

def cmd(käsky):
    konsoli = subprocess.Popen(käsky, shell=False, stdout=subprocess.PIPE)
    ulostulo = str(konsoli.communicate()[0])
    paluuarvo = ulostulo.strip("b'")
    paluuarvo = paluuarvo[:-2]

    return paluuarvo


def main():
    poisto = False
    print("Valitse toiminto: (a)sennus, (p)oistaminen")
    vastaus = input()
    match vastaus:
        case "a":
            paketit = [ "matplotlib", "numpy", "requests" ]
            for paketti in paketit:
                subprocess.check_call([sys.executable, "-m", "pip", "install", paketti])
                
        case "p":
            poisto = True
        
        case _ :
            print("Vastaa joko j tai e")
            exit()

    
    
    if platform == "win32": 
        alusta = "win"
        kohde = os.path.join( "C:\\", "Users", str(cmd("whoami")).split("\\")[2], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "sähkönhinta.pyw")
    if platform == "linux" or platform == "linux2": 
        alusta = "lin"
        binpolku = "/home/" + str(cmd("whoami")) + "/.local/bin/sähkönhinta.py"
    if poisto: 
        match alusta:
            case "win":
                try:
                    os.remove(kohde)
                    print("Asennus poistettu")
                    
                except:
                    print("Softaa ei ole asennettu")
                exit()    

            case "lin":
                try:
                    käsky = str("rm " + binpolku)
                    #arsi = cmd(käsky)
                    arsi = subprocess.run(käsky)
                    print(arsi)
                    print("Asennus poistettu")
                    
                except Exception as e:
                    print("Softan poisto epäonnistui: " + str(e))
                exit()    


    if alusta == "win": print("\n Haluatko pikakuvakkeen työkansioon? j/e")
    if alusta == "lin": print("\n Haluatko pikakäyttöintegraation bashiin? j/e")
    vastaus = input()
    match vastaus:
        case "j":
            if alusta == "win":
                #with open("sähkönhinta.bat", "w") as filu:
                #    filu.write("@echo off \n")
                #    filu.write("")
                #    filu.write("python sähkönhinta.pyw \n")
                
                #print (kohde)   
                #exit()
                kohde = os.path.join( "C:\\", "Users", str(cmd("whoami")).split("\\")[2], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup\\")
                shutil.copy("sähkönhinta.pyw", kohde)
                print("\n Asennus onnistui")
            
            if alusta == "lin":
                shutil.copyfile("./sähkönhinta.py", binpolku)
                os.popen("chmod +x " + binpolku)
                print("\n Asennus onnistui")
        
        case "e":
                print("\n Asennus onnistui")
                exit()

        case _ :
                print("Vastaa joko j tai e")
                exit()

if __name__ == "__main__":
    main()
