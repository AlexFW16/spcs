package at.jku.spcs;

import org.eclipse.paho.client.mqttv3.MqttException;

import java.util.Map;

public class ControlConnector extends JsonMQTTConnector {

    private State currentState;
    private long blocked_time = System.currentTimeMillis();

    public ControlConnector(String topic, State currentState) {
        super(topic);
        this.currentState = currentState;
    }

    protected void handleMessage(Map<String, Object> msg) {
        if (msg.keySet().contains("pressed")) {
            int was_pressed = Integer.parseInt(msg.get("pressed").toString());
            if (was_pressed == 1) {
                //gets the category depending on the current state of weather and light
                int state = currentState.get();
                try {
                    if (System.currentTimeMillis() >= blocked_time) { // button is blocked until it turns off again
                        sendMessage("{\"state\":\"" + state + "\"}");
                        blocked_time = System.currentTimeMillis() + currentState.getDuration() * 1000;
                    }

                } catch (MqttException e) {
                    System.out.println("MQTT Exception during sending the control msg");
                    throw new RuntimeException(e);
                }


            } else System.out.println("Button was not pressed, something went wrong");
        }

    }
}

