"""
EE250 Project - Smart HVAC

Hardware Components:
- GrovePi Board
- LCD RGB Backlight
- /// Ultrasonic Ranger (D4) ///
- Temperature & Humidity Sensor (D7)
- Rotary Angle Sensor (D4)
- Relay (D3)
- Buzzer (D2)

Software Components:
- GrovePi library
- Flask web framework

Display current temp & humidity on LCD
Rotary Angle Sensor: adjust to set temp & humidity
Relay: AC Control
Buzzer: alert if temp/humidity go past desirable range

Flask web framework: view current and adjust temp & humidity and AC Control

Requirement Check:
Physical Nodes (2) - Raspberry Pi, Laptop
Data collection from Sensor - Temperature & Humidity Sensor
Signal or data processing - Automatic AC Control (Relay)
Node-to-node communication - between RPi and Laptop
Visualization and control - MQTT server (publish/subscribe)
"""

import grovepi
import time
from grove_rgb_lcd import *
#import requests
#from threading import Thread

th_sensor_port = 7
rotary_angle_sensor_port = 0
button_port = 4
relay_port = 3
buzzer_port = 2
lcd_port = 1

setRGB(0, 128, 64)

grovepi.pinMode(th_sensor_port, "INPUT")
grovepi.pinMode(rotary_angle_sensor_port, "INPUT")
grovepi.pinMode(button_port, "INPUT")
grovepi.pinMode(relay_port, "OUTPUT")
grovepi.pinMode(buzzer_port, "OUTPUT")

temperature = 0
humidity = 0
HVAC_on = False

temperature = grovepi.dht(th_sensor_port, 0)[0]
humidity = grovepi.dht(th_sensor_port, 0)[1]

'''
def control_HVAC():
    global HVAC_on
    if temperature > 25:
        grovepi.digitalWrite(relay_port, 1)
        HVAC_on = True
    elif temperature < 20:
        grovepi.digitalWrite(relay_port, 0)
        HVAC_on = False
'''
'''
def send_data():
    global temperature, humidity, HVAC_on
    data = {'temperature': temperature,
            'humidity': humidity,
            'HVAC_on': HVAC_on}
    requests.post('https://localhost:5000/data', json=data)
'''
'''
read_temperature_humidity_thread = Thread(target=read_temperature_humidity)
control_HVAC_thread = Tread(target=control_HVAC)

read_temperature_humidity_thread.start()
control_HVAC_thread.start()
'''
while True:
    #send_data()
    #time.sleep(1)
    [temperature, humidity] = grovepi.dht(th_sensor_port, 0)
    temperature = (temperature * 1.8) + 32

    dial = grovepi.analogRead(rotary_angle_sensor_port)
    temp_range = (dial * 50) / 1023 + 40

    if temperature > temp_range:
        grovepi.digitalWrite(relay_port, 1)
        HVAC_on = True
        #setText_norefresh("DT:{0:.0f}F AC ON \nT:{1:.0f}F H:{2:.0f}%".format(temp_range, temperature, humidity))
    else:
        grovepi.digitalWrite(relay_port, 0)
        HVAC_on = False
        #setText_norefresh("DT:{0:.0f}F AC OFF\nT:{1:.0f}F H:{2:.0f}%".format(temp_range, temperature, humidity))

    if humidity > 80:
        grovepi.digitalWrite(buzzer_port, 1)
    else:
        grovepi.digitalWrite(buzzer_port, 0)

    button_state = grovepi.digitalRead(button_port)

    if button_state == HIGH:
        HVAC_on = False
        setText("Emergency/nReboot")
    else:
        HVAC_on = True

    if HVAC_on == True:
        setText_norefresh("AC ON   DT:{0:.0f}F\nT:{1:.0f}F H:{2:.0f}%".format(temp_range, temperature, humidity))
    else:
        setText_norefresh("AC OFF  DT:{0:.0f}F\nT:{1:.0f}F H:{2:.0f}%".format(temp_range, temperature, humidity))    