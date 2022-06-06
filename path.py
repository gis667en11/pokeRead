import os

dir = os.path.dirname(os.path.realpath(__file__))
reference = os.path.join(dir,'Reference')
processImages = os.path.join(dir,'processImages')
uniqueDialog = os.path.join(dir,'uniqueDialogue')
screenshotFull = os.path.join(uniqueDialog,'screenshotFull')
tbForHash = os.path.join(uniqueDialog,'tbForHash')

file_HashTable = os.path.join(uniqueDialog,'hashTable.csv')
file_blueTop = os.path.join(reference,'blue_Top.png')
file_fightTop = os.path.join(reference,'fight_Top.png')
file_greyTop = os.path.join(reference,'grey_Top.png')
file_redArrow_refWhite = os.path.join(reference,'redArrow_refWhite.png')
file_redArrow_refBlue = os.path.join(reference,'redArrow_refBlue.png')
file_redArrow_eraseWhite = os.path.join(reference,'redArrow_eraseWhite.png')
file_redArrow_eraseBlue = os.path.join(reference,'redArrow_eraseBlue.png')