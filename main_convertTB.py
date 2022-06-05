'''
This program converts a previously created screenshot to a new
hash reference image

'''

import os
import path
from PIL import Image

FINAL_IMAGE_INDEX = 1000
FINAL_WIDTH = 415
FINAL_HEIGHT = 496

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

        if textBlock_exists(indexImage):

            fileName_old = str(indexImage) + "_full.png"
            path_oldFile = os.path.join(path.screenshotFull,fileName_old)

            imageOld = Image.open(path_oldFile)

            oldImages = []

            # testFileName = [0,0,0]
            # testFileName[0] = str(indexImage) + "_test0.png"
            # testFileName[1] = str(indexImage) + "_test1.png"
            # testFileName[2] = str(indexImage) + "_test2.png"

            oldImages.append(crop_image(imageOld, 128, 816, 1660, 62))
            oldImages.append(crop_image(imageOld, 128, 909, 1660, 62))

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

            new_im = Image.new('RGBA', (FINAL_WIDTH , FINAL_HEIGHT))

            y_offset = 0
            for im in tbChunks:
                new_im.paste(im, (0,y_offset))
                y_offset += im.size[1]

            fileName_new = str(indexImage) + ".png"
            path_newFile = os.path.join(path.tbForHash,fileName_new)

            new_im.save(path_newFile, "PNG")
            




        
        indexImage += 1
