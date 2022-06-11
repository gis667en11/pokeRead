JSONObject json;
import processing.net.*; 

Boolean firstScan = true;
BetterImage pika;
Client myClient; 
String raw;
int currentMillis, previousMillis = 0;


Slider[] slider = new Slider[5];

int ptr0;
BetterMouse bmouse;

void sendSocketData() {
  JSONObject json = new JSONObject();
  
  JSONArray slidersJSON = new JSONArray();

  for (int i = 0; i < slider.length; i++) {

    JSONObject sliderJSON = new JSONObject();

    sliderJSON.setInt("id", i);
    sliderJSON.setFloat("knobValue", slider[i].knobValue);

    slidersJSON.setJSONObject(i, sliderJSON);
  }
  
  json = new JSONObject();
  json.setJSONArray("sliders", slidersJSON);
  byte[] sendData = json.toString().getBytes();
  
  myClient.write(sendData);
}

void setup() {
  
  myClient = new Client(this, "localhost", 50007); 
  paths();
  bmouse = new BetterMouse();
  
  currentMillis = millis();
  previousMillis = currentMillis;
  
  for(int i = 0 ; i < slider.length; i++){
    slider[i] = new Slider(
      // String paths to image for track and knob
      path_file_sliderTrack_Vert,path_file_eyeKnob,
      // how much of the track can the knob use? 0.0 - 1.0
      0.8,
      // orientation is ORIENT_VERT or _HOR
      ORIENT_VERT,
      // track center position, (x, y)
      100.0 + i * 150.0, 250.0,
      // starting location for knob 0.0 - 1.0
      0.5);
  }
        
  size(800, 650);
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
  
  if (myClient.available() > 0) { 
    raw = myClient.readString();
    println(raw);
    if (raw.equals("dataReq")) {
      vol_sendSocketData = true;
      println("sending data +++++");
    }
  }
  
  if (vol_sendSocketData) {
    sendSocketData();
  }

  if (firstScan) {
    firstScan = false;
  }
}
