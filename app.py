import json
import time
import paho.mqtt.client as mqtt
import grovepi
from grovepi import *
from grove_rgb_lcd import *

# Set pin numbers for sensors
temp_hum_sensor = 7
light_sensor = 0
ultrasonic_sensor = 4
rotary_sensor = 2
button = 3
relay = 2
buzzer = 4

# Set sensor types
grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(ultrasonic_sensor,"INPUT")
grovepi.pinMode(rotary_sensor,"INPUT")
grovepi.pinMode(button,"INPUT")
grovepi.pinMode(relay,"OUTPUT")
grovepi.pinMode(buzzer,"OUTPUT")

# Set up MQTT client
client = mqtt.Client("smart_hvac_controller")
client.connect("localhost", 1883, 60)

# Define callback function for MQTT message received
def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    print("Received message:", data)
    set_temperature = data["temperature"]
    current_temperature = grovepi.temp(temp_hum_sensor,'1.1')
    current_humidity = grovepi.temp(temp_hum_sensor,'1.2')
    current_light = grovepi.analogRead(light_sensor)
    current_distance = grovepi.ultrasonicRead(ultrasonic_sensor)
    current_rotary = grovepi.analogRead(rotary_sensor)
    
    # Control HVAC system based on temperature
    if current_temperature > set_temperature:
        grovepi.digitalWrite(relay,1)
        setText("Temperature:\n" + str(current_temperature) + "C\nTurning on AC")
    else:
        grovepi.digitalWrite(relay,0)
        setText("Temperature:\n" + str(current_temperature) + "C\nTurning off AC")
        
    # Alert user if too dark
    if current_light < 300:
        grovepi.analogWrite(buzzer, 255)
        time.sleep(1)
        grovepi.analogWrite(buzzer, 0)
        
    # Alert user if too close
    if current_distance < 50:
        grovepi.analogWrite(buzzer, 255)
        time.sleep(1)
        grovepi.analogWrite(buzzer, 0)
        
# Set up MQTT subscription to receive temperature settings
client.subscribe("smart_hvac/temperature")

# Loop to continuously receive MQTT messages
client.loop_forever()
