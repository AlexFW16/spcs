package at.jku.spcs;

import java.util.Map;

public class DataConnector extends JsonMQTTConnector {

    private State currentState;

    public DataConnector(String topic, State currentState) {
        super(topic);
        this.currentState = currentState;
    }

    @Override
    protected void handleMessage(Map<String, Object> msg) {
        System.out.println(msg.get("humidity").toString());
        if (msg.keySet().contains("humidity"))
            currentState.setHumidity(Double.parseDouble(msg.get("humidity").toString()));


        if (msg.keySet().contains("light"))
            currentState.setLight(Integer.parseInt(msg.get("light").toString()));

        System.out.println("current state: " + currentState.get());
    }

}
