
'''
This program calculates the difference between hashes of
every reference image in a range and outputs
as a matrix in CSV
'''

import os
import path
import imagehash
from PIL import Image

FINAL_IMAGE_INDEX = 64

def textBlock_exists(index):

    fileName = str(index) + ".png"
    path_file = os.path.join(path.tbForHash,fileName)
    return os.path.exists(path_file)



if __name__ == "__main__":

    hashDiff = [[-1 for x in range(FINAL_IMAGE_INDEX+1)] for x in range(FINAL_IMAGE_INDEX+1)]

    for x in range(0,FINAL_IMAGE_INDEX+1):

        if textBlock_exists(x):

            fileName = str(x) + ".png"
            path_x = os.path.join(path.tbForHash,fileName)

            im_x = Image.open(path_x)

            for y in range(x,FINAL_IMAGE_INDEX+1):
                
                if textBlock_exists(y):

                    fileName = str(y) + ".png"
                    path_y = os.path.join(path.tbForHash,fileName)

                    im_y = Image.open(path_y)

                    hashDiff[x][y] = imagehash.dhash(im_x, hash_size = 16) - imagehash.dhash(im_y, hash_size = 16)
    
    for x in range(0,FINAL_IMAGE_INDEX+1):

        for y in range(0,FINAL_IMAGE_INDEX+1):

            print(hashDiff[x][y], end=',')
        print("")




