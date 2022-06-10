
import pokeconstants
import pokepath
import pyautogui
import imagehash
import pyttsx3
engine = pyttsx3.init()
import os
import csv
from PIL import Image
import imageFunctions as imfun
from pynput import keyboard

# Echo server program
import socket
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

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

uniqueHash = []
hashDiffFlat_Count = 0
appendNewHash = 0
im = Image.new('RGBA', (pokeconstants.SQUAREHASH_WIDTH,pokeconstants.SQUAREHASH_HEIGHT))
prev_hash = imagehash.dhash(im, hash_size=pokeconstants.HASH_SIZE)

# MainProgram
if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    s.setblocking(False)
    client = None

    # Check for previously written hash table
    if os.path.exists(pokepath.file_HashTable):

        # Open table
        with open(pokepath.file_HashTable, mode='r') as file_csv:
            reader_obj = csv.reader(file_csv)
            for row in reader_obj:

                if row[1] != "0":
                    uniqueHash.append(imagehash.hex_to_hash(row[1]))
        print(f"hashData uploaded; found {len(uniqueHash)} hashes")
    else:
        print("Hash file not found")

    while True:
        
        if client is None:
            sent = 0
            try:
                client, addr = s.accept()
                print('Connected by', addr)
            except BlockingIOError:
                pass
        else:
            if sent == 0:
                message = 255
                msgString = str("r,200,g,70,b,120") 
                try:
                    client.sendall(msgString.encode('ascii'))
                except BlockingIOError:
                    pass
                else:
                    sent = 1
            try:
                raw = client.recv(1024)
            except:
                pass
            else:
                if raw:
                    rawString = raw.decode('utf-8')
                    splitString = rawString.split(',')
                    print(rawString)

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
            # This function also deletes the red square
            squareTB = imfun.getSquareTB(screenshotWhole)

            # Process hash of square textbox image
            new_hash = imagehash.dhash(squareTB, pokeconstants.HASH_SIZE)
            diff = new_hash - prev_hash
            print(str(new_hash)[0:10] + ", " + str(prev_hash)[0:10] + ", diff = " + str(diff))
            prev_hash = new_hash

            # Monitor when the text box is steady,
            # Meaning new characters are not rolling out
            if diff > pokeconstants.FLATHASH_THRESHOLD:
                hashDiffFlat_Count = 0
            else:
                hashDiffFlat_Count += 1

            if hashDiffFlat_Count > pokeconstants.FLATHASH_COUNTGOAL:
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
                path_file_squareTB = os.path.join(pokepath.tbForHash,fileName_squareTB)
                path_file_screenshotFull = os.path.join(pokepath.screenshotFull,fileName_screenshotFull)

                squareTB.save(path_file_squareTB)
                screenshotWhole.save(path_file_screenshotFull)

                with open(pokepath.file_HashTable, 'w') as fp:

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
