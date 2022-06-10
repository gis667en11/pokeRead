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