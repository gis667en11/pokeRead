import os

dir = os.path.dirname(os.path.realpath(__file__))
Border = os.path.join(dir,'borderReference')
processImages = os.path.join(dir,'processImages')
uniqueDialog = os.path.join(dir,'uniqueDialogue')
dialogHashTable = os.path.join(uniqueDialog,'hashTable.csv')
screenshotFull = os.path.join(uniqueDialog,'screenshotFull')
tbRaw = os.path.join(processImages,'image_1_tbRaw.png')
tbTextRaw = os.path.join(processImages,'image_1_tbTextRaw.png')
tbForHash = os.path.join(uniqueDialog,'tbForHash')