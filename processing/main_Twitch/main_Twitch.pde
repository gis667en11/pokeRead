
import processing.net.*; 

Boolean firstScan = true;
BetterImage pika;
Client myClient; 
String raw;
int currentMillis, previousMillis = 0;
int captureCount = 0;
Boolean flatHash, tbBlue, tbGrey, tbFight = false;
Boolean vol_sendSocketData = false;

Slider[] slider = new Slider[5];
Button[] button = new Button[5];

int ptr0;
BetterMouse bmouse;

void readSocketData() {
  
  vol_sendSocketData = false;
  
  if (myClient.available() > 0) { 
    raw = myClient.readString();
    print(raw);
    
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
    }
  }
}

void sendSocketData() {
  JSONObject json = new JSONObject();
  
  JSONArray slidersJSON = new JSONArray();

  for (int i = 0; i < slider.length; i++) {

    JSONObject sliderJSON = new JSONObject();

    sliderJSON.setInt("id", i);
    sliderJSON.setFloat("knobValue", slider[i].knobValue);

    slidersJSON.setJSONObject(i, sliderJSON);
  }
  
  JSONArray buttonsJSON = new JSONArray();

  for (int i = 0; i < button.length; i++) {

    JSONObject buttonJSON = new JSONObject();

    buttonJSON.setInt("id", i);
    buttonJSON.setInt("pressCount", button[i].pressCount);

    buttonsJSON.setJSONObject(i, buttonJSON);
  }
  
  json = new JSONObject();
  json.setJSONArray("sliders", slidersJSON);
  json.setJSONArray("buttons", buttonsJSON);
  byte[] sendData = json.toString().getBytes();
  
  myClient.write(sendData);
}

void setup() {
  
  myClient = new Client(this, "localhost", 50007); 
  paths();
  bmouse = new BetterMouse();
  
  currentMillis = millis();
  previousMillis = currentMillis;
  
  for(int i = 0 ; i < button.length; i++){
    button[i] = new Button(
      // String paths to image for button
      path_file_eyeKnob,
      // track center position, (x, y)
      100.0 + i * 150.0, 700);
  }

  for(int i = 0 ; i < slider.length; i++){
    slider[i] = new Slider(
      // String paths to image for track and knob
      path_file_sliderTrack_Vert,path_file_sliderKnob,
      // how much of the track can the knob use? 0.0 - 1.0
      0.85,
      // orientation is ORIENT_VERT or _HOR
      ORIENT_VERT,
      // track center position, (x, y)
      100.0 + i * 150.0, 250.0,
      // starting location for knob 0.0 - 1.0
      0.5);
  }
        
  size(800, 800);
}

void draw() {
  
  boolean vol_sendSocketData = false;

  background(127);

  // Gives the program a better mouse
  // pulse bits and state of each button
  bmouse.run();
  
  for (int i = 0; i < slider.length; i++) {
    slider[i].run();
  }
  for (int i = 0; i < button.length; i++) {
    button[i].run();
  }
  
  readSocketData();

  if (vol_sendSocketData) {
    sendSocketData();
  }

  if (firstScan) {
    firstScan = false;
  }
}
