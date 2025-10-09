import machine  
import utime 

Rotary_sensor = machine.ADC(0)
buzzer = machine.PWM(machine.Pin(16))
button = machine.Pin(20, machine.Pin.IN)
score = {"DO":[1046, 250],"MI" :[1318, 250], "FA" :[1397, 250],
        "RE":[1175,250], "SOL" : [1568, 500], "LA" :[1760, 125],
        "SI":[1967, 500] }

avengers_theme = [
    "FA", "FA", "LA", "FA",
    "RE", "DO", "RE",
    "FA", "FA", "LA", "FA",
    "RE", "DO", "RE"
]

pirates_theme = [
    "RE", "MI", "FA", "SOL", "FA", "MI", "RE",
    "FA", "SOL", "LA", "SOL", "FA", "MI", "FA"
]

jurassic_park_theme = [
    "FA", "FA", "MI", "RE", "DO",
    "DO", "RE", "MI", "FA",
    "FA", "MI", "RE", "DO"
]

harry_potter_theme = [
    "SI", "MI", "SOL", "FA", "MI",
    "SI", "MI", "SOL", "FA", "RE",
    "SI", "MI", "SOL", "FA", "MI"
]

super_mario_theme = [
    "MI", "MI", "MI",
    "DO", "MI", "SOL",
    "SOL", "DO", "SOL", "MI",
    "LA", "SI", "LA", "SOL", "MI",
    "SOL", "LA", "FA", "SOL"
]


star_wars_theme_simplifie = [
    "SOL", "SOL", "SOL", "MI",
    "SI", "SOL", "MI", "SI", "SOL",
    "RE", "RE", "RE", "MI", "SI", "FA", "MI", "SI", "SOL"
]

nom_musique = [star_wars_theme_simplifie,super_mario_theme,harry_potter_theme,jurassic_park_theme, pirates_theme,avengers_theme]
nom_musique_prime = ["star_wars_theme_simplifie","super_mario_theme","harry_potter_theme","jurassic_park_theme", "pirates_theme","avengers_theme"]

def music_notes(score, notes, last, i) :
    new = utime.ticks_ms() 
    #print(new-last)
    if score[notes][1]<(new - last):
        print("rentre")
        resistance = Rotary_sensor.read_u16() 
        intensity = int(resistance*0.30518)
        buzzer.freq(score[notes][0])
        buzzer.duty_u16(intensity)
        return utime.ticks_ms(), i+1
    return last, i
        

ref_musique = 0
ancien_index =0
i = 0
changement = False
last = utime.ticks_ms()
last_button= utime.ticks_ms()
while True:
    index = button.value()
    new_button = utime.ticks_ms()
    if  250 < (new_button-last_button) and index==1:
        changement = True
        if ref_musique ==5:
            ref_musique =0
        else :
            ref_musique +=1
        last_button= utime.ticks_ms()
    else :
        changement = False

    ancien_index = index
    print(nom_musique_prime[ref_musique])
    while i != (len(nom_musique[ref_musique])) and button.value()!=1 and changement ==False:

        musique = nom_musique[ref_musique]
        Note = musique[i]
        last, i =music_notes(score, Note, last, i)
        
    print("sort")
    i = 0
    
 
   
    
