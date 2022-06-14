import processing.net.*;

Boolean firstScan = true;
BetterImage pikaFrame;
Lamp lamp_question, lamp_match, lamp_new, lamp_gray, lamp_blue, lamp_fight;
Client myClient; 
String raw;
int currentMillis = 0;
int captureCount, prevCaptureCount = 0;
Boolean flatHash, tbBlue, tbGrey, tbFight = false;
Boolean vol_sendSocketData = false;
PFont counterFont;
int recordState = 0;
int STATE_RECORDIDLE = 0;
int STATE_RECORDREADY = 1;
int STATE_RECORDING = 2;
int STATE_RECORDINGCOMPLETE = 3;
int STATE_PLAYBACK = 4;
int flasherMillis = 0;

Slider[] slider = new Slider[1];
LampButton[] button = new LampButton[4];

int ptr0;
BetterMouse bmouse;

void readSocketData() {
  
  vol_sendSocketData = false;
  
  if (myClient.available() > 0) { 
    raw = myClient.readString();
    
    JSONObject json = parseJSONObject(raw);
    if (json == null) {
      println("JSONObject could not be parsed");
      flatHash = false;
      tbBlue = false;
      tbGrey = false;
      tbFight = false;
    }
    else {
      vol_sendSocketData = json.getBoolean("dataReq");
      flatHash = json.getBoolean("flatHash");
      captureCount = json.getInt("captureCount");
      tbBlue = json.getBoolean("tbBlue");
      tbGrey = json.getBoolean("tbGrey");
      tbFight = json.getBoolean("tbFight");
      recordState = json.getInt("recordState");
      
      print("dataReq: " + str(vol_sendSocketData) + ", captureCount: " + str(captureCount)
            + ", tbBlue: " + str(tbBlue) + ", tbGrey: " + str(tbGrey) + ", tbFight: " + str(tbFight) + "\n");
    }
  }
}

void sendSocketData() {
  JSONObject json = new JSONObject();
  
  //JSONArray slidersJSON = new JSONArray();

  //for (int i = 0; i < slider.length; i++) {

  //  JSONObject sliderJSON = new JSONObject();

  //  sliderJSON.setInt("id", i);
  //  sliderJSON.setFloat("knobValue", slider[i].knobValue);

  //  slidersJSON.setJSONObject(i, sliderJSON);
  //}
  
  JSONArray buttonsJSON = new JSONArray();

  for (int i = 0; i < button.length; i++) {

    JSONObject buttonJSON = new JSONObject();

    buttonJSON.setInt("id", i);
    buttonJSON.setInt("pressCount", button[i].pressCount);

    buttonsJSON.setJSONObject(i, buttonJSON);
  }
  
  json = new JSONObject();
  //json.setJSONArray("sliders", slidersJSON);
  json.setJSONArray("buttons", buttonsJSON);
  byte[] sendData = json.toString().getBytes();
  
  myClient.write(sendData);
}

