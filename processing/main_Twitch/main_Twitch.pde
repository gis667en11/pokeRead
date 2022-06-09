
BetterMouse bmouse;
Boolean firstScan = true;

Slider slider;
int LEN_slider = 4;

int ptr0;

void setup() {

  paths();

  bmouse = new BetterMouse();
  

  slider = new Slider(
        // String paths to image for track and knob
        path_file_sliderTrack, path_file_sliderKnob,
        // how much of the track can the knob use? 0.0 - 1.0
        0.8,
        // orientation is ORIENT_VERT or _HOR
        ORIENT_VERT,
        // track center position, (x, y)
        50.0, 250.0,
        // starting location for knob 0.0 - 1.0
        0.8);

  size(500, 500);  
}

void draw() {

  background(255);

  // Gives the program a better mouse
  // pulse bits and state of each button
  bmouse.run();
  


  slider.run();

  if (firstScan) {
    firstScan = false;
  }
}
