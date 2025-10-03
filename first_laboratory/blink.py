import machine
import utime
 
 
 
LED = machine.Pin(16, machine.Pin.OUT) # pin 16
button = machine.Pin(20, machine.Pin.IN) #pin 20
on = 1
off = 0
last_time = utime.time_ns()
etat_led = "on"
valeur_bouton=0
new_time_before = last_time
while True:
    index = button.value()
   
    new_time = utime.time_ns()
    Break = 2.5e8/(1+ valeur_bouton)
    if index ==1 and new_time-new_time_before > 1.5e8:
        valeur_bouton= valeur_bouton+1
        new_time_before =new_time
   
   
    print(valeur_bouton)
    if valeur_bouton == 0 or valeur_bouton == 1:
       
        if etat_led == "off" and new_time-last_time >= Break:
           
            LED.value(on)
            etat_led = "on"
            last_time = utime.time_ns()
        elif new_time-last_time >= Break:
           
            LED.value(off)
            etat_led = "off"
            last_time = utime.time_ns()
 
 
       
    elif valeur_bouton == 2:
        LED.value(off)
       
    else :
        valeur_bouton = 0
# test