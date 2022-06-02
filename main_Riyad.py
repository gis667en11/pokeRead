import re
import cv2 
import numpy as np
import pytesseract
from pytesseract import Output
import time
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
plt=matplotlib.pyplot

i=0
for file in os.listdir("pics"):
    tik=time.time()
    # Plot original image
    image = cv2.imread(f"pics/{file}")
    # b,g,r = cv2.split(image)
    # rgb_img = cv2.merge([r,g,b])
    # plt.title('AUREBESH ORIGINAL IMAGE')
    # plt.imsave("heelo.jpeg",rgb_img)
    # print(image)
    
    new_shape=image.shape

    # new_shape=np.shape((image.shape[0],int(image.shape[1]*.2),image.shape[2]))
    # np.eye()
    new_array=np.zeros(image.shape,dtype=np.uint8)[:,0:int(image.shape[1]*.1),:]
    new_array[:]=248
    # print(new_array.shape)

    image=np.concatenate((new_array,image),axis=1)
    # print(image)


    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh=cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((5,5),np.uint8)
    opened=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    blur = cv2.blur(opened,(4,4))
    # canny=cv2.Canny(thresh, 200, 300)
    plt.imsave(f"pics_thres/{file}_thresh.jpeg",blur, cmap='gray')    

    custom_config = r'--oem 3 --psm 6'
    text=pytesseract.image_to_string(blur, config=custom_config).replace("\n"," ").replace("\r"," ")
    print(f"image {file} says \" {text} \"")
    i=i+1
    tok=time.time()
    # print(tok-tik)%