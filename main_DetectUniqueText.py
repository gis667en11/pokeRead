
import constants
import path
import pyautogui
import imagehash
import pyttsx3
engine = pyttsx3.init()
import os
import csv
from PIL import Image
import imageFunctions as imfun
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

hashTable_from_csv = {}
uniqueIndex = []
uniqueHash = []
hashDiffFlat_Count = 0
appendNewHash = 0
im = Image.new('RGBA', (constants.SQUAREHASH_WIDTH,constants.SQUAREHASH_HEIGHT))
prev_hash = imagehash.dhash(im, hash_size=constants.HASH_SIZE)

# MainProgram
if __name__ == "__main__":    

    # Check for previously written hash table
    if os.path.exists(path.file_HashTable):
        
        # Open table
        with open(path.file_HashTable, mode='r') as file_csv:
            reader_obj = csv.reader(file_csv)
            for row in reader_obj:

                if row[1] != "0":
                    uniqueHash.append(imagehash.hex_to_hash(row[1]))
                    uniqueIndex.append(row[0])
        print(f"hashData uploaded; found {len(uniqueIndex)} hashes")
    else:
        print("Hash file not found")

    while True:

        # Grab whole screen
        screenshotWhole = pyautogui.screenshot()

        # Check if text box is on screen
        tbDetected = []
        tbDetected.append(imfun.detect_blueTB(screenshotWhole))
        tbDetected.append(imfun.detect_greyTB(screenshotWhole))
        tbDetected.append(imfun.detect_fightTB(screenshotWhole))

        # If any textbox is present, we must determine if it's new
        # in order to capture it and it's hash
        if 1 in tbDetected:

            # Get the square textbox image
            squareTB = imfun.getSquareTB(screenshotWhole)

            # Process hash of square textbox image
            new_hash = imagehash.dhash(squareTB, constants.HASH_SIZE)
            diff = new_hash - prev_hash
            print(str(new_hash)[0:10] + ", " + str(prev_hash)[0:10] + ", diff = " + str(diff))
            prev_hash = new_hash

            # Monitor when the text box is steady,
            # Meaning new characters are not rolling out
            if diff > constants.FLATHASH_THRESHOLD:
                hashDiffFlat_Count = 0
            else:
                hashDiffFlat_Count += 1

            if hashDiffFlat_Count > constants.FLATHASH_COUNTGOAL:
                appendNewHash = 1
            else:
                appendNewHash = 0 

            # Check if this text was previously recorded
            for x in uniqueHash:
                if x == new_hash:
                    appendNewHash = 0
            
            if appendNewHash:
                uniqueHash.append(new_hash)

                newIndex = len(uniqueHash) - 1

                # save screenshot
                fileName_squareTB = str(newIndex) + ".png"
                fileName_screenshotFull = str(newIndex) + "_full.png"
                path_file_squareTB = os.path.join(path.tbForHash,fileName_squareTB)
                path_file_screenshotFull = os.path.join(path.screenshotFull,fileName_screenshotFull)

                squareTB.save(path_file_squareTB)
                screenshotWhole.save(path_file_screenshotFull)

                with open(path.file_HashTable, 'w') as fp:

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
