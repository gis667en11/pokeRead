String path_dir;
String path_data;
String path_background;
String path_file_sliderKnob;
String path_file_pikaKnob;
String path_file_boatKnob;
String path_file_sliderTrack_Vert;
String path_file_sliderTrack_Hor;
String path_file_donutKnob;
String path_file_eyeKnob;
 
void paths() {
  path_dir = sketchPath() + "\\";
  path_data = path_dir + "data\\";
  path_file_sliderKnob = path_data + "sliderKnob.bmp";
  path_file_pikaKnob = path_data + "fatPikaKnob.png";
  path_file_boatKnob = path_data + "sliderBoat.png";
  path_file_sliderTrack_Vert = path_data + "sliderTrack_Vert_long.png";
  path_file_sliderTrack_Hor = path_data + "sliderTrack_Hor_long.png";
  path_file_donutKnob = path_data + "donutKnob.png";
  path_file_eyeKnob = path_data + "eyeKnob.png";
}
