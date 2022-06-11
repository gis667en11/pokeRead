
class Button {
  BetterImage im;
  int pressCount;
  boolean leftOnButton;
  float xCent, yCent;

  Button (String i_path_Image,
          float i_xCenter, float i_yCenter) 
            {
              im = new BetterImage(i_path_Image);
              pressCount = 0;
              leftOnButton = false;
              xCent = i_xCenter;
              yCent = i_yCenter;
              run();
            }

  void run() {
    if (!firstScan) {
      if (bmouse.pulse_leftPressed) {
          if (
              abs(bmouse.x - im.xCenter) < (im.w / 2)
              &&
              abs(bmouse.y - im.yCenter) < (im.h / 2)
              ) {
                  leftOnButton = true;
                  pressCount++;
          }
      }
      else if (bmouse.pulse_leftReleased) {
          leftOnButton = false;
      }
  
      if (leftOnButton) {
          im.place(CENTER, xCent, yCent + 8);
      }
      else {
          im.place(CENTER, xCent, yCent);
      }
    }
  }
  
}
