
import time
import json
import requests

from multiprocessing import Process, Value
from flask import Flask, request, make_response, json


# Define shared variables between process
SEND = Value('b', False)
INTERVAL = Value('i', 5)

# Define the PC IP adress
PC_IP = "192.168.15.9"

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return "Hello, David!", 200

@app.route("/Device/001", methods=['GET', 'POST'])
def device_001():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        if "switch" in data:
            if SEND.value == False:
                print("Problem here")
                SEND.value = True
                return make_response(json.dumps({'switch': 'Sending data'}), 200)
            elif SEND.value == True:
                SEND.value = False
                return make_response(json.dumps({'switch': 'Stopped sending data'}), 200)
        elif "interval" in data:
            try:
                INTERVAL.value = int(data['interval'])
                return make_response(json.dumps({'interval': 'Interval changed'}), 200)
            except:
                return make_response(json.dumps({'error': 'Method not allowed'}), 405)
            return make_response(json.dumps({'error': 'Invalid Interval'}), 405)
        else:
            return make_response(json.dumps({'error': 'Method not allowed'}), 405)

        

# Function to save data in a csv file. Running from a thread.
def sendData():
    while True:
        if SEND.value:
            try:
                humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_GPIOPIN)
            except:
                print("error reading DHT22")

            # try to send message
            url = f"http://{PC_IP}:7896/iot/json?k=4jggokgpepnvsb2uv4s40d59ov&i=device_001"

            payload = json.dumps({
                "t": temperature,
                "rh":  humidity
            })

            headers = {
                'fiware-service': 'openiot',
                'fiware-servicepath': '/',
                'Content-Type': 'application/json'  
            }
            try:
                response = requests.request("POST", url, headers=headers, data=payload)
            except:
                print("Error sending the message")

        time.sleep(INTERVAL.value)

p = Process(target=sendData).start()

if __name__ == "__main__":
    sendData()