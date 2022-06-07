/**
 * Load and Display 
 * 
 * Images can be loaded and displayed to the screen at their actual size
 * or any other size. 
 */


ONS_instance ons_leftClick = new ONS_instance();
boolean leftPressing = false;
boolean leftOnSliderKnob = false;

void setup() {
  paths();
  init_Images();
  size(500, 500);  
}

void draw() {
  
  leftPressing = (mousePressed == true && (mouseButton == LEFT));
  ons_leftClick.trigger = leftPressing;
  ons_leftClick.run();
  
  if (ons_leftClick.pulse) {
    if (
      abs(mouseX - sliderKnob.x) < (sliderKnob.w / 2)
      &&
      abs(mouseY - sliderKnob.y) < (sliderKnob.h / 2)
      ) {
      leftOnSliderKnob = true;
    }
  }
  else if (!mousePressed) {
    leftOnSliderKnob = false;
  }    
  
  if (leftOnSliderKnob) {
    sliderKnob.y = mouseY;
    if (sliderKnob.y > SLIDER_MAX_Y) {
      sliderKnob.y = SLIDER_MAX_Y;
    }
    else if (sliderKnob.y < SLIDER_MIN_Y) {
      sliderKnob.y = SLIDER_MIN_Y;
    }
  }
  
  buildScreen();
}

void buildScreen() {
  background(255);
  sliderTrack.place();
  sliderKnob.place();
}
