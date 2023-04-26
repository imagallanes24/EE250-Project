import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code "+str(rc))
    client.subscribe("imagalla/temp")
    client.subscribe("imagalla/humid")
    client.subscribe("imagalla/HVAC")

    client.message_callback_add("imagalla/temp", on_message_from_temp)
    client.message_callback_add("imagalla/humid", on_message_from_humid)
    client.message_callback_add("imagalla/HVAC", on_message_from_HVAC)

def on_message(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload, "utf-8"))

def on_message_from_temp(client, userdata, message):
    print("Current Temperature: " + message.payload.decode())
def on_message_from_humid(client, userdata, message):
    print("Current Humidity: " + message.payload.decode())
def on_message_from_HVAC(client, userdata, message):
    print("HVAC: " + message.payload.decode())
    
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    client.connect(host="68.181.32.115", port=11000, keepalive=60)

    client.loop_forever()