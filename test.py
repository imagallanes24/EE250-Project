"""
TESTING FILE:
Humidity Level for Emergency Alert changed to > 80%
"""
import grovepi
import time
from datetime import datetime, timedelta
from grove_rgb_lcd import *
import paho.mqtt.client as mqtt

th_sensor_port = 7
rotary_angle_sensor_port = 0
relay_port = 3
buzzer_port = 2
lcd_port = 1

setRGB(0, 128, 64)

grovepi.pinMode(th_sensor_port, "INPUT")
grovepi.pinMode(rotary_angle_sensor_port, "INPUT")
grovepi.pinMode(relay_port, "OUTPUT")
grovepi.pinMode(buzzer_port, "OUTPUT")

temperature = 0
humidity = 0
HVAC_on = False

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code "+str(rc))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="172.20.10.4", port=1883, keepalive=60)
    client.loop_start()
    time.sleep(1)

    next_publish_time = datetime.now() + timedelta(seconds=5)

    while True:
        [temperature, humidity] = grovepi.dht(th_sensor_port, 0)
        temperature = (temperature * 1.8) + 32

        dial = grovepi.analogRead(rotary_angle_sensor_port)
        temp_range = (dial * 50) / 1023 + 40

        now = datetime.now()
        dateinfo = now.strftime("%m/%d/%Y")
        timeinfo = now.strftime("%H:%M:%S")
        dateandtime = f"{dateinfo} {timeinfo}"

        if temperature > temp_range:
            grovepi.digitalWrite(relay_port, 1)
            HVAC_on = True
        else:
            grovepi.digitalWrite(relay_port, 0)
            HVAC_on = False

        emer_str = "HIGH HUMIDITY (POSSIBLE FIRE)"
        if humidity > 80:
            grovepi.digitalWrite(buzzer_port, 1)
            client.publish("imagalla/emergencyalert", "{}".format(emer_str))
            setRGB(200,0,0)
        else:
            grovepi.digitalWrite(buzzer_port, 0)
            setRGB(0, 128, 64)
        
        HVAConoff = ""
        if HVAC_on == True:
            setText_norefresh("DT:{0:.0f}F AC ON \nT:{1:.0f}F H:{2:.0f}%".format(temp_range, temperature, humidity))
            HVAConoff = "ON"
        else:
            setText_norefresh("DT:{0:.0f}F AC OFF\nT:{1:.0f}F H:{2:.0f}%".format(temp_range, temperature, humidity))   
            HVAConoff = "OFF"

        if now >= next_publish_time:
            client.publish("imagalla/datetime", "{}".format(dateandtime))
            print("Publishing datetime data")
            client.publish("imagalla/temp", "{}".format(temperature))
            print("Publishing temperature data")
            client.publish("imagalla/humid", "{}".format(humidity))
            print("Publishing humidity data")
            client.publish("imagalla/HVAC", "{}".format(HVAConoff))
            print("Publishing HVAC data")
            next_publish_time = now + timedelta(seconds=5)