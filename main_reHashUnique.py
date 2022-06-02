
from distutils.command.build_scripts import first_line_re
from enum import unique
from fileinput import filename
from numpy import append
from PIL import Image
import imagehash
import os

# Get the directory for this program
path_dir = os.path.dirname(os.path.realpath(__file__))
path_uniqueDialog = os.path.join(path_dir,'uniqueDialogue')
path_dialogHashTable = os.path.join(path_uniqueDialog,'hashTable.txt')

uniqueHash = []

# MainProgram
if __name__ == "__main__":

    lastImage = 0
    imageIndex = 0
    noImageCount = 0

    # Build uniqueHash list
    while not lastImage:

        fileName = str(imageIndex) + ".png"
        path_newImage = os.path.join(path_uniqueDialog,fileName)

        try:
            image = Image.open(path_newImage)
        except:
            noImageCount += 1
            uniqueHash.append("0") # Pad with zero to keep index matching image name
            if noImageCount > 10:
                lastImage = 1
        else:
            uniqueHash.append(str(imagehash.dhash(image, hash_size = 16)))
        finally:
            imageIndex += 1

    # Write hash table to file
    with open(path_dialogHashTable, 'w') as fp:
        writeIndex = 0
        for x in uniqueHash:
            strvar = str(x)
            fp.write("%d,%s\n" % (writeIndex, strvar))
            writeIndex += 1
    
    print("Done!")