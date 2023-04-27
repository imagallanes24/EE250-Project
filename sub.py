import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code "+str(rc))
    client.subscribe("imagalla/datetime")
    client.subscribe("imagalla/temp")
    client.subscribe("imagalla/humid")
    client.subscribe("imagalla/HVAC")
    client.subscribe("imagalla/emergencyalert")

    client.message_callback_add("imagalla/datetime", on_message_datetime)
    client.message_callback_add("imagalla/temp", on_message_from_temp)
    client.message_callback_add("imagalla/humid", on_message_from_humid)
    client.message_callback_add("imagalla/HVAC", on_message_from_HVAC)
    client.message_callback_add("imagalla/emergencyalert", on_message_emergency)

def on_message(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload, "utf-8"))

def on_message_datetime(client, userdata, message):
    print("" + message.payload.decode())
def on_message_from_temp(client, userdata, message):
    print("Current Temperature: " + message.payload.decode())
def on_message_from_humid(client, userdata, message):
    print("Current Humidity: " + message.payload.decode())
def on_message_from_HVAC(client, userdata, message):
    print("AC: " + message.payload.decode() + "\n")
def on_message_emergency(client, userdata, message):
    print("" + message.payload.decode())
    
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    client.connect(host="172.20.10.4", port=1883, keepalive=60)

    client.loop_forever()