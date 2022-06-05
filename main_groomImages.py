'''
This program searches for sequentially named images in

path.uniqueDialogue
and
path.screenshotFull

If an image, by number, is missing from either, they are both deleted.
If a gap in numbering is determined, subsequent image pairs are renamed to fill the gap.

'''

import os
import path

FINAL_IMAGE_INDEX = 1000

def textBlock_exists(index):

    fileName = str(index) + ".png"
    path_file = os.path.join(path.tbForHash,fileName)
    return os.path.exists(path_file)

def screenshotFull_exists(index):
    
    fileName = str(index) + "_full.png"
    path_file = os.path.join(path.screenshotFull,fileName)
    return os.path.exists(path_file)

def deleteIm(index):

    fileName = str(index) + ".png"
    path_file = os.path.join(path.tbForHash,fileName)
    if os.path.exists(path_file):
        os.remove(path_file)

    fileName = str(index) + "_full.png"
    path_file = os.path.join(path.screenshotFull,fileName)
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
        
            fileName_old = str(x) + ".png"
            path_oldFile = os.path.join(path.tbForHash,fileName_old)

            fileName_new = str(indexImage) + ".png"
            path_newFile = os.path.join(path.tbForHash,fileName_new)

            os.rename(path_oldFile,path_newFile)

            fileName_old = str(x) + "_full.png"
            path_oldFile = os.path.join(path.screenshotFull,fileName_old)

            fileName_new = str(indexImage) + "_full.png"
            path_newFile = os.path.join(path.screenshotFull,fileName_new)

            os.rename(path_oldFile,path_newFile)

        indexImage += 1
