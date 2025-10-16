from machine import Pin, I2C, ADC
from utime import sleep
from lcd1602 import LCD1602
from dht20 import DHT20
import machine,utime






    

i2c = I2C(1)
dht20 = DHT20(i2c)
Rotary_sensor = machine.ADC(2)  
i2c = I2C(0,scl=Pin(9), sda=Pin(8), freq=400000)
display = LCD1602(i2c, 2, 16)




display.display()

display.setCursor(0,0)

buzzer = machine.PWM(machine.Pin(16))
LED = machine.Pin(18, machine.Pin.OUT)


buzzer.freq(1046)
last_time = utime.ticks_ms()
last_time_delete = last_time
last_time_temp = last_time
temperature = dht20.dht20_temperature()
while True:
    new_time = utime.ticks_ms()
    resistance = Rotary_sensor.read_u16()
    temp=int(resistance/3120.761905)+15
        
    if 200 < (new_time-last_time_delete):
        print("hello")
        display.clear()
        last_time_delete = new_time
    if 1000 < (new_time-last_time_temp):
        temperature = dht20.dht20_temperature()
        last_time_temp = new_time

    if 200 < (new_time-last_time):
        last_time=new_time
        display.setCursor(0,0)
        display.print("Ambient:"+"{:.1f}".format(temperature))
        display.setCursor(0,1)
        display.print("SET:"+"{:.1f}".format(temp))

    

    
    if temperature >=  int(resistance/3120.761905)+3+15:
        display.setCursor(0,1)
        display.print("ALARM")
        buzzer.duty_u16(12000)
    else :
        buzzer.duty_u16(0) 
        
        
        
    


