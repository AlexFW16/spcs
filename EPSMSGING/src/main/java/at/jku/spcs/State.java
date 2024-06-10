package at.jku.spcs;

public class State {

    private static final int HUMIDITY_THRESHOLD = 41;
    //private static final int LIGHT_THRESHOLD = 10;
    private double humidity = 20;
    private int darkness = 0;

    private static final int[] DURATIONS = {0, 25, 17, 27, 25};
    public void setLight(int darkness){
        this.darkness = darkness;
    }
    public void setHumidity(double humidity){
        this.humidity = humidity;
    }

    // returns -1 for wrong values of darkness
    public int get(){
        if (humidity < HUMIDITY_THRESHOLD && darkness == 0) // not rain and not dark
            return 0;
        else if(humidity < HUMIDITY_THRESHOLD && darkness == 1) //not rain and dark
            return 1;
        else if (humidity >= HUMIDITY_THRESHOLD && darkness == 0) //rain and not dark
            return 2;
        else if (humidity >= HUMIDITY_THRESHOLD && darkness == 1) //rain and dark
            return 3;
        else return -1;
    }

    // Returns a duration value of 0 if an error occurred
    public int getDuration(){
        return DURATIONS[get()+1];
    }
}
