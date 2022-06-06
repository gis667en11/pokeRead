
import constants
from PIL import Image
import imagehash
import os
import path
import imageFunctions as imfun

uniqueHash = []

def reHash():

    # delete all previously saved square TB images
    for f in os.listdir(path.tbForHash):
        os.remove(os.path.join(path.tbForHash, f))

    lastImage = 0
    imageIndex = 0
    noImageCount = 0

    # Build uniqueHash list
    while not lastImage:
        
        # For each full screenshot
        fileName_screenshotFull = str(imageIndex) + "_full.png"
        path_file_screenshotFull = os.path.join(path.screenshotFull,fileName_screenshotFull)
        
        # Check if it's there
        try:
            im_screenshotFull = Image.open(path_file_screenshotFull)

        # If it isn't, append a zero to the unique hash table
        except:
            noImageCount += 1
            uniqueHash.append("0") # Pad with zero to keep index matching image name
            if noImageCount > 10:
                lastImage = 1

        # If there is a screenshot, get the squareTB image and process hash
        else:
            squareTB = imfun.getSquareTB(im_screenshotFull)
            uniqueHash.append(imagehash.dhash(squareTB, hash_size = constants.HASH_SIZE))

            # and save the squareTB, why not
            fileName_squareTB = str(imageIndex) + ".png"
            path_file_squareTB = os.path.join(path.tbForHash,fileName_squareTB)
            squareTB.save(path_file_squareTB)

        finally:
            imageIndex += 1

    # Write hash table to file
    with open(path.file_HashTable, 'w') as fp:
        writeIndex = 0
        for x in uniqueHash:
            strvar = str(x)
            fp.write("%d,%s\n" % (writeIndex, strvar))
            writeIndex += 1

    print("Done!")

# MainProgram
if __name__ == "__main__":

    reHash()
    