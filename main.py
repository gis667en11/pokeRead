
from distutils.command.build_scripts import first_line_re
import pyautogui
from PIL import Image
import imagehash
import pyttsx3
import os

# Get the directory for this program
path_dir = os.path.dirname(os.path.realpath(__file__))
path_Border = os.path.join(path_dir,'borderReference')
path_processImages = os.path.join(path_dir,'processImages')

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
    path_Top = 0
    path_Bottom = 0
    path_Left = 0
    path_Right = 0

tb_blueConv = textBoxOutline()

tb_blueConv.path_Top = os.path.join(path_Border,'blue_Top')
tb_blueConv.path_Bottom = os.path.join(path_Border,'blue_Bottom')
tb_blueConv.path_Left = os.path.join(path_Border,'blue_Left')
tb_blueConv.path_Right = os.path.join(path_Border,'blue_Right')

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

path_tbRaw = os.path.join(path_processImages,'image_1_tbRaw.png')
path_tbTextRaw = os.path.join(path_processImages,'image_1_tbTextRaw.png')

firstScan = 1

def crop_image(input_image, start_x, start_y, width, height):
    """Pass input name image, output name image, x coordinate to start croping, y coordinate to start croping, width to crop, height to crop """
    input_image
    box = (start_x, start_y, start_x + width, start_y + height)
    return input_image.crop(box)

def mainLoop():
    
    global firstScan
    global prev_hash
    
    # Initialize text box object
    clearTextbox(tb_blueConv)

    # Take screenshot
    tb_Raw = pyautogui.screenshot(region=(40,760,1839,260)) # (region=(1960,760,1839,260))
    #tb_Raw.save(path_tbRaw)

    tb_textRaw = crop_image(tb_Raw, 88, 18, 1663, 224)
    #tb_textRaw.save(path_tbTextRaw)

    if firstScan:
        prev_hash = imagehash.dhash(tb_textRaw)
        firstScan = 0
    new_hash = imagehash.dhash(tb_textRaw)

    diff = new_hash - prev_hash
    print(str(new_hash) + ", " + str(prev_hash) + ", diff = " + str(diff))
    prev_hash = new_hash

# MainProgram
if __name__ == "__main__":

    while True:
        mainLoop()
