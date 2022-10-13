import re
import time
import paho.mqtt.client as mqtt
import random

from multiprocessing import Process, Value

# Create shared variables between process
SEND = Value('b', False)
INTERVAL = Value('i', 5)

# Define MQTT client
client = mqtt.Client()
client.connect("mosquitto", 1883, 60)

# The callback for when a message is received from the server.
def on_message(client, userdata, msg):
    # print(f"Topic: {msg.topic}| Payload: {str(msg.payload)}")
    # Parses the message payload described in the FIWARE specification. 
    # the payload is something like "b'<device ID>@<command name>|<command value>'"
    match = re.search(r"[@](.+)[|](.+)'", str(msg.payload)) # regex to parse the payload and get <command name> and <command value>
    command = match.group(1) # command name
    value = match.group(2) # command value

    # Check if the command is the one we want to execute
    if command == "switch":
        if SEND.value == False:
            SEND.value = True
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', "switch_status|OK")
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', "switch_info|Started sending data")
        elif SEND.value == True:
            SEND.value = False
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', "switch_status|OK")
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', "switch_info|Stopped sending data")
    elif command == "interval":
        try:
            INTERVAL.value = int(value)
        except:
            INTERVAL.value = 5
        client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', "interval_status|OK")
        client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', f"interval_info|Interval set to {INTERVAL.value}")

def run_mqtt(client):
    # Creates a MQTT client. 
    client.on_message = on_message

    # Subscribe to the topic for the device
    client.subscribe("/4jggokgpepnvsb2uv4s40d59ov/device001/cmd")

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

def send_data(client):
    while True:
        if SEND.value:
            # Create random temperature and relative umidity values
            temperature = round(random.uniform(10, 40), 2)
            humidity = round(random.uniform(0, 100), 2)

            # Send random variables via MQTT
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', f"t|{temperature}")
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', f"rh|{humidity}")

        # Waint some amout of time
        time.sleep(INTERVAL.value)


if __name__ == "__main__":
    # Create a process to run the MQTT client
    client
    p = Process(target=run_mqtt, args=(client,))
    p.start()
    
    # Create a process to send the data to the MQTT broker
    p = Process(target=send_data, args=(client,))
    p.start()
    