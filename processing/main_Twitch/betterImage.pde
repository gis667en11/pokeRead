class BetterImage {
  float x0, y0, x1, y1, xCenter, yCenter = 0.0;
  int w, h = 0;
  PImage im;
  BetterImage(String path) {
    im = loadImage(path);
    w = im.width;
    h = im.height;
  }

  void place(int coordinateMode, float i_x0, float i_y0, float i_x1, float i_y1) {

    if (coordinateMode != CORNERS) {
      print("(x,y) (x1,y1) mode requires coordinateMode CORNERS");
      return;
    }
    imageMode(coordinateMode);

    image(im, i_x0, i_y0, i_x1, i_y1);
    xCenter = (i_x1 - i_x0) / 2;
    yCenter = (i_y1 - i_y0) / 2;
    x0 = i_x0;
    y0 = i_y0;
    x1 = i_x1;
    y1 = i_y1;
    w = int(x1 - x0);
    h = int(y1 - y0);
  }

  void place(int coordinateMode, float i_x, float i_y) {

    if (coordinateMode == CORNERS) {
      print("(x,y) mode requires coordinateMode CENTER or CORNER");
      return;
    }
    imageMode(coordinateMode);
    
    if (coordinateMode == CENTER) {
      image(im, i_x, i_y);
      xCenter = i_x;
      yCenter = i_y;
      x0 = i_x - (w / 2);
      y0 = i_y - (h / 2);
      x1 = i_x + (w / 2);
      y1 = i_y + (h / 2);
    }
    if (coordinateMode == CORNER) {
      image(im, i_x, i_y);
      xCenter = i_x + (w / 2);
      yCenter = i_y + (h / 2);
      x0 = i_x;
      y0 = i_y;
      x1 = i_x + w;
      y1 = i_y + h;
    }
  }
}