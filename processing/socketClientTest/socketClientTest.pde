import processing.net.*; 

Client myClient; 
String raw;
int bg_R, bg_G, bg_B;

void setup() { 
  size(200, 200); 
  // Connect to the local machine at port 5204.
  // This example will not run if you haven't
  // previously started a server on this port.
  myClient = new Client(this, "localhost", 50007); 
} 
 
void draw() { 
  if (myClient.available() > 0) { 
    raw = myClient.readString();
    String[] list = split(raw, ',');
    for (int i = 0; i < list.length; i = i + 2) {
      print("( " + list[i] + ", " + list[i+1] + " ) ");
    }
    println();
    myClient.write("received");
    
    // Parse into RGB integer tripplet or w/e it's called
    
    for (int i = 0; i < list.length; i = i + 2) {
      switch(list[i]) {
        case "r":
          try {
            bg_R = Integer.parseInt(list[i+1]);
          } 
          catch (NumberFormatException e) {
            bg_R = -1;
          }
        case "g":
          try {
            bg_G = Integer.parseInt(list[i+1]);
          } 
          catch (NumberFormatException e) {
            bg_G = -1;
          }
        case "b":
          try {
            bg_B = Integer.parseInt(list[i+1]);
          } 
          catch (NumberFormatException e) {
            bg_B = -1;
          }
          
      }
    }
    
    boolean validBGColor = true;
    if (bg_R == -1) validBGColor = false;
    if (bg_G == -1) validBGColor = false;
    if (bg_B == -1) validBGColor = false;
    if (validBGColor) {
      background(bg_R, bg_G, bg_B);
    }
    
  } 
} 
