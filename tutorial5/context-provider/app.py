# compose_flask/app.py
import random
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route('/health', methods=['GET', 'POST'])
def healthRandom():
    temperature = random.randint(10, 50)
    relativeHumidity = random.randint(0, 100)
    return jsonify({
        "temperature": temperature,
        "relative humidity" : relativeHumidity,
    })

@app.route('/op/query', methods=['GET', 'POST'])
def query():
    response = []
    data = request.json
    try:
        if data['entities']:
            try:
                if data['attrs']:
                    for entity in data['entities']:
                        part = {
                            "id":entity['id'], 
                            "type":entity['type']
                        }
                        for attribute in data['attrs']:
                            if attribute == "temperature":
                                part.update({attribute : {"type": "Number", "value": random.randint(10,40)}})
                            elif attribute == "relativeHumidity":
                                part.update({attribute : {"type": "Number", "value": random.randint(0,100)}})
                            else:
                                part.update({attribute : {"type": "Text", "value": "random"}})
                        response.append(part)
            except:
                return jsonify({'error': 'Body does not contain attributes'}), 400
    except:
        return jsonify({'error': 'Body does not contain entities'}), 400
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)