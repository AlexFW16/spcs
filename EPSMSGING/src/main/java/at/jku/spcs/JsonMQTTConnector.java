package at.jku.spcs;

import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import org.json.JSONException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collection;
import java.util.Collections;
import java.util.*;

import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttAsyncClient;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;


abstract public class JsonMQTTConnector {


    final static Logger LOG = LoggerFactory.getLogger(JsonMQTTConnector.class);

    protected boolean connected;
    private String sendTopic;
    protected final int qos = 2;
    protected MqttAsyncClient sampleClient;
    protected String broker;
    protected String clientId;
    protected Collection<String> topics;

    private static boolean buttonPressed = false;

    public JsonMQTTConnector(String topic) {
        this("tcp://broker.hivemq.com:1883", MqttAsyncClient.generateClientId(), Collections.singleton(topic));
    }

    public JsonMQTTConnector(String broker, String clientId, Collection<String> topics) {
        if (topics != null && topics.size() == 1 && sendTopic == null) {
            sendTopic = topics.iterator().next();
        }
        if (clientId == null || sendTopic == null || broker == null || topics == null || broker.isEmpty() || clientId.isEmpty() || sendTopic.isEmpty()) {
            throw new RuntimeException(String.format("invalid configuration broker: %s  clientId: %s  topics: %s ", broker, clientId, topics));
        }
        this.broker = broker;
        this.clientId = clientId;
        this.topics = topics;
        setup();
    }

    private void setup() {
        MemoryPersistence persistence = new MemoryPersistence();
        try {
            sampleClient = new MqttAsyncClient(this.broker, this.clientId, persistence);
            MqttConnectOptions connOpts = new MqttConnectOptions();
            connOpts.setCleanSession(true);
            LOG.info("Connecting to broker: " + broker);

            sampleClient.setCallback(new MqttCallback() {

                public void messageArrived(String topic, MqttMessage message) throws Exception {
                    //LOG.info("message size {}", (message.getPayload().length));
                    LOG.debug("message arrived Topic: {} with Content: {}", topic, message);
                    //here we add what is executed when smth arrives
                    try {
                        HashMap<String, Object> jsonMap = new HashMap<>(Utility.jsonToMap(message.toString()));
                        handleMessage(jsonMap);
                    } catch (JSONException e) {
                        System.out.println("Exception while parsing JSON Message to JSON Object");
                        throw new RuntimeException(e);
                    }
                }

                public void deliveryComplete(IMqttDeliveryToken token) {
                    LOG.trace("deliveryComplete with token {}", token);
                }

                public void connectionLost(Throwable cause) {
                    LOG.error("connection lost", cause);
                }
            });

            sampleClient.connect(connOpts, null, new IMqttActionListener() {

                public void onSuccess(IMqttToken asyncActionToken) {
                    LOG.info("connected to {}", JsonMQTTConnector.this.broker);
                    for (String topic : JsonMQTTConnector.this.topics) {
                        try {
                            sampleClient.subscribe(topic, qos);
                        } catch (MqttException e) {
                            LOG.error("error subscribing to topic", e);
                        }
                    }
                    connected = true;
                }

                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    LOG.error("failed to connect", exception);
                    connected = false;
                }
            });

        } catch (MqttException me) {
            processEx(me);
        }
    }

    protected static void processEx(MqttException me) {
        LOG.error("exception raised (1): reason: {}; msg; {}; ", me.getReasonCode(), me.getMessage());
        LOG.error("exception raised (2): error", me);
    }

    public void sendMessage(String content) throws MqttException {
        if (connected) {
            LOG.debug("Publishing message: {}", content);
            MqttMessage message = new MqttMessage(content.getBytes());
            message.setQos(qos);
            sampleClient.publish(sendTopic, message);
        } else {
            LOG.error("connect first before sending");
        }
    }

    public void close() {
        if (connected) {
            try {
                sampleClient.disconnect();
            } catch (MqttException e) {
                processEx(e);
            }
        } else {
            LOG.error("not connected - cannot disconnect");
        }
    }

    protected abstract void handleMessage(Map<String, Object> msg);
}


