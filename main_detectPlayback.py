
import pokeconstants
import pokepath
import imageFunctions as imfun
import pyautogui
import imagehash
import os
import csv
import winsound
from PIL import Image

hashTable_from_csv = {}
uniqueHash = []
prev_playedHash = -1
flatHash = 0
hashDiffFlat_Count = 0
# Initialize prev_hash with correctly sized value
im = Image.new('RGBA', (pokeconstants.SQUAREHASH_WIDTH,pokeconstants.SQUAREHASH_HEIGHT))
prev_hash = imagehash.dhash(im, hash_size=pokeconstants.HASH_SIZE)

# MainProgram
if __name__ == "__main__":

    print("main started")

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
        print("Hash file not found. This ain't gonna work, buddy. This python program must")
        print("run from a folder that contains /uniqueDialogue/hashTable.csv")

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
                flatHash = 1
            else:
                flatHash = 0 

            if flatHash:
                index0 = 0
                for x in uniqueHash:
                    if (x == new_hash) and index0 != prev_playedHash:
                        prev_playedHash = index0
                        print(f'triggering audio for file {index0}')
                        fileName = str(index0) + ".wav"
                        print("FileName: " + fileName)
                        path_fileName = os.path.join(pokepath.audio,fileName)
                        print("FilePath: " + path_fileName)
                        if os.path.exists(path_fileName):
                            winsound.PlaySound(path_fileName, winsound.SND_ASYNC | winsound.SND_ALIAS )
                    index0 += 1

        else:
            flatHash = 0
            hashDiffFlat_Count = 0
