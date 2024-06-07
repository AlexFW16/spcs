#!/usr/bin/python

from __future__ import division
import time
import paho.mqtt.client as mqtt
import logging
import threading
import json

# static stuff
topic_control = "topic_control"
topic_data = "topic_data"

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
	client.subscribe(topic_control, qos=0) #TODO do differently?


# mqtt message received callback function
def on_message(client, userdata, msg):
	topic = msg.topic
	print(topic)
	if topic == "topic_control":
	    m_decode = str(msg.payload.decode("utf-8", "ignore"))
	    state_dict = json.loads(m_decode)
	    if "state" in state_dict:
	        print("the current state is" + state_dict['state'])
	        handle_leds(m_decode)
	#DEBUG
	#print("Data received: " + m_decode)
	

def publish_light(client):
    light = get_light();
    msg = "{\"light\": \"" + str(light) + "\"}"
    result = client.publish(topic_data, msg)

    status = 0#result[0, 1] # TODO does not work properly yet
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic_data}`")
    else:
        print(f"Failed sending `{msg}` to topic `{topic_data}`")

def publish_data(client):
    try:
        while True:
            publish_light(client)
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        logger.info("disconnecting...")
        client.disconnect()
        time.sleep(1)
        logger.info("succesfully disconnected.")

def listen(client):
	client.loop_forever()



#TODO
# gets as input one of the four states (0, 1, 2,  3)
# and should do the raspi stuff
def handle_leds(state):
    pass

# to be implemented
def get_light():
    return 99

#=======================

# setup mqtt
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect mqtt
client.connect("broker.hivemq.com", 1883, 60)

listener = threading.Thread(target=listen, args=(client,))
publisher = threading.Thread(target=publish_data, args=(client,))

listener.start()
publisher.start()

# debug stuff
try: 

    i = 0
    while i < 10:
        input()
        publish_data(client)
        time.sleep(1)
        i += 1

except (KeyboardInterrupt, SystemExit):
    logger.info("disconnecting...")
    client.disconnect()
    time.sleep(1)
    logger.info("succesfully disconnected.")


