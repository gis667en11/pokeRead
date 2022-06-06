
import pokepath
import pokeconstants
import os
from PIL import Image
import pyautogui
from PIL import ImageChops

def crop_image(input_image, start_x, start_y, width, height):
    box = (start_x, start_y, start_x + width, start_y + height)
    return input_image.crop(box)

def are_images_equal(img1, img2):
    equal_size = img1.height == img2.height and img1.width == img2.width

    equal_content = not ImageChops.difference(
        img1.convert("RGB"), img2.convert("RGB")
    ).getbbox()

    return equal_size and equal_content

def detect_InImage(i_path, searchImage, confidenceValue = 1):
    searchResult = pyautogui.locate(i_path, searchImage, grayscale=False, confidence = confidenceValue)
    if not isinstance(searchResult, type(None)):
        return 1, searchResult
    else:
        return 0, 0

def detect_blueTB(searchImage):
    imref = Image.open(pokepath.file_blueTop)
    imsample = crop_image(searchImage, 200, pokeconstants.TB_CON_PIXEL_Y_DARK, 256, 4)
    return are_images_equal(imref,imsample)

def detect_greyTB(searchImage):
    imref = Image.open(pokepath.file_greyTop)
    imsample = crop_image(searchImage, 200, pokeconstants.TB_CON_PIXEL_Y_DARK, 256, 4)
    return are_images_equal(imref,imsample)

def detect_fightTB(searchImage):
    imref = Image.open(pokepath.file_fightTop)
    imsample = crop_image(searchImage, 200, pokeconstants.TB_FIGHT_PIXEL_Y_DARK, 256, 4)
    return are_images_equal(imref,imsample)

'''
Searches for red arrow within image
Deletes if found
Returns cleansed image regardless
'''
def delete_redArrow(image):

    redArrow = pyautogui.locate(pokepath.file_redArrow_refWhite, image, grayscale=False, confidence = pokeconstants.RED_ARROW_SEARCH_CONFIDENCE)

    if not isinstance(redArrow, type(None)):
        eraseRedArrow = Image.open(pokepath.file_redArrow_eraseWhite)
        image.paste(eraseRedArrow, (redArrow[0],redArrow[1]))
        return image
    
    redArrow = pyautogui.locate(pokepath.file_redArrow_refBlue, image, grayscale=False, confidence = 0.9)

    if not isinstance(redArrow, type(None)):
        eraseRedArrow = Image.open(pokepath.file_redArrow_eraseBlue)
        image.paste(eraseRedArrow, (redArrow[0],redArrow[1]))
        return image

    return image

def getSquareTB(i_image, manual_Conv = 0, manual_Fight = 0):

    # First remove red arrow if present
    other_image = delete_redArrow(i_image)

    # Detect which type of TB
    blueTB = detect_blueTB(other_image)
    greyTB = detect_greyTB(other_image)
    fightTB = detect_fightTB(other_image)

    print(f'TBs detected: Blue: {int(blueTB)}, Grey: {int(greyTB)}, Fight: {int(fightTB)}')

    # Set crop coordinates for two lines
    # of text depending on TB type
    if blueTB or greyTB or manual_Conv:
        line_x = 128
        line1_y = 816
        line2_y = 909
    if fightTB or manual_Fight:
        line_x = 80
        line1_y = 822
        line2_y = 922

    # Get two lines of text from source image
    tbLines = []
    tbLines.append(crop_image(i_image, line_x, line1_y, 1660, 62))
    tbLines.append(crop_image(i_image, line_x, line2_y, 1660, 62))

    #Create stripped down, information dense image
    tbStripped = Image.new('RGBA', (1660, 124))
    tbStripped.paste(tbLines[0], (0,0))
    tbStripped.paste(tbLines[1], (0,62))

    # Break stripped TB image into four parts
    tbChunks = []
    for x in range(4):
        tbChunks.append(
            crop_image(
                tbStripped, 
                pokeconstants.SQUAREHASH_WIDTH * x, 0,
                pokeconstants.SQUAREHASH_WIDTH, tbStripped.size[1]
            )
        )

    squareTB = Image.new('RGBA', (pokeconstants.SQUAREHASH_WIDTH , pokeconstants.SQUAREHASH_HEIGHT))

    y_offset = 0
    for im in tbChunks:
        squareTB.paste(im, (0,y_offset))
        y_offset += im.size[1]

    return squareTB