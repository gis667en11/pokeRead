class Lamp {
    int state_Triggered = 1;
    int state_Running = 2;
    int state_Idle = 3;
    BetterImage im_icon;
    BetterImage im_iconGrey;
    int state;
    private int startMillis;
    int fadeDuration_ms;
    float xCent, yCent;
    

    Lamp (String i_path_icon,
            float i_xCenter, float i_yCenter) 
            {
            xCent = i_xCenter;
            yCent = i_yCenter;
            im_icon = new BetterImage(i_path_icon);
            im_iconGrey = new BetterImage(i_path_icon);
            im_iconGrey.im.filter(GRAY);
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
            int activeTime = 0;
            tint(128.0, 128.0);
            im_iconGrey.place(CENTER,xCent,yCent);
            noTint();
            
            if (state == state_Triggered) {
                startMillis = currentMillis;
                state = state_Running;
            }
            if (state == state_Running) {
                activeTime = currentMillis - startMillis;
                
                if ( activeTime > fadeDuration_ms) {
                    state = state_Idle;
                }
               
                if ( activeTime < fadeDuration_ms * 0.75 ) {
                    tint(255,255);
                    im_icon.place(CENTER, xCent, yCent);
                }
                else {
                    // Calculate tint gray; opacity for gray
                    // opacity must reach 1.0 at the end of 
                    // fade
                    float m = -255.0 / ( fadeDuration_ms * 0.25 );
                    // apply linear function to determine opacity from time
                    float tintGray = clamp_f(m * (activeTime - fadeDuration_ms * 0.75) + 255.0, 0.0, 255.0);
                    println(tintGray);
                    tint(255.0, tintGray);
                    im_icon.place(CENTER, xCent, yCent);
                    noTint();
                }
          }
      }
  }
}

class LampButton {
    int state_Triggered = 1;
    int state_Running = 2;
    int state_Idle = 3;
    BetterImage im_icon;
    BetterImage im_iconGrey;
    int state;
    private int startMillis;
    int fadeDuration_ms;
    float xCent, yCent;
    int pressCount;
    boolean leftOnButton;
    

    LampButton (String i_path_icon,
            float i_xCenter, float i_yCenter) 
            {
            xCent = i_xCenter;
            yCent = i_yCenter;
            im_icon = new BetterImage(i_path_icon);
            im_iconGrey = new BetterImage(i_path_icon);
            im_iconGrey.im.filter(GRAY);
            state = state_Idle;
            startMillis = currentMillis;
            fadeDuration_ms = 1000;
            pressCount = 0;
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
          
            if (bmouse.pulse_leftPressed) {
                if (
                    abs(bmouse.x - im_iconGrey.xCenter) < (im_iconGrey.w / 2)
                    &&
                    abs(bmouse.y - im_iconGrey.yCenter) < (im_iconGrey.h / 2)
                    ) {
                        leftOnButton = true;
                        pressCount++;
                }
            }
            else if (bmouse.pulse_leftReleased) {
                leftOnButton = false;
            }
        
            if (leftOnButton) {
                tint(128.0, 128.0);
                im_iconGrey.place(CENTER,xCent,yCent+8);
                noTint();
            }
            else {
                tint(128.0, 128.0);
                im_iconGrey.place(CENTER,xCent,yCent);
                noTint();
            }
      
            int activeTime = 0;

            if (state == state_Triggered) {
                startMillis = currentMillis;
                state = state_Running;
            }
            if (state == state_Running) {
                activeTime = currentMillis - startMillis;
                
                if ( activeTime > fadeDuration_ms) {
                    state = state_Idle;
                }
               
                if ( activeTime < fadeDuration_ms * 0.75 ) {
                    tint(255,255);
                    im_icon.place(CENTER, xCent, yCent);
                }
                else {
                    // Calculate tint gray; opacity for gray
                    // opacity must reach 1.0 at the end of 
                    // fade
                    float m = -255.0 / ( fadeDuration_ms * 0.25 );
                    // apply linear function to determine opacity from time
                    float tintGray = clamp_f(m * (activeTime - fadeDuration_ms * 0.75) + 255.0, 0.0, 255.0);
                    println(tintGray);
                    tint(255.0, tintGray);
                    im_icon.place(CENTER, xCent, yCent);
                    noTint();
                    if (leftOnButton) {
                        tint(255.0, tintGray);
                        im_icon.place(CENTER, xCent, +8);
                        noTint();
                    }
                    else {
                        tint(255.0, tintGray);
                        im_icon.place(CENTER, xCent, yCent);
                        noTint();
                    }
                }
          }
      }
  }
}
