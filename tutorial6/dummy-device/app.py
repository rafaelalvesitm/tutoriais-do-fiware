# compose_flask/app.py
import random, logging
from flask import Flask, request, jsonify, abort

SEND = False

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello, World"

@app.route('/health', methods=['GET', 'POST'])
def healthRandom():
    return jsonify({"status": "ok"})

@app.route('/device1', methods=['GET', 'POST'])
def lamp():
    if request.method == "POST":
        data = request.json
        app.logger.info(data)
        if "switch" in data:
            global SEND
            if SEND == True:
                SEND = False
                return jsonify({"switch": "Stopped sending data"}), 200
            else:
                data = request.json
                SEND = True
                return jsonify({"switch": "Started sending data"}), 200
        else:
            return jsonify({"message": "Method not allowed"}), 405



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)