#!/usr/bin/python

from __future__ import division
import time
import paho.mqtt.client as mqtt
import logging
import threading
import json
import RPi.GPIO as GPIO


# static stuff
topic_control = "topic_control_jku_20"
topic_data = "topic_data_jku_20"

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")


#TODO our stuff
brokers_out = {"broker1": "tcp://broker.hivemq.com:1883"}	
data_out = json.dumps(brokers_out)
data_in = data_out
brokers_in = json.loads(data_in)

# LED setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT) 
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.IN)
isRed = True
GPIO.output(25, isRed)
GPIO.output(24, not isRed)


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
	    mode_dict = json.loads(m_decode)
	    if "mode" in mode_dict:
	        print("the current mode is" + mode_dict['mode'])
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
def handle_leds(mode):
    if isRed: 
        isRed = False
        if mode == 0: 
           control_leds(10, 15)
        elif mode == 1:
            control_leds(7, 15)
        elif mode == 2: 
            control_leds(7, 20)
        elif mode == 3: 
            control_leds(5, 20)
        else:
            logger.info("Invalid control signal")
        isRed = True
          
def control_leds(ttg, gd): 
    sleep(ttg)
    GPIO.output(25, False)
    GPIO.output(24, True)
    sleep(gd)
    GPIO.output(25, True)
    GPIO.output(24, False)

# to be implemented
def get_light():
    curLvl = 1-GPIO.input(23)
    logger.info(f"Light level measured: {curLvl}")
    return curLvl

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
        publish(client)
        time.sleep(1)
        i += 1

except (KeyboardInterrupt, SystemExit):
    logger.info("disconnecting...")
    client.disconnect()
    GPIO.cleanup()
    time.sleep(1)
    logger.info("succesfully disconnected.")
