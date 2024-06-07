#!/usr/bin/python

from __future__ import division
import time
import paho.mqtt.client as mqtt
import logging
import threading
import json

# static stuff
topic = "topic_control"

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
	client.subscribe(topic, qos=0) #TODO do differently?


# mqtt message received callback function
def on_message(client, userdata, msg):
	topic = msg.topic
	m_decode = str(msg.payload.decode("utf-8", "ignore"))
	handle_message(m_decode)
	#DEBUG
	#print("Data received: " + m_decode)
	
# our method to publish messages
def publish(client):
    msg = "{\"pressed\": \"1\"}"
    result = client.publish(topic, msg)
    status = 0#result[0, 1]
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic}`")
    else:
        print(f"Failed sending `{msg}` to topic `{topic}`")


#TODO
# gets as input one of the four states (0, 1, 2,  3)
# and should do the raspi stuff
def handle_message(mode)

def listen(client):
	client.loop_forever()


#=======================

# setup mqtt
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect mqtt
client.connect("broker.hivemq.com", 1883, 60)

#Thread that waits for messages
listener = threading.Thread(target=listen, args=(client,))
listener.start()
try: 

    i = 0
    while i < 10:
        input()
        publish(client)
        time.sleep(1)
        i += 1

except (KeyboardInterrupt, SystemExit):
    logger.info("disconnecting...")
    client.disconnect()
    time.sleep(1)
    logger.info("succesfully disconnected.")


