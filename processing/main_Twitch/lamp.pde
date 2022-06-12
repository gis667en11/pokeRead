class Lamp {
    int state_Triggered = 1;
    int state_Running = 2;
    int state_Idle = 3;
    BetterImage im_icon;
    BetterImage im_iconGrey;
    private int state;
    private int startMillis;
    int fadeDuration_ms;
    float xCent, yCent;

    Button (String i_path_icon, float i_lampDiameter,
            float i_xCenter, float i_yCenter) 
            {
            xCent = i_xCenter;
            yCent = i_yCenter;
            im_icon = new BetterImage(i_path_imState0);
            im_iconGrey = new BetterImage(im_icon.im);
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