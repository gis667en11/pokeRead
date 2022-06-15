'''
This program searches for sequentially named images in

pokepath.uniqueDialogue
and
pokepath.screenshotFull

If an image, by number, is missing from either, they are both deleted.
If a gap in numbering is determined, subsequent image pairs are renamed to fill the gap.

'''

import os
import pokepath

FINAL_IMAGE_INDEX = 1000

def textBlock_exists(index):

    fileName = str(index) + ".png"
    path_file = os.path.join(pokepath.tbForHash,fileName)
    return os.path.exists(path_file)

def screenshotFull_exists(index):
    
    fileName = str(index) + "_full.png"
    path_file = os.path.join(pokepath.screenshotFull,fileName)
    return os.path.exists(path_file)

def deleteIm(index):

    fileName = str(index) + ".png"
    path_file = os.path.join(pokepath.tbForHash,fileName)
    if os.path.exists(path_file):
        os.remove(path_file)

    fileName = str(index) + "_full.png"
    path_file = os.path.join(pokepath.screenshotFull,fileName)
    if os.path.exists(path_file):
        os.remove(path_file)

    fileName = str(index) + ".wav"
    path_file = os.path.join(pokepath.audio,fileName)
    if os.path.exists(path_file):
        os.remove(path_file)

indexImage = 0
validImagePair = []

if __name__ == "__main__":

    while indexImage < FINAL_IMAGE_INDEX:

        tb_ex = textBlock_exists(indexImage)
        sf_ex = screenshotFull_exists(indexImage)

        # If both images exist, we have a good matching pair
        if tb_ex and sf_ex:
            validImagePair.append(indexImage)
        
        else:

            # Or else we either need to delete orphan images
            if tb_ex or sf_ex:
                deleteIm(indexImage)
        
        indexImage += 1
    
    # Rename all existing image files to make them
    # nice and contiguous
    indexImage = 0

    for x in validImagePair:
        
        # If this image pair needs to be renamed
        if x != indexImage:
        
        # textbox hash image move
            fileName_old = str(x) + ".png"
            path_oldFile = os.path.join(pokepath.tbForHash,fileName_old)

            fileName_new = str(indexImage) + ".png"
            path_newFile = os.path.join(pokepath.tbForHash,fileName_new)

            os.rename(path_oldFile,path_newFile)

        # Full screenshot move
            fileName_old = str(x) + "_full.png"
            path_oldFile = os.path.join(pokepath.screenshotFull,fileName_old)

            fileName_new = str(indexImage) + "_full.png"
            path_newFile = os.path.join(pokepath.screenshotFull,fileName_new)

            os.rename(path_oldFile,path_newFile)

        # Audio file move
            fileName = str(x) + ".wav"
            path_oldFile = os.path.join(pokepath.audio,fileName)

            fileName = str(indexImage) + ".wav"
            path_newFile = os.path.join(pokepath.audio,fileName)
            if os.path.exists(path_oldFile):
                os.rename(path_oldFile,path_newFile)



        indexImage += 1

    print('Done!')