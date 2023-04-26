import socket
import threading
import RPi.GPIO as GPIO
import time

# set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) # AC unit
GPIO.setup(23, GPIO.OUT) # Heater
GPIO.setup(24, GPIO.OUT) # Fan

# create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host and port
server_socket.bind(('0.0.0.0', 8000))

# listen for incoming connections
server_socket.listen(5)

# function to handle client connections
def handle_client(client_socket):
    while True:
        # receive data from client
        data = client_socket.recv(1024).decode()

        if not data:
            # client has disconnected
            break

        # parse data
        data_parts = data.split(',')
        temp = float(data_parts[0])
        humidity = float(data_parts[1])

        # determine HVAC control
        if temp > 25.0:
            GPIO.output(18, GPIO.HIGH) # turn on AC unit
            GPIO.output(23, GPIO.LOW) # turn off heater
            GPIO.output(24, GPIO.HIGH) # turn on fan
        elif temp < 20.0:
            GPIO.output(18, GPIO.LOW) # turn off AC unit
            GPIO.output(23, GPIO.HIGH) # turn on heater
            GPIO.output(24, GPIO.HIGH) # turn on fan
        else:
            GPIO.output(18, GPIO.LOW) # turn off AC unit
            GPIO.output(23, GPIO.LOW) # turn off heater
            GPIO.output(24, GPIO.LOW) # turn off fan

    # close client socket
    client_socket.close()

# main loop to accept incoming connections
while True:
    client_socket, address = server_socket.accept()
    print(f"Connected to {address[0]}:{address[1]}")

    # start thread to handle client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
