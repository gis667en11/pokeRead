
from turtle import done
import pokeFunctions
import pokeconstants
import pokepath
import pyautogui
import pokeFunctions
from functionsTiming import TimerON
import imagehash
import os
import pokeComm
from PIL import Image
import imageFunctions as imfun
from audacityPipe import do_command, do_command_async, get_response_async

uniqueHash = []
hashDiffFlat_Count = 0
appendNewHash = 0
newIndex = 0

# These states are for the audacity recording tools
STATE_RECORDIDLE = 0
STATE_RECORDREADY = 1
STATE_RECORDING = 2
STATE_RECORDINGCOMPLETE = 3
STATE_PLAYBACK = 4

recordDuration = TimerON()
playbackTimeout = TimerON()
waitingForResponse = False

# Initialize prev_hash with trash hash to avoid
# "variable used before defined"
im = Image.new('RGBA', (pokeconstants.SQUAREHASH_WIDTH,pokeconstants.SQUAREHASH_HEIGHT))
prev_hash = imagehash.dhash(im, hash_size=pokeconstants.HASH_SIZE)

# print('AtMain')
# MainProgram
if __name__ == "__main__":


    pokeComm.init_socketServer()

    pokeFunctions.pokeReadHashTable(uniqueHash)

    pokeComm.commHandler.imageCaptureCount = len(uniqueHash)

    # print('AtWhileTrue')
    while True:

        # Grab whole screen
        screenshotWhole = pyautogui.screenshot()

        # Check if text box is on screen
        tbDetected = []
        pokeComm.commHandler.tbDialogue = imfun.detect_blueTB(screenshotWhole)
        pokeComm.commHandler.tbGrey = imfun.detect_greyTB(screenshotWhole)
        pokeComm.commHandler.tbFight = imfun.detect_fightTB(screenshotWhole)
        tbDetected.append(pokeComm.commHandler.tbDialogue)
        tbDetected.append(pokeComm.commHandler.tbGrey)
        tbDetected.append(pokeComm.commHandler.tbFight)

        # print('AtIfTrueIntbDetected')
        # If any textbox is present, we must determine if it's new
        # in order to capture it and it's hash
        if True in tbDetected:

            # Get the square textbox image
            # This function also deletes the red square
            squareTB = imfun.getSquareTB(screenshotWhole)

            # Process hash of square textbox image
            new_hash = imagehash.dhash(squareTB, pokeconstants.HASH_SIZE)
            diff = new_hash - prev_hash
            prev_hash = new_hash

            # Monitor when the text box is steady,
            # Meaning new characters are not rolling out
            if diff > pokeconstants.FLATHASH_THRESHOLD:
                hashDiffFlat_Count = 0
            else:
                hashDiffFlat_Count += 1

            if hashDiffFlat_Count > pokeconstants.FLATHASH_COUNTGOAL:
                pokeComm.commHandler.hashFlat = True
            else:
                pokeComm.commHandler.hashFlat = False 

            # Check if this text was previously recorded
            pokeComm.commHandler.hashMatch = False
            for x in uniqueHash:
                if x == new_hash:
                    pokeComm.commHandler.hashMatch = True                    

            if ((not pokeComm.commHandler.hashMatch or pokeComm.buttons[0].pulse_Pressed) 
                and pokeComm.commHandler.hashFlat):
                
                uniqueHash.append(new_hash)

                newIndex = len(uniqueHash) - 1

                pokeComm.commHandler.imageCaptureCount = len(uniqueHash)

                pokeComm.commHandler.recordState = STATE_RECORDREADY

                # save screenshot
                fileName_squareTB = str(newIndex) + ".png"
                fileName_screenshotFull = str(newIndex) + "_full.png"
                path_file_squareTB = os.path.join(pokepath.tbForHash,fileName_squareTB)
                path_file_screenshotFull = os.path.join(pokepath.screenshotFull,fileName_screenshotFull)

                squareTB.save(path_file_squareTB)
                screenshotWhole.save(path_file_screenshotFull)

                with open(pokepath.file_HashTable, 'w') as fp:

                    writeIndex = 0
                    for x in uniqueHash:
                        strvar = str(x)
                        fp.write("%d,%s\n" % (writeIndex, strvar))
                        writeIndex += 1

        else:
            hashDiffFlat_Count = 0
            pokeComm.commHandler.hashFlat = False
            pokeComm.commHandler.hashMatch = False

# Audacity control

        # print('Made it to record button')
        # Press record button
        if (( pokeComm.commHandler.recordState == STATE_RECORDREADY or pokeComm.commHandler.recordState == STATE_RECORDINGCOMPLETE) 
            and pokeComm.buttons[1].pulse_Pressed):
            do_command('SelectAll')
            do_command('Delete')
            do_command('Record1stChoice')
            pokeComm.commHandler.recordState = STATE_RECORDING
        
        # Stop recording
        elif pokeComm.commHandler.recordState == STATE_RECORDING and pokeComm.buttons[1].pulse_Pressed:
            do_command('Stop')
            do_command('SelectAll')
            do_command('TruncateSilence')
            pokeComm.commHandler.recordState = STATE_RECORDINGCOMPLETE

        # print('After recording')
        recordDuration.run(pokeComm.commHandler.recordState == STATE_RECORDING, 2147483647)

        # print('after record duration TON')
        # Trigger playback
        if pokeComm.commHandler.recordState == STATE_RECORDINGCOMPLETE and pokeComm.buttons[2].pulse_Pressed:
            # print('Before Play')
            playbackTimeout.run(1, recordDuration.accumulated)
            do_command('Play')
            #waitingForResponse = True
            # print('After Play')
            pokeComm.commHandler.recordState = STATE_PLAYBACK

        # Stop playback
        elif (pokeComm.commHandler.recordState == STATE_PLAYBACK and not waitingForResponse and (pokeComm.buttons[2].pulse_Pressed or playbackTimeout.done)):
            do_command('Stop')
            pokeComm.commHandler.recordState = STATE_RECORDINGCOMPLETE

        # # print('before async response')
        # if waitingForResponse:
        #     if get_response_async() != False:
        #         waitingForResponse = False

        playbackTimeout.run(pokeComm.commHandler.recordState == STATE_PLAYBACK, recordDuration.accumulated)

        # Save audio and export
        if pokeComm.commHandler.recordState == STATE_RECORDINGCOMPLETE and pokeComm.buttons[3].pulse_Pressed:
            do_command('SelectAll')
            fileName_audio = pokepath.audio + '/' + str(newIndex) + '.wav'
            do_command('Export2: Filename=' + fileName_audio)
            do_command('SelectAll')
            do_command('Delete')
            pokeComm.commHandler.recordState = STATE_RECORDIDLE

        pokeComm.handle_socketServer()

        # print("test")