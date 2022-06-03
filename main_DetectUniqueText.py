
import pyautogui
import imagehash
import pyttsx3
engine = pyttsx3.init()
import os
import csv

# Get the directory for this program
path_dir = os.path.dirname(os.path.realpath(__file__))
path_Border = os.path.join(path_dir,'borderReference')
path_processImages = os.path.join(path_dir,'processImages')
path_uniqueDialog = os.path.join(path_dir,'uniqueDialogue')
path_dialogHashTable = os.path.join(path_uniqueDialog,'hashTable.csv')

hashTable_from_csv = {}

class textBoxOutline:
    present_All = 0
    present_Any = 0
    obstructed = 0
    absent = 0
    detected = 0
    path_blueTop = 0
    path_blueBottom = 0
    path_blueLeft = 0
    path_blueRight = 0
    path_greyTop = 0
    path_greyBottom = 0
    path_greyLeft = 0
    path_greyRight = 0

tb_Conv = textBoxOutline()

tb_Conv.path_blueTop = os.path.join(path_Border,'blue_Top.png')
tb_Conv.path_blueBottom = os.path.join(path_Border,'blue_Bottom.png')
tb_Conv.path_blueLeft = os.path.join(path_Border,'blue_Left.png')
tb_Conv.path_blueRight = os.path.join(path_Border,'blue_Right.png')
tb_Conv.path_greyTop = os.path.join(path_Border,'grey_Top.png')
tb_Conv.path_greyBottom = os.path.join(path_Border,'grey_Bottom.png')
tb_Conv.path_greyLeft = os.path.join(path_Border,'grey_Left.png')
tb_Conv.path_greyRight = os.path.join(path_Border,'grey_Right.png')

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

    side = pyautogui.locate(tbReference.path_blueTop, searchImage, grayscale=False)

    if not isinstance(side, type(None)):
        tbReference.detected = 1
    else:
        side = pyautogui.locate(tbReference.path_greyTop, searchImage, grayscale=False)
        if not isinstance(side, type(None)):
            tbReference.detected = 1
        else:
            tbReference.detected = 0

uniqueHash = []
hashDiffFlat_Count = 0
appendNewHash = 0

# MainProgram
if __name__ == "__main__":

    # Check for previously written hash table
    if os.path.exists(path_dialogHashTable):
        
        # Open table
        with open(path_dialogHashTable, mode='r') as file_csv:
            reader = csv.reader(file_csv)
            hashTable_from_csv = {rows[0]:rows[1] for rows in reader}

            for x in list(hashTable_from_csv.values()):
                uniqueHash.append(imagehash.hex_to_hash(x))

    while True:

        # Take screenshot
        tb_Raw = pyautogui.screenshot(region=(40,760,1839,260))

        detect_tb(tb_Conv, tb_Raw)

        if tb_Conv.detected:
            tb_textRaw = crop_image(tb_Raw, 88, 18, 1663, 224)

            if firstScan:
                prev_hash = imagehash.dhash(tb_textRaw, hash_size = 16)
                firstScan = 0

            new_hash = imagehash.dhash(tb_textRaw, hash_size = 16)
            diff = new_hash - prev_hash
            print(str(new_hash) + ", " + str(prev_hash) + ", diff = " + str(diff))
            prev_hash = new_hash

            if abs(diff) >= 15:
                hashDiffFlat_Count = 0
            else:
                hashDiffFlat_Count += 1

            if hashDiffFlat_Count > 8:
                appendNewHash = 1
            else:
                appendNewHash = 0                

            for x in uniqueHash:
                if abs(x - new_hash) < 15:
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
            
