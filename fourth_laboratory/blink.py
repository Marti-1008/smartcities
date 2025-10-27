from ws2812 import WS2812
from machine import ADC
import utime

def red(led_value, noise_mean) :
    color_red = int((noise_mean-13000)*4.87*10**-3-(-2*led_value)*2)
    if 255>color_red and color_red>0 :
        return color_red
    else : 
        return int((noise_mean-13000)*4.87*10**-3)


def green(BPM_now, led_value):
    color_green = int(0.853333*BPM_now-(led_value-2)*2)
    if 255>color_green and color_green >0:
        return color_green
    else : 
        return int(0.853333*BPM_now)

def blue (last_noise, led_value):
    color_blue = int((last_noise-13000)*4.87*10**-3-(led_value+5)*2)
    if 255>color_blue and color_blue >0:
        return color_blue
    else :
        return int((last_noise-13000)*4.87*10**-3)

 


BPM_now = 0
RGB = WS2812(20,1) # le 1 représente le nombre de LED qu'il y a en série
sound_sensor = ADC(0)
noise_list=[]
last_noise = 0
NO_noise = 13000 # la valeur retournée quand il n'y a pas de son et musique (bruit, ...)


led_value = 0


while len(noise_list)!=15:
        noise=(sound_sensor.read_u16())
        if noise!=0:
            noise_list.append(noise)
last_time = utime.ticks_ms()          
last_time_led = last_time
last_time_writte = last_time
k = 0
prise_de_mesure = True
noise_mean= 0
BPM=[]
while True:
    led_value = led_value+1
    if led_value>10:
        led_value= -10
    while prise_de_mesure:

        noise=(sound_sensor.read_u16())
        if noise!=0:
            del noise_list[0]
            noise_list.append(noise)
            prise_de_mesure = False
    prise_de_mesure = True
    last_noise =noise_mean
    noise_mean=0
    for i in range(15):
        noise_mean +=noise_list[i]
    noise_mean = noise_mean/15
    diff = noise_mean-last_noise
    noise_mean=(noise_mean)*0.8+0.2*diff
    new_time = utime.ticks_ms()
    
    
    if noise_mean > last_noise and  new_time-last_time >200 and noise_mean>NO_noise : # correspond à 300 BPM
        print(noise_mean)
        BPM_now = 60000/(new_time-last_time)
        BPM.append(BPM_now)
        last_time= new_time
        last_noise = noise_mean*0.95 # pics
        print(BPM_now)
        
    if new_time-last_time_writte>6000 :
        last_time_writte=new_time
        if len(BPM)!=0:
            bpm = sum(BPM)/len(BPM)
            BPM.clear()
        else :
            bpm=0

        #try:
            #with open("bpm_log.txt", "a") as f: # la structure with ferme automatiquement
                    #f.write(f"{utime.localtime()}: {bpm:.1f} BPM\n")
                    #print("Valeur enregistrée dans bpm_log.txt")
        #except Exception as e:
                #print("Erreur d’écriture dans le fichier :", e) # e contient l'objet d'excetion
            
        print("le BPM moyen est de ",bpm)
    if new_time-last_time_led > 200:
        color = red(led_value, noise_mean), green(BPM_now, led_value), blue(last_noise, led_value)
        RGB.pixels_fill(color)
        RGB.pixels_show()
        last_time_led=new_time

    
    
