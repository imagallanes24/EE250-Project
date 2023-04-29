# **Final Project: End-to-End Iot System**
## **"Smart HVAC System"** created by Issac Magallanes


Submission Demo Link: [YouTube](https://drive.google.com/file/d/1BxWqBJm5qHQvtorulevsBsMeADJpt_dN/view?usp=sharing)

**Program Instructions:**

First things first, before proceeding, please make sure all the necessary external libraries used for this project are installed on your Raspberry Pi. The only external library needing to be installed on your laptop is `paho.mqtt`.

Now attach the GrovePi shield to your Raspberry Pi. Connect the GrovePi attachments to the following ports:

- LCD RGB Backlight = (I2C-1)
- Temperature & Humidity Sensor = (D7)
- Rotary Angle Sensor = (A0)
- Relay = (D3)
- Buzzer = (D2)

SSH into your Raspberry Pi and cd to this cloned repository. Run `main.py` using the following command.
```
python3 main.py
```
Then, on your laptop, open up a separate terminal window, cd to this cloned repository, and run `sub.py` using the following command.
```
python3 sub.py
```

**External libraries used:**
- grovepi
- grove_rgb_lcd
- paho.mqtt
- time
- datetime

**Installing `grovepi`**: Before attaching the GrovePi shield to your Raspberry Pi, run the following commands on your ssh terminal.
```
echo ~
cd ~
sudo apt-get install curl
sudo curl -kL dexterindustries.com/update_grovepi | bash
```
Now connect the GrovePi shield to the Raspberry Pi and invoke the following commands.
```
cd ~/Dexter/GrovePi/Firmware
./firmware_update.sh
sudo reboot
```
Reconnect to your Raspberry Pi via SSH and run the following commands to confirm the firmware version (1.4.0).
```
cd ~/Dexter/GrovePi/Software/Python
python grove_firmware_version_check.py
```
**Installing `paho.mqtt`**: run the following commands on both your Raspberry Pi and laptop.
```
sudo apt install python3-pip
pip3 install paho-mqtt
```
**Broker install and configuration**: SSH into your Raspberry Pi and run the following commands.
```
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
sudo nano /etc/mosquitto/mosquitto.conf
```
Add to the end of the file:
```
listener 1883
allow_anonymous true
```
Then restart the mosquitto service.
```
sudo systemctl restart mosquitto
```
Also, take note of the IP Address of your Raspberry Pi.
```
hostname -I
```
Now, you can change the IP address in the `main.py` and `sub.py` files to the IP address of your Raspberry Pi.