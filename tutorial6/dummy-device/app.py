# compose_flask/app.py
import random, logging, csv, time, requests, json
from flask import Flask, request, jsonify
from multiprocessing import Process, Value

# Create a shared memory variable for parallel processing
SEND = Value("b", False)

app = Flask(__name__)

# Index route. Just to check if container is working properlu
@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello, World"


# Check for a json message
@app.route("/health", methods=["GET", "POST"])
def healthRandom():
    return jsonify({"status": "ok"})


# Receive the command from the IoT Agent JSON
@app.route("/device1", methods=["GET", "POST"])
def lamp():
    if request.method == "POST":
        data = request.json
        app.logger.info(data)
        if "switch" in data:
            global SEND
            if SEND.value == True:
                SEND.value = False
                return jsonify({"switch": "Stopped sending data"}), 200
            else:
                data = request.json
                SEND.value = True
                return jsonify({"switch": "Started sending data"}), 200
        else:
            return jsonify({"message": "Method not allowed"}), 405

def sendData():
    while True:
        print("reading")
        if SEND.value:
            url = "http://fiware-iot-agent-json:7896/iot/json?k=4jggokgpepnvsb2uv4s40d59ov&i=device001"

            payload = json.dumps({
                "t": random.randint(10, 40),
                "rh":  random.randint(0, 100)
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
        time.sleep(5)


p = Process(target=sendData).start()

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=80, debug=True)
    sendData()
