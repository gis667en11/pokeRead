String path_dir;
String path_data;
String path_background;
String path_file_sliderKnob;
String path_file_pikaKnob;
String path_file_boatKnob;
String path_file_sliderTrack;

void paths() {
  path_dir = sketchPath() + "\\";
  path_data = path_dir + "data\\";
  path_file_sliderKnob = path_data + "sliderKnob.bmp";
  path_file_pikaKnob = path_data + "fatPikaKnob.png";
  path_file_boatKnob = path_data + "sliderBoat.png";
  path_file_sliderTrack = path_data + "sliderTrack.bmp";
}