import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code "+str(rc))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    time.sleep(1)

    while True:
        client.publish("imagalla/temp", f"{temperature}")
        print("Publishing temperature data")
        client.publish("imagalla/humid", f"{humidity}")
        print("Publishing humidity data")
        client.publish("imagalla/HVAC", f"{HVAC}")
        print("Publishing HVAC data")