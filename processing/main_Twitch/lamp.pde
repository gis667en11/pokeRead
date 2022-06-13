//import functions

//class Lamp {
//    int state_Triggered = 1;
//    int state_Running = 2;
//    int state_Idle = 3;
//    BetterImage im_icon;
//    BetterImage im_iconGrey;
//    int state;
//    private int startMillis;
//    int fadeDuration_ms;
//    float xCent, yCent;
    

//    Lamp (String i_path_icon,
//            float i_xCenter, float i_yCenter) 
//            {
//            xCent = i_xCenter;
//            yCent = i_yCenter;
//            im_icon = new BetterImage(i_path_imState0);
//            im_iconGrey = new BetterImage(im_icon.im);
//            im_iconGrey.filter(GRAY);
//            state = state_Idle;
//            startMillis = currentMillis;
//            fadeDuration_ms = 1000;
//            }

//    void trigger() {
//        state = state_Triggered;
//    }

//    void trigger(int i_fadeDuration) {
//        fadeDuration_ms = i_fadeDuration;
//        trigger();
//    }

//    void run() {
//        if (!firstScan) {
//            int activeTime = 0;
            
//            if (state == state_Triggered) {
//                startMillis = currentMillis;
//                state = state_Active;
//            }
//            if (state == state_Active) {
//                int activeTime = currentMillis - startMillis;
                
//                if ( activeTime > fadeDuration_ms) {
//                    state = state_Idle;
//                }
//                tint(1.0);
//                im_icon.place(CENTER,xCent,yCent);

//                if ( activeTime < fadeDuration_ms * 0.25 ) {
//                    im_iconGrey.place(CENTER, xCent, yCent);
//                }
//                else {
//                    // Calculate tint gray; opacity for gray
//                    // opacity must reach 1.0 at the end of 
//                    // fade
//                    float m = 1.0 / ( fadeDuration_ms * 0.75 );
//                    // apply linear function to determine opacity from time
//                    float tintGray = clamp_f(m * (activeTime - fadeDuration_ms * 0.25), 0.0, 1.0);
//                    tint(tintGray);
//                    im_iconGrey.place(CENTER, xCent, yCent);
//                }
                
                
//            }
//            if (state == state_Idle) {
//                im_iconGrey.place(CENTER,xCent,yCent);
//            }
//        }
//    }
//}
