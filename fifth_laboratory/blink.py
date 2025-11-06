from machine import Pin, PWM
import machine
from utime import sleep
import utime
import urequests
import gc
import json
moteur = PWM(Pin(20))
button = machine.Pin(16, machine.Pin.IN)
moteur.freq(100)

#while True:
#    moteur.duty_u16(7250)
#    sleep(1)
  #  moteur.duty_u16(10500)
 #   sleep(1)
#


import network
import time
import socket
import ntptime
import sys
 
 
ssid = 'plc-511'       # 🔁 Remplace par le nom de ton réseau Wi-Fi
password = 'TOMHWVEGGSZQZHAT'  # 🔁 Remplace par ton mot de passe Wi-Fi
 
wlan = network.WLAN(network.STA_IF)  
wlan.active(True) 
print(wlan.scan())                   
wlan.connect(ssid, password)         
 
# Attente de la connexion
max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    print('Connexion en cours...')
    time.sleep(1)
    max_wait -= 1
 
if wlan.isconnected():
    print('Connecté !')
    print('Adresse IP :', wlan.ifconfig()[0])
else:
    print('Échec de connexion.')

initial_time = 17000
final_time =4000 
last_time = utime.ticks_ms()
last_time_bottom=last_time
affichage = last_time
buttom_pressed=0

time_utc = ["Etc/GMT","Etc/GMT+0","Etc/GMT+1","Etc/GMT+10","Etc/GMT+11","Etc/GMT+12","Etc/GMT+2","Etc/GMT+3","Etc/GMT+4","Etc/GMT+5","Etc/GMT+6","Etc/GMT+7","Etc/GMT+8","Etc/GMT+9","Etc/GMT-0","Etc/GMT-1","Etc/GMT-10","Etc/GMT-11","Etc/GMT-12","Etc/GMT-13","Etc/GMT-14","Etc/GMT-2","Etc/GMT-3","Etc/GMT-4","Etc/GMT-5","Etc/GMT-6","Etc/GMT-7","Etc/GMT-8","Etc/GMT-9","Etc/GMT0","Etc/Greenwich","Etc/UCT","Etc/UTC","Etc/Universal","Etc/Zulu"]

index = 0
change =True
heure_ref = 12
i = 0
pressed = False
first = True
heure = 0
h = "pas ok"
while True:
    try:
  
        new_time = utime.ticks_ms()
        if button.value()==1 :
            
            if new_time-boutom_pressed>1000:
                index +=1
                boutom_pressed=new_time
                print(index)
                print(time_utc[index])
            if new_time-last_time_bottom>250:
                last_time_bottom=new_time
                if change:
                    change = False
                    heure_ref = 24
                else :
                    change = True
                    heure_ref = 12
                print("l'heure de ref est :",heure_ref)

        else :
            boutom_pressed=new_time

        if (new_time-affichage)>5000:
            affichage=new_time
            print(time_utc[index])
            print("l'heure de la référence",heure_ref)
            print("la fréquence est de", freq)
            print(heure)
            print(h)

        if (new_time-last_time)>6000 or first:
            first = False
            last_time=new_time
            try :
                print("######################################")
                response =urequests.get(f'https://worldtimeapi.org/api/timezone/{time_utc[index]}')
                
                data =(response.json())
                datetime_str = data['datetime']
                gtm = data['timezone']
                print("Le gtm renvoyé par l'api est : ",gtm)
                heure  = int(datetime_str[11:13])   # 08
                minute = int(datetime_str[14:16])   # 56
                seconde = int(datetime_str[17:19])  # 28
                
                response.close()
                gc.collect()
                
                print(heure)
                 
            except Exception as e:
                gc.collect()
                print("erreur")
                print(e)
        if change:
            heure = heure%12
            h = "ok"
        
        freq = int((13000/heure_ref)*(heure)+4000)
        #print(freq)
        moteur.duty_u16(freq)   

    except KeyboardInterrupt:
            print("fin")
            sys.exit()


 