void setup() {

  size(1920, 437);
  surface.setTitle("mainTwitchGUI");
  
  counterFont = createFont("Anton-Regular.ttf", 110);
  
  myClient = new Client(this, "localhost", 50007);
  
  paths();
  
  bmouse = new BetterMouse();
  
  pikaFrame = new BetterImage(path_file_pikaFrame);
  pikaFrame.place(CENTER, height / 2, height / 2);
  
  currentMillis = millis();


//  for(int i = 0 ; i < slider.length; i++){
//    slider[i] = new Slider(
//      // String paths to image for track and knob
//      path_file_sliderTrack_Vert,path_file_pikaKnob,
//      // how much of the track can the knob use? 0.0 - 1.0
//      0.85,
//      // orientation is ORIENT_VERT or _HOR
//      ORIENT_VERT,
//      // track center position, (x, y)
//      100.0 + i * 150.0, 250.0,
//      // starting location for knob 0.0 - 1.0
//      0.5);
//  }

  float offset0 = 88;
  
  lamp_gray = new Lamp(
    path_file_iconGrey,
    pikaFrame.w + 105.0, height / 2.0 - offset0
  );
  
  lamp_blue = new Lamp(
    path_file_iconBlue,
    pikaFrame.w + 105.0 + 200 * 1, height / 2.0 - offset0
  );
  
  lamp_fight = new Lamp(
    path_file_iconFight,
    pikaFrame.w + 105.0 + 200 * 2, height / 2.0 - offset0
  );
  
  lamp_question = new Lamp(
    path_file_iconQuestion,
    pikaFrame.w + 205, height / 2.0 + offset0
  );
  
  lamp_match = new Lamp(
    path_file_iconMatch,
    pikaFrame.w + 205.0 + 200 * 1, height / 2.0 + offset0
  );
  
  lamp_new = new Lamp(
    path_file_iconNew,
    pikaFrame.w + 205.0 + 200 * 2, height / 2.0 + offset0
  );
  
  button[0] = new LampButton(
    // String paths to image for button
    path_file_buttonForceUnique,
    // track center position, (x, y)
    1300 , height / 2.0 - offset0);
    
  button[1] = new LampButton(
    // String paths to image for button
    path_file_buttonRecord,
    // track center position, (x, y)
    1400 , height / 2.0 + offset0);
    
  button[2] = new LampButton(
    // String paths to image for button
    path_file_buttonPlay,
    // track center position, (x, y)
    1500 , height / 2.0 - offset0);
    
  button[3] = new LampButton(
    // String paths to image for button
    path_file_buttonSave,
    // track center position, (x, y)
    1600 , height / 2.0 + offset0);

}

void draw() {

  currentMillis = millis();

  background(0xFCD883);
  pikaFrame.place(CENTER, height / 2, height / 2);
  
  textFont(counterFont);
  fill(0);
  textAlign(CENTER,CENTER);
  text(captureCount, pikaFrame.xCenter, pikaFrame.yCenter - 10);
  

  // Gives the program a better mouse
  // pulse bits and state of each button
  bmouse.run();
  
  //for (int i = 0; i < slider.length; i++) {
  //  slider[i].run();
  //}
  for (int i = 0; i < button.length; i++) {
    button[i].run();
  }
  
  readSocketData();

  if (vol_sendSocketData) {
    sendSocketData();
  }
  
  if ( tbBlue != null && tbGrey != null && tbFight != null
        && flatHash != null) {

    if (captureCount != prevCaptureCount && (tbBlue || tbGrey || tbFight)) {
      lamp_new.trigger(1000);
    }
    
    if (captureCount == prevCaptureCount && lamp_new.state != lamp_new.state_Running
        && (tbBlue || tbGrey || tbFight) && flatHash) {
      lamp_match.trigger(50);
    }
    
    if (!flatHash && (tbBlue || tbGrey || tbFight)) {
      lamp_question.trigger(50);
    }
    
    if (tbGrey) {
      lamp_gray.trigger(50);
    }
    if (tbBlue) {
      lamp_blue.trigger(50);
    }
    if (tbFight) {
      lamp_fight.trigger(50);
    }
    
    // Force Unique button behavior
    if ( lamp_match.state != lamp_match.state_Idle && button[0].leftOnButton ) {
      button[0].trigger(1000);
    }
    
    // Flashing buttons
    if ( currentMillis - flasherMillis > 500 ) {
        // Record button
        if ( recordState == STATE_RECORDREADY || recordState == STATE_RECORDINGCOMPLETE) {
          button[1].trigger(250);
        }
        // Play button, Save button
        if (recordState == STATE_RECORDINGCOMPLETE) {
          button[2].trigger(250);
          button[3].trigger(250);
    }
        flasherMillis = currentMillis;
    }
    
    // Record button on steady
    if ( recordState == STATE_RECORDING ) {
        button[1].trigger(250);
    }
    
    // Play button on steady
    if ( recordState == STATE_PLAYBACK ) {
        button[2].trigger(250);
    }   
    
  }

  lamp_gray.run();
  lamp_blue.run();
  lamp_fight.run();
  lamp_question.run();
  lamp_match.run();
  lamp_new.run();

  if (firstScan) {
    firstScan = false;
  }

  prevCaptureCount = captureCount;
}
