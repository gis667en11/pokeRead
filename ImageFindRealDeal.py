import pyautogui
import pyttsx3
import time
engine = pyttsx3.init()
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

# Global stuff
textChange = 0
prev_textChange = 0
pulse_newText = 0
prev_Str = 0
new_Str = "bloated whale"

class textBoxOutline:
    present_Left = 0
    present_Right = 0
    present_Top = 0
    present_Right = 0
    present_All = 0
    present_Any = 0
    obstructed = 0
    absent = 0
    detected = 0

tb = textBoxOutline()

def clearTextbox(outline):
    outline.present_Left = 0
    outline.present_Right = 0
    outline.present_Top = 0
    outline.present_Bottom = 0
    outline.present_All = 0
    outline.present_Any = 0
    outline.obstructed = 0
    outline.absent = 0
    outline.detected = 0

while True:

    # Initialize text box object
    clearTextbox(tb)

    # Take screenshot
    im1 = pyautogui.screenshot(region=(30,750,1852,288))
    im1.save('C:\\Users\\Family\\Documents\\Python\\processing\\im1_raw.png')    

    ## Detect all sides
    sideCount = 0
    # Left
    side_L = pyautogui.locate('C:\\Users\\Family\\Documents\\Python\\textOutline_Left.png', im1, grayscale=False)
    if not isinstance(side_L, type(None)):
        tb.present_Any = 1
        tb.present_Left = 1
        sideCount += 1
    # Right
    side_R = pyautogui.locate('C:\\Users\\Family\\Documents\\Python\\textOutline_Right.png', im1, grayscale=False)
    if not isinstance(side_R, type(None)):
        tb.present_Any = 1
        tb.present_Right = 1
        sideCount += 1
    # Top
    side_T = pyautogui.locate('C:\\Users\\Family\\Documents\\Python\\textOutline_Top.png', im1, grayscale=False)
    if not isinstance(side_T, type(None)):
        tb.present_Any = 1
        tb.present_Top = 1
        sideCount += 1
    # Bottom
    side_B = pyautogui.locate('C:\\Users\\Family\\Documents\\Python\\textOutline_Bottom.png', im1, grayscale=False)
    if not isinstance(side_B, type(None)):
        tb.present_Any = 1
        tb.present_Bottom = 1
        sideCount += 1

    # Check side presence
    if not tb.present_Any:
        tb.absent = 1
    elif sideCount != 4:
        tb.obstructed = 1
    else:
        tb.detected = 1

    if tb.obstructed:
        #engine.say("Obstructed")
        #engine.runAndWait()
        print("obstructed")
    if tb.absent:
        #engine.say("Absent")
        #engine.runAndWait()
        print("absent")

    # Detect completely new text box
    pulse_newText = 0

    # If the text box is entirely present...
    if tb.detected:
            
        tb.present_Any = 1
        # Extracting the width and height 
        # of the image:
        width, height = im1.size
        
        # Initialize im2
        im2 = im1

        clearedPixels = 0

        # For all pixels
        for i in range(width):
            for j in range(height):
                
                # getting the RGB pixel value.
                r, g, b = im2.getpixel((i, j))

                if r == 208 and g == 208 and b == 200:
                    clearedPixels += 1
                    
                    # setting the pixel value.
                    im2.putpixel((i,j),(248,248,248))
        print("Cleared pixels: ",(clearedPixels))
        im2.save('C:\\Users\\Family\\Documents\\Python\\processing\\im2_shadowErased.png')

        im5 = ImageOps.grayscale(im2)
        im5.save('C:\\Users\\Family\\Documents\\Python\\processing\\im5_greyScale.png')

        # Resize
        im3 = im5.resize((1000, 300), Image.ANTIALIAS)
        im3.save('C:\\Users\\Family\\Documents\\Python\\processing\\im3_resize.png')

        im6 = im3.filter(ImageFilter.SMOOTH_MORE)
        im6.save('C:\\Users\\Family\\Documents\\Python\\processing\\im6_Smoothed.png')

        # Improve image contrast
        enhancer = ImageEnhance.Contrast(im6)

        im4 = enhancer.enhance(7.0)
        im4.save('C:\\Users\\Family\\Documents\\Python\\processing\\im4_contrasted.png')

        new_Str = pytesseract.image_to_string(im4)
        print("processed")

        # Check if the current string is different from previous read
        if new_Str != prev_Str:

            # If they're not the same, the game is still rolling out characters
            textChange = 1
        else:

            # If the text is the same, the game is done printing characters
            textChange = 0

            # If this is the first scan that the text stopped changing, speak it
            if prev_textChange:
                pulse_newText = 1
                
        prev_Str = new_Str
        prev_textChange = textChange
        
    else:
        prev_textChange = 0
        prev_Str = 0

    if pulse_newText:
        index0 = new_Str.find("¥")
        print("yen index: ",index0)
        if not index0 == -1:
            print("yen detected")
            length0 = len(new_Str)
            print("message length: ",length0)
            length0 = index0 - 1
            new_Str = new_Str[:length0]
        
        index0 = new_Str.find("ELLIE")
        
        print(new_Str)
        engine.say(new_Str)
        engine.runAndWait()
        prev_Str = "dookie"
        
    #time.sleep(3)
    
    
