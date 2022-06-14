#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Test Import / Export and recording.

recording-test.py loads a WAV file, plays it, recording at the same time until
the end of the track, and then exports the recording as a WAV with "-out"
appended to the file name.

To run the test without input prompts, set valid values for
PATH and INFILE.

User supplied variables
-------
    PATH: Path to the folder containing the input test file. Also used for exporting the result.
    INFILE: Name of the input WAV file.

With a little modification, can be suitable for rinse and repeat with different
input files.

Make sure Audacity is running and that mod-script-pipe is enabled
before running this script.
"""

import os
import sys
import time
import json


# Platform specific file name and file path.
# PATH is the location of files to be imported / exported.

# #PATH = './'
# PATH = ""
# while not os.path.isdir(PATH):
#     PATH = os.path.realpath(input('Path to test folder: '))
#     if not os.path.isdir(PATH):
#         print('Invalid path. Try again.')
# print('Test folder: ' + PATH)


# #INFILE = "testfile.wav"
# INFILE = ""
# while not os.path.isfile(os.path.join(PATH, INFILE)):
#     INFILE = input('Name of input WAV file: ')
#     # Ensure we have the .wav extension.
#     INFILE = os.path.splitext(INFILE)[0] + '.wav'
#     if not os.path.isfile(os.path.join(PATH, INFILE)):
#         print(f"{os.path.join(PATH, INFILE)} not found. Try again.")
#     else:
#         print(f"Input file: {os.path.join(PATH, INFILE)}")
# # Remove file extension.
# INFILE = os.path.splitext(INFILE)[0]


# Platform specific constants
if sys.platform == 'win32':
    print("recording-test.py, running on windows")
    PIPE_TO_AUDACITY = '\\\\.\\pipe\\ToSrvPipe'
    PIPE_FROM_AUDACITY = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    print("recording-test.py, running on linux or mac")
    PIPE_TO_AUDACITY = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    PIPE_FROM_AUDACITY = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'


print("Write to  \"" + PIPE_TO_AUDACITY +"\"")
if not os.path.exists(PIPE_TO_AUDACITY):
    print(""" ..does not exist.
    Ensure Audacity is running with mod-script-pipe.""")
    sys.exit()

print("Read from \"" + PIPE_FROM_AUDACITY +"\"")
if not os.path.exists(PIPE_FROM_AUDACITY):
    print(""" ..does not exist.
    Ensure Audacity is running with mod-script-pipe.""")
    sys.exit()

print("-- Both pipes exist.  Good.")

TOPIPE = open(PIPE_TO_AUDACITY, 'w')
print("-- File to write to has been opened")
FROMPIPE = open(PIPE_FROM_AUDACITY, 'r')
print("-- File to read from has now been opened too\r\n")


def send_command(command):
    """Send a command to Audacity."""
    print("Send: >>> "+command)
    TOPIPE.write(command + EOL)
    TOPIPE.flush()


def get_response():
    """Get response from Audacity."""
    line = FROMPIPE.readline()
    result = ""
    while True:
        result += line
        line = FROMPIPE.readline()
        # print(f"Line read: [{line}]")
        if line == '\n':
            return result


def do_command(command):
    """Do the command. Return the response."""
    send_command(command)
    # time.sleep(0.1) # may be required on slow machines
    response = get_response()
    print("Rcvd: <<< " + response)
    return response

def do_command_async(command):
    """Do the command. Return the response."""
    send_command(command)

def get_response_async():
    """Get response from Audacity."""
    line = FROMPIPE.readline()
    print(line + 'at line consideration')
    result = ""
    if line == "":
        return False
    else:
        while True:
            result += line
            line = FROMPIPE.readline()
            # print(f"Line read: [{line}]")
            if line == '\n':
                return result

def quick_test():
    """Quick test to ensure pipe is working."""
    print(do_command('Record1stChoice'))

if __name__ == '__main__':

    quick_test()
