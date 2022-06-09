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

class ONS_instance {
  boolean trigger, memory, pulse = false;
  Boolean run() {
    if (trigger == true && memory == false) {
      pulse = true;
    } 
    else { 
      pulse = false;
    }
    memory = trigger;
    return pulse;
  }
  Boolean run(Boolean i_trigger) {
    trigger = i_trigger;
    return run();
  }
}

class BetterImage {
  float x0, y0, x1, y1, xCenter, yCenter = 0.0;
  int w, h = 0;
  PImage im;
  BetterImage(String path) {
    im = loadImage(path);
    w = im.width;
    h = im.height;
  }

  void place(int coordinateMode, float i_x0, float i_y0, float i_x1, float i_y1) {

    if (coordinateMode != CORNERS) {
      print("(x,y) (x1,y1) mode requires coordinateMode CORNERS");
      return;
    }
    imageMode(coordinateMode);

    image(im, i_x0, i_y0, i_x1, i_y1);
    xCenter = (i_x1 - i_x0) / 2;
    yCenter = (i_y1 - i_y0) / 2;
    x0 = i_x0;
    y0 = i_y0;
    x1 = i_x1;
    y1 = i_y1;
    w = int(x1 - x0);
    h = int(y1 - y0);
  }

  void place(int coordinateMode, float i_x, float i_y) {

    if (coordinateMode == CORNERS) {
      print("(x,y) mode requires coordinateMode CENTER or CORNER");
      return;
    }
    imageMode(coordinateMode);
    
    if (coordinateMode == CENTER) {
      image(im, i_x, i_y);
      xCenter = i_x;
      yCenter = i_y;
      x0 = i_x - (w / 2);
      y0 = i_y - (h / 2);
      x1 = i_x + (w / 2);
      y1 = i_y + (h / 2);
    }
    if (coordinateMode == CORNER) {
      image(im, i_x, i_y);
      xCenter = i_x + (w / 2);
      yCenter = i_y + (h / 2);
      x0 = i_x;
      y0 = i_y;
      x1 = i_x + w;
      y1 = i_y + h;
    }
  }
}

float clamp_f(float input, float limit_low, float limit_high) {
  if (input > limit_high) {
    input = limit_high;
  }
  else if (input < limit_low) {
    input = limit_low;
  }
  return input;
}

Boolean ORIENT_HOR = true;
boolean ORIENT_VERT = false;

class Slider {
  BetterImage track;
  BetterImage knob;
  float knobPixelRangeScalar; // 0.0 to 1.0
  Boolean orientation;
  Float knobValue;
  Boolean leftOnSliderKnob = false;
  float minKnobPixel, maxKnobPixel;
  float knobPixelRange;

  Slider (String i_path_Track, String i_path_Knob,
          Float i_knobPixelRangeScalar, 
          Boolean i_orientation,
          float i_xCenter, float i_yCenter,
          float i_initKnobScalar) 
            {
              knob = new BetterImage(i_path_Knob);
              track = new BetterImage(i_path_Track);
              knobPixelRangeScalar = clamp_f(i_knobPixelRangeScalar, 0.0, 1.0);
              knobValue = clamp_f(i_initKnobScalar, 0.0, 1.0);
              knob.xCenter = i_xCenter;
              knob.yCenter = i_yCenter;
              track.xCenter = i_xCenter;
              track.yCenter = i_yCenter;
              orientation = i_orientation;
              
              // Set correct xCenter pixel for slider
              // according to init knobValue
              if (orientation == ORIENT_HOR) {
                minKnobPixel = track.xCenter - ( (track.w * knobPixelRangeScalar) / 2.0);
                maxKnobPixel = track.xCenter + ( (track.w * knobPixelRangeScalar) / 2.0);
                knobPixelRange = (maxKnobPixel - minKnobPixel);
                knob.xCenter = knobPixelRange * knobValue + minKnobPixel;
              }
              else {
                minKnobPixel = track.yCenter - ( (track.h * knobPixelRangeScalar) / 2.0);
                maxKnobPixel = track.yCenter + ( (track.h * knobPixelRangeScalar) / 2.0);
                knobPixelRange = (maxKnobPixel - minKnobPixel);
                // y is positive down
                knob.yCenter = maxKnobPixel - knobPixelRange * knobValue;
              }
              
              run();
            }

  
  void run() {
    if (!firstScan) {
      if (bmouse.pulse_leftPressed) {
        if (
          abs(bmouse.x - knob.xCenter) < (knob.w / 2)
          &&
          abs(bmouse.y - knob.yCenter) < (knob.h / 2)
          ) {
          leftOnSliderKnob = true;
        }
      }
      else if (bmouse.pulse_leftReleased) {
        leftOnSliderKnob = false;
      }

      // Drag slider with mouse
      if (leftOnSliderKnob) {
        if (orientation == ORIENT_HOR) {
          knob.xCenter = clamp_f(float(bmouse.x), minKnobPixel, maxKnobPixel);
          knobValue = (knob.xCenter - minKnobPixel) / knobPixelRange;
        }
        else {
          knob.yCenter = clamp_f(float(bmouse.y), minKnobPixel, maxKnobPixel);
          knobValue = 1.0 - (knob.yCenter - minKnobPixel) / knobPixelRange;
        }
        println(knobValue);
      }
    }

    track.place(CENTER, track.xCenter, track.yCenter);
    knob.place(CENTER, knob.xCenter, knob.yCenter);

  }

}

String path_dir;
String path_data;
String path_background;
String path_file_sliderKnob;
String path_file_sliderTrack;

void paths() {
  path_dir = sketchPath() + "\\";
  path_data = path_dir + "data\\";
  path_file_sliderKnob = path_data + "fatPikaKnob.png";
  path_file_sliderTrack = path_data + "sliderTrack.bmp";
}
