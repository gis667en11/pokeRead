import path
import pyautogui
import imagehash
import pyttsx3
engine = pyttsx3.init()
import os
import csv
from PIL import Image

from pynput import keyboard

def on_activate_8():
    global manualTrigger8
    manualTrigger8 = 1

def on_activate_9():
    global manualTrigger9
    manualTrigger9 = 1

manualTrigger8 = 0
manualTrigger9 = 0

listener = keyboard.GlobalHotKeys({
        '8': on_activate_8,
        '9': on_activate_9})

listener.start()

LIKENESS_THRESHOLD = 30
FINAL_WIDTH = 415
FINAL_HEIGHT = 496

hashTable_from_csv = {}

class textBoxOutline:
    detected = 0
    path_blueTop = 0
    path_greyTop = 0

class fightChatOutline:
    detected = 0
    path_fightTop = 0

tb_Conv = textBoxOutline()
tb_fightChat = fightChatOutline()

tb_Conv.path_blueTop = os.path.join(path.Border,'blue_Top.png')
tb_Conv.path_greyTop = os.path.join(path.Border,'grey_Top.png')
tb_fightChat.path_fightTop = os.path.join(path.Border,'fight_top.png')

firstScan = 1

def crop_image(input_image, start_x, start_y, width, height):
    """Pass input name image, output name image, x coordinate to start croping, y coordinate to start croping, width to crop, height to crop """
    box = (start_x, start_y, start_x + width, start_y + height)
    return input_image.crop(box)

def detect_tb(tbReference, searchImage):

    side = pyautogui.locate(tbReference.path_blueTop, searchImage, grayscale=False)

    if not isinstance(side, type(None)):
        tbReference.detected = 1
    else:
        side = pyautogui.locate(tbReference.path_greyTop, searchImage, grayscale=False)
        if not isinstance(side, type(None)):
            tbReference.detected = 1
        else:
            tbReference.detected = 0

def detect_fightChat(fightChatObject, searchImage):

    side = pyautogui.locate(fightChatObject.path_fightTop, searchImage, grayscale=False)

    if not isinstance(side, type(None)):
        fightChatObject.detected = 1
    else:
        fightChatObject.detected = 0

from PIL import ImageChops

def are_images_equal(img1, img2):
    equal_size = img1.height == img2.height and img1.width == img2.width

    equal_content = not ImageChops.difference(
        img1.convert("RGB"), img2.convert("RGB")
    ).getbbox()

    return equal_size and equal_content

uniqueIndex = []
uniqueHash = []
hashDiffFlat_Count = 0
appendNewHash = 0

# MainProgram
if __name__ == "__main__":    

    # sio.connect('http://localhost:5000')

    # Check for previously written hash table
    if os.path.exists(path.dialogHashTable):
        
        # Open table
        with open(path.dialogHashTable, mode='r') as file_csv:
            reader_obj = csv.reader(file_csv)
            for row in reader_obj:

                if row[1] != "0":
                    uniqueHash.append(imagehash.hex_to_hash(row[1]))
                    uniqueIndex.append(row[0])

    while True:

        # Grab whole screen
        screenshotWhole = pyautogui.screenshot()

        # Take screenshot
        tb_Raw = pyautogui.screenshot(region=(0,740,1920,300))

        detect_tb(tb_Conv, tb_Raw)
        detect_fightChat(tb_fightChat, tb_Raw)

        if tb_Conv.detected or tb_fightChat.detected or manualTrigger8 or manualTrigger9:

            if tb_Conv.detected or manualTrigger8:
                line_x = 128
                line1_y = 816
                line2_y = 909
            if tb_fightChat.detected or manualTrigger9:
                line_x = 80
                line1_y = 822
                line2_y = 922

            oldImages = []
            oldImages.append(crop_image(screenshotWhole, line_x, line1_y, 1660, 62))
            oldImages.append(crop_image(screenshotWhole, line_x, line2_y, 1660, 62))

            newTB = Image.new('RGBA', (1660, 124))

            newTB.paste(oldImages[0], (0,0))
            newTB.paste(oldImages[1], (0,62))

            tbChunks = []
            for x in range(4):
                # testImage = crop_image(imageOld, FINAL_WIDTH * x, 26, FINAL_WIDTH, 175)
                # oldImages.append(testImage)
                # path_testFile = os.path.join(path.tbForHash,testFileName[x])
                # testImage.save(path_testFile,"PNG")

                tbChunks.append(crop_image(newTB, FINAL_WIDTH * x, 0, FINAL_WIDTH, 124))

            tb_Hashy = Image.new('RGBA', (FINAL_WIDTH , FINAL_HEIGHT))

            y_offset = 0
            for im in tbChunks:
                tb_Hashy.paste(im, (0,y_offset))
                y_offset += im.size[1]

            if firstScan:
                prev_hash = imagehash.phash(tb_Hashy, hash_size = 24)
                firstScan = 0

            new_hash = imagehash.dhash(tb_Hashy, hash_size = 24)
            diff = new_hash - prev_hash
            print(str(new_hash)[0:10] + ", " + str(prev_hash)[0:10] + ", diff = " + str(diff))
            prev_hash = new_hash

            if abs(diff) >= LIKENESS_THRESHOLD:
                hashDiffFlat_Count = 0
            else:
                hashDiffFlat_Count += 1

            if hashDiffFlat_Count > 8:
                appendNewHash = 1
            else:
                appendNewHash = 0                

            # Check if any previously saved hash is too similar to this one
            for x in uniqueHash:
                if abs(x - new_hash) < LIKENESS_THRESHOLD + 10:
                    appendNewHash = 0
            
            if appendNewHash or manualTrigger8 or manualTrigger9:
                uniqueHash.append(new_hash)

                newIndex = len(uniqueHash) - 1

                # save screenshot
                fileName = str(newIndex) + ".png"
                fileNameFull = str(newIndex) + "_full.png"
                path_newImage = os.path.join(path.tbForHash,fileName)
                path_newImageFull = os.path.join(path.screenshotFull,fileNameFull)

                tb_Hashy.save(path_newImage)
                screenshotWhole.save(path_newImageFull)

                with open(path.dialogHashTable, 'w') as fp:

                    writeIndex = 0
                    for x in uniqueHash:
                        strvar = str(x)
                        fp.write("%d,%s\n" % (writeIndex, strvar))
                        writeIndex += 1
                
                engine.say('caught')
                engine.runAndWait()
        else:
            hashDiffFlat_Count = 0
            
        if manualTrigger8:
            manualTrigger8 = 0
        
        if manualTrigger9:
            manualTrigger9 = 0
