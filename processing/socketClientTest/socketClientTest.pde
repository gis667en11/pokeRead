import processing.net.*; 

Client myClient; 
int dataIn; 
 
void setup() { 
  size(200, 200); 
  // Connect to the local machine at port 5204.
  // This example will not run if you haven't
  // previously started a server on this port.
  myClient = new Client(this, "localhost", 50007); 
} 
 
void draw() { 
  if (myClient.available() > 0) { 
    dataIn = myClient.read();
    print(dataIn);
  } 
  background(dataIn); 
} 
