String path_dir;
String path_data;
String path_background;
String path_file_pikaFrame;
String path_file_sliderTrack_Vert;
String path_file_sliderTrack_Hor;

String path_file_buttonForceUnique;
String path_file_buttonRecord;
String path_file_buttonPlay;
String path_file_buttonSave;

String path_file_iconQuestion;
String path_file_iconMatch;
String path_file_iconNew;
String path_file_iconBlue;
String path_file_iconGrey;
String path_file_iconFight;

String path_file_bigHand;

 
void paths() {
  path_dir = sketchPath() + "\\";
  path_data = path_dir + "data\\";
  
  path_file_buttonForceUnique = path_data + "icon_ForceUniqueButton.png";
  path_file_buttonRecord = path_data + "icon_recordButton.png";
  path_file_buttonPlay = path_data + "icon_playButton.png";
  path_file_buttonSave = path_data + "icon_saveButton.png";
  
  path_file_sliderTrack_Vert = path_data + "sliderTrack_Vert_long.png";
  path_file_sliderTrack_Hor = path_data + "sliderTrack_Hor_long.png";
  path_file_pikaFrame = path_data + "pikaFrame.png";
  path_file_iconQuestion = path_data + "icon_Question.png";
  path_file_iconMatch = path_data + "icon_Match.png";
  path_file_iconNew = path_data + "icon_New.png";
  path_file_iconBlue = path_data + "icon_Blue.png";
  path_file_iconGrey = path_data + "icon_Gray.png";
  path_file_iconFight = path_data + "icon_Fight.png";

  path_file_bigHand = path_data + "BigHand.png";
}
