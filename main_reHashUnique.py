
from distutils.command.build_scripts import first_line_re
from enum import unique
from fileinput import filename
from numpy import append
import pyautogui
from PIL import Image
import imagehash
import pyttsx3
engine = pyttsx3.init()
import os

# Get the directory for this program
path_dir = os.path.dirname(os.path.realpath(__file__))
path_Border = os.path.join(path_dir,'borderReference')
path_processImages = os.path.join(path_dir,'processImages')
path_uniqueDialog = os.path.join(path_dir,'uniqueDialogue')
path_dialogHashTable = os.path.join(path_uniqueDialog,'hashTable.txt')

class textBoxOutline:
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

tb_blueConv.path_Top = os.path.join(path_Border,'blue_Top.png')
tb_blueConv.path_Bottom = os.path.join(path_Border,'blue_Bottom.png')
tb_blueConv.path_Left = os.path.join(path_Border,'blue_Left.png')
tb_blueConv.path_Right = os.path.join(path_Border,'blue_Right.png')

def clearTextbox(outline):
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

def detect_tb(tbReference, searchImage):
    # Initialize text box object
    clearTextbox(tbReference)

    side = [0,0,0,0]
    sideCount = 0

    side[0] = pyautogui.locate(tbReference.path_Top, searchImage, grayscale=False)
    side[1] = pyautogui.locate(tbReference.path_Bottom, searchImage, grayscale=False)
    side[2] = pyautogui.locate(tbReference.path_Left, searchImage, grayscale=False)
    side[3] = pyautogui.locate(tbReference.path_Right, searchImage, grayscale=False)

    for x in side:
        if not isinstance(x, type(None)):
            tbReference.present_Any = 1
            sideCount += 1

    # Check side presence
    if not tbReference.present_Any:
        tbReference.absent = 1
    elif sideCount != 4:
        tbReference.obstructed = 1
    else:
        tbReference.detected = 1

uniqueHash = []
hashDiffFlat_Count = 0
appendNewHash = 0

# MainProgram
if __name__ == "__main__":


            tb_textRaw = crop_image(tb_Raw, 88, 18, 1663, 224)

            if firstScan:
                prev_hash = imagehash.dhash(tb_textRaw)
                firstScan = 0

            new_hash = imagehash.dhash(tb_textRaw)
            diff = new_hash - prev_hash
            print(str(new_hash) + ", " + str(prev_hash) + ", diff = " + str(diff))
            prev_hash = new_hash

            if abs(diff) >= 4:
                hashDiffFlat_Count = 0
            else:
                hashDiffFlat_Count += 1

            if hashDiffFlat_Count > 4:
                appendNewHash = 1
            else:
                appendNewHash = 0                

            for x in uniqueHash:
                if abs(x - new_hash) < 4:
                    appendNewHash = 0
            
            if appendNewHash:
                uniqueHash.append(new_hash)

                newIndex = len(uniqueHash) - 1

                fileName = str(newIndex) + ".png"

                path_newImage = os.path.join(path_uniqueDialog,fileName)
                tb_textRaw.save(path_newImage)

                with open(path_dialogHashTable, 'w') as fp:

                    writeIndex = 0
                    for x in uniqueHash:
                        strvar = str(x)
                        fp.write("%d,%s\n" % (writeIndex, strvar))
                        writeIndex += 1
                
                engine.say('caught')
                engine.runAndWait()
        else:
            hashDiffFlat_Count = 0
            
