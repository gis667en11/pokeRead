
class ONS_instance {
  boolean trigger, memory, pulse;
  void run() {
    if (trigger == true && memory == false) {
      pulse = true;
    } 
    else { 
      pulse = false;
    }
    memory = trigger;
  }
}

class BetterImage {
  int x, y, w, h;
  String path;
  PImage im;
  void load() {
    im = loadImage(path);
    w = im.width;
    h = im.height;
  }
  void place() {
    place(CENTER); 
  }
  void place(int coordinateMode) {
     imageMode(coordinateMode);
     image(im, x, y);
  }
}

// Image instances
BetterImage sliderKnob = new BetterImage();
BetterImage sliderTrack = new BetterImage();

String path_dir;
String path_data;
String path_background;
String path_file_sliderKnob;
String path_file_sliderTrack;

void paths() {
  path_dir = sketchPath() + "\\";
  path_data = path_dir + "data\\";
  path_file_sliderKnob = path_data + "sliderKnob.bmp";
  path_file_sliderTrack = path_data + "sliderTrack.bmp";
}

void init_Images() {
  sliderKnob.path = path_file_sliderKnob;
  sliderKnob.load();
  sliderKnob.x = SLIDER_CENTER_X;
  sliderKnob.y = SLIDER_CENTER_Y;
  
  sliderTrack.path = path_file_sliderTrack;
  sliderTrack.load();
  sliderTrack.x = SLIDER_CENTER_X;
  sliderTrack.y = SLIDER_CENTER_Y;
}
