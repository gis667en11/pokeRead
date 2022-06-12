class Lamp {
    int state_Triggered = 1;
    int state_Running = 2;
    int state_Idle = 3;
    BetterImage im_state0;
    BetterImage im_state1;
    private int state;
    private int startMillis;
    int fadeDuration_ms;
    float xCent, yCent;


    Button (String i_path_imState0, i_path_imState1,
            float i_xCenter, float i_yCenter) 
            {
            xCent = i_xCenter;
            yCent = i_yCenter;
            im_state0 = new BetterImage(i_path_imState0);
            im_state1 = new BetterImage(i_path_imState1);
            state = state_Idle;
            startMillis = currentMillis;
            fadeDuration_ms = 1000;
            }

    void trigger() {
        state = state_Triggered;
    }

    void trigger(int i_fadeDuration) {
        fadeDuration_ms = i_fadeDuration;
        trigger();
    }

    void run() {
        if (!firstScan) {
            if (state == state_Triggered) {
                startMillis = currentMillis;
                state = state_Active;
            }
            if (state == state_Active) {
                if (currentMillis - startMillis > fadeDuration_ms) {
                    state = state_Idle;
                }
                im_state1.place(CENTER,xCent,yCent);
            }
            if (state == state_Idle) {
                im_state0.place(CENTER,xCent,yCent);
            }
        }
    }
}