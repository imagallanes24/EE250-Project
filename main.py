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
import requests
from threading import Thread

th_sensor_port = 7
#ultrasonic_ranger_port = 4
#light_sensor_port = 2
rotary_angle_sensor_port = 4
relay_port = 3
buzzer_port = 2

grovepi.pinMode(th_sensor_port, "INPUT")
grovepi.pinMode(rotary_angle_sensor_port, "INPUT")
grovepi.pinMode(relay_port, "OUTPUT")
grovepi.pinMode(buzzer_port, "OUTPUT")

temperature = 0
humidity = 0
#distance = 0
#light_intensity = 0
HVAC_on = False

def read_temperature_humidity():
    global temperature, humidity
    temperature, humidity = grovepi.dht(th_sensor_port, 0)

'''
def read_distance():
    global distance
    distance = grovepi.ultrasonicRead(ultrasonic_ranger_port)

def read_light_intensity():
    global light_intensity
    light_intensity = grovepi.analogRead(light_sensor_port)
'''
 
def control_HVAC():
    global HVAC_on
    if temperature > 25:
        grovepi.digitalWrite(relay_port, 1)
        HVAC_on = True
    elif temperature < 20:
        grovepi.digitalWrite(relay_port, 0)
        HVAC_on = False

def send_data():
    global temperature, humidity, HVAC_on
    data = {'temperature': temperature,
            'humidity': humidity,
            'HVAC_on': HVAC_on}
    requests.post('https://localhost:5000/data', json=data)

read_temperature_humidity_thread = Thread(target=read_temperature_humidity)
control_HVAC_thread = Thread(target=control_HVAC)

read_temperature_humidity_thread.start()
control_HVAC_thread.start()

while True:
    send_data()
    time.sleep(1)