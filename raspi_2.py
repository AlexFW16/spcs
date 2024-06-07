#!/usr/bin/python

from __future__ import division
from time import sleep
import paho.mqtt.client as mqtt
import logging
import threading
import json
import RPi.GPIO as GPIO

# topics
topic_control = "topic_control_jku_20"
topic_data = "topic_data_jku_20"

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

brokers_out = {"broker1": "tcp://broker.hivemq.com:1883"}
data_out = json.dumps(brokers_out)
data_in = data_out
brokers_in = json.loads(data_in)

ttg = [10, 7, 7, 5]  # red
gd = [15, 10, 20, 20]  # green

# LED setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.IN)

GPIO.output(25, True)
GPIO.output(24, False)


# mqtt connect callback function
def on_connect(client, userdata, flags, rc):
    logger.info('Connected with result code %s', str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_data, qos=0)
    client.subscribe(topic_control, qos=0)


# mqtt message received callback function
def on_message(client, userdata, msg):
    topic = msg.topic
    if topic == topic_control:
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        state_dict = json.loads(m_decode)
        if "state" in state_dict:
            state = state_dict['state']
            threading.Thread(target=handle_leds, args=(state,)).start()


# DEBUG
# print("Data received: " + m_decode)


def publish_light(client):
    light = get_light()
    msg = "{\"light\": \"" + str(light) + "\"}"
    result = client.publish(topic_data, msg)
    print(f"Sent `{msg}` to topic `{topic_data}`")


def publish_data(client):
    try:
        while True:
            publish_light(client)
            sleep(5)
    except (KeyboardInterrupt, SystemExit):
        logger.info("disconnecting...")
        client.disconnect()
        sleep(1)
        logger.info("succesfully disconnected.")


def listen(client):
    client.loop_forever()


# TODO tg/gd useless??? @LEON
# gets as input one of the four states (0, 1, 2,  3)
# and should do the raspi stuff
def handle_leds(state):
    tg = [10, 7, 7, 5]
    gd = [15, 10, 20, 20]
    numeric = int(state)
    if numeric < 4:
        control_leds(ttg[numeric], gd[numeric])
    else:
        logger.info(f"Invalid control signal: {state}")


def control_leds(local_ttg, local_gd):
    sleep(local_ttg)
    GPIO.output(25, False)
    GPIO.output(24, True)
    sleep(local_gd)
    GPIO.output(25, True)
    GPIO.output(24, False)


def get_light():
    curLvl = 1 - GPIO.input(23)
    logger.info(f"Light level measured: {curLvl}")
    return curLvl


# =======================

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
