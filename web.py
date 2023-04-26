import json
from flask import Flask, request, render_template
import paho.mqtt.publish as publish

app = Flask(__name__)

# Define index route to render template
@app.route("/")
def index():
    return render_template('index.html')

# Define route to receive form data and publish to MQTT topic
@app.route("/temperature", methods=['POST'])
def temperature():
    temperature = request.form['temperature']
    data = {"temperature": int(temperature)}
    publish.single("smart_hvac/temperature", payload=json.dumps(data), hostname="localhost")
    return "Temperature set to: " + temperature

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')