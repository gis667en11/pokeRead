class BetterMouse {
  ONS_instance ons_leftPressed;
  ONS_instance ons_leftReleased;
  ONS_instance ons_rightPressed;
  ONS_instance ons_rightReleased;
  ONS_instance ons_centerPressed;
  ONS_instance ons_centerReleased;
  ONS_instance ons_anyPressed;
  Boolean anyPressed,
          leftPressed,
          rightPressed,
          centerPressed,
          pulse_anyPressed,
          pulse_leftPressed, pulse_leftReleased,
          pulse_rightPressed, pulse_rightReleased,
          pulse_centerPressed, pulse_centerReleased = false;
  int x, y, px, py, xChange, yChange = 0;
  BetterMouse() {
    ons_leftPressed = new ONS_instance();
    ons_leftReleased = new ONS_instance();
    ons_rightPressed = new ONS_instance();
    ons_rightReleased = new ONS_instance();
    ons_centerPressed = new ONS_instance();
    ons_centerReleased = new ONS_instance();
    ons_anyPressed = new ONS_instance();
  }
  void run() {
    x = mouseX;
    y = mouseY;
    px = pmouseX;
    py = pmouseY;
    xChange = x - px;
    yChange = y - py;
    leftPressed = (mousePressed == true) && (mouseButton == LEFT);
    rightPressed = (mousePressed == true) && (mouseButton == RIGHT);
    centerPressed = (mousePressed == true) && (mouseButton == CENTER);
    anyPressed = (leftPressed || rightPressed || centerPressed);
    pulse_leftPressed = ons_leftPressed.run(leftPressed);
    pulse_leftReleased = ons_leftReleased.run(!leftPressed);
    pulse_rightPressed = ons_rightPressed.run(rightPressed);
    pulse_rightReleased = ons_rightReleased.run(!rightPressed);
    pulse_centerPressed = ons_centerPressed.run(centerPressed);
    pulse_centerReleased = ons_centerReleased.run(!centerPressed);
    pulse_anyPressed = ons_anyPressed.run(anyPressed);
  }
}