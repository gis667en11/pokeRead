import path
import constants
import os
from PIL import Image
import pyautogui

'''
Searches for red arrow within image
Deletes if found
Returns cleansed image regardless
'''
def delete_redArrow(image):

    redArrow = pyautogui.locate(path.file_redArrow_refWhite, image, grayscale=False, confidence = constants.RED_ARROW_SEARCH_CONFIDENCE)

    if not isinstance(redArrow, type(None)):
        eraseRedArrow = Image.open(path.file_redArrow_eraseWhite)
        image.paste(eraseRedArrow, (redArrow[0],redArrow[1]))
        return image
    
    redArrow = pyautogui.locate(path.file_redArrow_refBlue, image, grayscale=False, confidence = constants.RED_ARROW_SEARCH_CONFIDENCE)

    if not isinstance(redArrow, type(None)):
        eraseRedArrow = Image.open(path.file_redArrow_eraseBlue)
        image.paste(eraseRedArrow, (redArrow[0],redArrow[1]))
        return image

    return image


def hashFrom_rawScreenshot(image):

    image = delete_redArrow(image)

    