#!/usr/bin/python

from __future__ import division
import time
import paho.mqtt.client as mqtt
import logging
import threading
import json
from sense_hat import SenseHat
from pedestrian_light_counter import Pedestrian_Light_Counter
from sensehat_controller import Sensehat_Controller

# static stuff
topic_data = "topic_data"
topic_control = "topic_control"

plc = Sensehat_Controller()


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
	client.subscribe(topic_data, qos=0) #TODO do differently?
	client.subscribe(topic_control, qos=0)


# mqtt message received callback function
# display stuff
def on_message(client, userdata, msg):
	topic = msg.topic
	m_decode = str(msg.payload.decode("utf-8", "ignore"))
	# Needs to display the time
	print("Data received: " + m_decode)

	if topic == "topic_control":
	    m_decode = str(msg.payload.decode("utf-8", "ignore"))
	    state_dict = json.loads(m_decode)
	    if "state" in state_dict:
	        print("the current state is" + state_dict['state'])
            plc.start_countdown(state_dict['state'])
            plc.start_countdown(state)
	
# our method to publish messages
def publish_humidity(client):
    humidity = get_humidity();
    msg = "{\"humidity\": \"" + str(humidity) + "\"}"
    result = client.publish(topic_data, msg)

    status = 0#result[0, 1] # TODO does not work properly yet
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic_data}`")
    else:
        print(f"Failed sending `{msg}` to topic `{topic_data}`")

def publish_buttonPress(client):
    msg = "{\"pressed\": \"1\"}"
    result = client.publish(topic_control, msg)

    status = 0#result[0, 1] # TODO does not work properly yet
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic_control}`")
    else:
        print(f"Failed sending `{msg}` to topic `{topic_control}`")


# TODO implement
def get_humidity():
    return round(sense.get_humidity(), 2)

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



#=======================

# setup mqtt
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect mqtt
client.connect("broker.hivemq.com", 1883, 60)

#Thread that waits for messages
listener = threading.Thread(target=listen, args=(client,))
publisher = threading.Thread(target=publish_data, args=(client,))

listener.start()
publisher.start()

