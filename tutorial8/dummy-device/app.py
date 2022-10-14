import random
import time
import requests
import json

from multiprocessing import Process, Value
from flask import Flask, request, make_response, json

# Define shared variables between process
SEND = Value("b", False)
INTERVAL = Value("i", 5)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    print(f"request: {request.json}")
    return make_response(json.dumps({"on": "method executed"}), 200)


@app.route("/device1", methods=["GET", "POST"])
def device1():
    if request.method == "POST":
        data = request.json
        if "switch" in data:
            if SEND.value == False:
                SEND.value = True
                return make_response(
                    json.dumps({"switch": "Started sending data"}), 200
                )
            elif SEND.value == True:
                SEND.value == False
                return make_response(
                    json.dumps({"switch": "Stopped sending data"}), 200
                )
            else:
                return make_response(json.dumps({"error": "Method not allowed"}), 405)
        elif "interval" in data:
            try:
                INTERVAL.value = int(data["interval"])
                return make_response(json.dumps({"interval": "Interval changed"}), 200)
            except:
                return make_response(json.dumps({"error": "Method not allowed"}), 405)
            return make_response(json.dumps({"error": "Invalid Interval"}), 405)
        else:
            return make_response(json.dumps({"error": "Method not allowed"}), 405)


# Function to save data in a csv file. Running from a thread.
def sendData():
    while True:
        if SEND.value:
            humidity = random.randint(0, 100)
            temperature = random.randint(10, 40)

            url = "http://fiware-iot-agent-json:7896/iot/json?k=4jggokgpepnvsb2uv4s40d59ov&i=device001"

            payload = json.dumps({"t": f"{temperature}", "rh": f"{humidity}"})
            headers = {"Content-Type": "application/json"}

            requests.request("POST", url, headers=headers, data=payload)

        time.sleep(INTERVAL.value)


p = Process(target=sendData).start()

if __name__ == "__main__":
    sendData()
