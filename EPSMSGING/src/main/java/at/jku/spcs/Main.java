package at.jku.spcs;

import org.eclipse.paho.client.mqttv3.MqttException;

public class Main {

    //topics
    private static final String topic_data = "topic_data_jku_20"; // P1 and P2 send humidity and light data to the calculator
    private static final String topic_control = "topic_control_jku_20"; // P1 sends message to calculator when button is pressed

    public static void main(String[] args) {

        State currentState = new State();

        JsonMQTTConnector dataConnector = new DataConnector(topic_data, currentState);
        JsonMQTTConnector controlConnector = new ControlConnector(topic_control, currentState);

        try {
            // Starting messages, should also work without
            controlConnector.sendMessage("{}");
            dataConnector.sendMessage("{}");

            System.out.println("Started");
        } catch (MqttException e) {
            e.printStackTrace();
            dataConnector.close();
            controlConnector.close();
            System.exit(0);
        }


    }

}
