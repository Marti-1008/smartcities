from machine import Pin, PWM
import machine
from utime import sleep
import utime

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
 
 
ssid = 'electroProjectWifi'       # 🔁 Remplace par le nom de ton réseau Wi-Fi
password = 'B1MesureEnv'  # 🔁 Remplace par ton mot de passe Wi-Fi
 
wlan = network.WLAN(network.STA_IF)  
wlan.active(True)                    
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

time_utc = 0
passage = True
while passage:
    try :
        ntptime.settime()
        passage = False 
    except :
        print("erreur")
while True:
    try:
        new_time = utime.ticks_ms()
        if button.value()==1 and (new_time-last_time)>500:
            last_time= new_time
            time_utc = time_utc +1
            print("passage")

        heure = time.localtime()[3]
        if (heure+time_utc)%12!=0:
            heure = (heure+time_utc)%12            
        print(heure)
        
        print(int((13000/12)*(time_utc+heure))+4000)
        moteur.duty_u16(int((13000/60)*(heure+time_utc)+4000))
        

        print("Local time before synchronization：%s" %str(time.localtime()))
        


    except KeyboardInterrupt:
        print("fin")
        sys.exit()
        
    except Exception as e:
        print("❌ Erreur NTP :", e)
        print("erreur")
        sleep(2)

# ou 

#Try:
 #   while True:
  #      print("Local time before synchronization：%s" %str(time.localtime()))
   #     ntptime.settime()
    #    print("Local time after synchronization：%s" %str(time.localtime()))
      #  sleep(5)
#except:
#    print("erreur")

 