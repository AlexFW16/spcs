#!/usr/bin/python

from __future__ import division
import time
import paho.mqtt.client as mqtt
import logging
import threading
import json
from sense_hat import SenseHat
from sensehat_controller import Sensehat_Controller

# static stuff
topic_data = "topic_data_jku_20"
topic_control = "topic_control_jku_20"

sensehat_controller = Sensehat_Controller()


# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")


#TODO our stuff
brokers_out = {"broker1": "tcp://broker.hivemq.com:1883"}	
data_out = json.dumps(brokers_out)
data_in = data_out
brokers_in = json.loads(data_in)



# mqtt connect callback function
def on_connect(client, userdata, flags, rc):
	logger.info('Connected with result code %s',str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe(topic_data, qos=0) 
	client.subscribe(topic_control, qos=0)


# mqtt message received callback function
# display stuff
def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    # Needs to display the time
    print("Data received: " + m_decode)

    if topic == topic_control:
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        state_dict = json.loads(m_decode)
        if "state" in state_dict:
            state = state_dict['state']
            threading.Thread(target=print_to_display, args=(state,)).start()  # starts a thread for the display
	
# our method to publish messages
def publish_humidity(client):
    humidity = get_humidity()
    msg = "{\"humidity\": \"" + str(humidity) + "\"}"
    result = client.publish(topic_data, msg)
    print(f"Sent `{msg}` to topic `{topic_data}`")

def publish_buttonPress(client):
    msg = "{\"pressed\": \"1\"}"
    result = client.publish(topic_control, msg)
    print(f"Sent `{msg}` to topic `{topic_control}`")


# TODO implement
def get_humidity():
    return round(sensehat_controller.sense.get_humidity(), 2)

#When button is pressed, call publishButtonPress()


def listen(client):
	client.loop_forever()

def publish_data(client):
    try:
        while True:
            publish_humidity(client)
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        logger.info("disconnecting...")
        client.disconnect()
        time.sleep(1)
        logger.info("succesfully disconnected.")


def print_to_display(state):
	sensehat_controller.start_countdown(state)

#=======================

def listen_button(client):
        sensehat_controller.sense.clear()
        while True:
            for event in sensehat_controller.sense.stick.get_events():
                if event.action == "pressed" and event.direction == "middle":
                    publish_buttonPress(client)




# setup mqtt
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect mqtt
client.connect("broker.hivemq.com", 1883, 60)

#Thread that waits for messages
listener = threading.Thread(target=listen, args=(client,))
publisher = threading.Thread(target=publish_data, args=(client,))

button_listener = threading.Thread(target=listen_button, args=(client,))

listener.start()
publisher.start()
button_listener.start()

