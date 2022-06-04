'''
This program searches for sequentially named images in

path.uniqueDialogue
and
path.screenshotFull

If an image, by number, is missing from either, they are both deleted.
If a gap in numbering is determined, subsequent image pairs are renamed to fill the gap.

'''

import os
import sys
import path
from PIL import Image

FINAL_IMAGE_INDEX = 1000
FINAL_WIDTH = 554
FINAL_HEIGHT = 525

def crop_image(input_image, start_x, start_y, width, height):
    """Pass input name image, output name image, x coordinate to start croping, y coordinate to start croping, width to crop, height to crop """
    box = (start_x, start_y, start_x + width, start_y + height)
    return input_image.crop(box)

def textBlock_exists(index):

    fileName = str(index) + ".png"
    path_file = os.path.join(path.uniqueDialog,fileName)
    return os.path.exists(path_file)

indexImage = 0

if __name__ == "__main__":

    while indexImage < FINAL_IMAGE_INDEX:

        tb_ex = textBlock_exists(indexImage)

        # If both images exist, we have a good matching pair
        if tb_ex:

            fileName_old = str(indexImage) + ".png"
            path_oldFile = os.path.join(path.uniqueDialog,fileName_old)

            imageOld = Image.open(path_oldFile)

            oldImages = []

            # testFileName = [0,0,0]
            # testFileName[0] = str(indexImage) + "_test0.png"
            # testFileName[1] = str(indexImage) + "_test1.png"
            # testFileName[2] = str(indexImage) + "_test2.png"

            for x in range(0,3):
                # testImage = crop_image(imageOld, FINAL_WIDTH * x, 26, FINAL_WIDTH, 175)
                # oldImages.append(testImage)
                # path_testFile = os.path.join(path.tbForHash,testFileName[x])
                # testImage.save(path_testFile,"PNG")

                oldImages.append(crop_image(imageOld, FINAL_WIDTH * x, 26, FINAL_WIDTH, 175))

            new_im = Image.new('RGBA', (FINAL_WIDTH , FINAL_HEIGHT))

            y_offset = 0
            for im in oldImages:
                new_im.paste(im, (0,y_offset))
                y_offset += im.size[1]

            fileName_new = str(indexImage) + "_square.png"
            path_newFile = os.path.join(path.tbForHash,fileName_new)

            new_im.save(path_newFile, "PNG")
            




        
        indexImage += 1
