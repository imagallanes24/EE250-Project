import grovepi
import time
import socket

# set up temperature and humidity sensor
sensor = 7

# set up LCD display
lcd = 2

# set up ultrasonic ranger
ultrasonic_ranger = 4

# set up button
button = 3

# set up buzzer
buzzer = 8

# set up RGB backlight
rgb_backlight = 5

# set up socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
client_socket.connect(('localhost', 8000))

# main loop
while True:
    try:
        # read temperature and humidity from sensor
        [temp, humidity] = grovepi.dht(sensor, 0)

        # read distance from ultrasonic ranger
        distance = grovepi.ultrasonicRead(ultrasonic_ranger)

        # update LCD display
        lcd_text = f"Temp: {temp:.1f}C\nHumidity: {humidity:.1f}%\nDist: {distance} cm"
        grovepi.lcd.setText(lcd, lcd_text)

        # check button status
        button_status = grovepi.digitalRead(button)
        if button_status:
            # button has been pressed
            grovepi.digitalWrite(buzzer, 1) # turn on buzzer
            grovepi.chainableRgbLedPattern(rgb_backlight, 
