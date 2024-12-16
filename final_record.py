import serial
import time
import glob
from enum import Enum
import os

### This script records data for various gestures.

class Gesture(Enum):
    NEUTRAL = "neutral"
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    FORWARDS = "forwards"
    BACKWARDS = "backwards"
    FLIP = "flip"
    LAND = "land"

#Change port value based on personal machine settings
PORT = "/dev/tty.usbserial-11130"
ser = serial.Serial(PORT, baudrate=115200)
#Script will name files with starting_index onwards
#i.e. if starting_index = 4: up_4.txt, up_5.txt, up_6.txt, etc.
STARTING_INDEX = 26
MOVEMENT_DURATION = 1
gesture_names = []
for gesture in Gesture:
    gesture_names.append(gesture.value)

def contains_substrings(string, substrings):
    return any(sub in string for sub in substrings)

def record(movement_duration, gest):
    start = time.time()
    txt_files = glob.glob("*.txt")
    filenum = 1
    #Iterate over all text files and count the number of files currently existing for the given gesture
    for filename in txt_files:
        prefix = filename.split('.')[0]
        #Check if txt file contains a gesture name in its title
        if contains_substrings(prefix, gesture_names):
            file_gesture = filename.split('_')[0]
            #Check if the txt file matches the current gesture
            if file_gesture == gest.value:
                filenum += 1
    
    if filenum <= STARTING_INDEX:
        filenum = STARTING_INDEX

    print()
    print("Recording " + gest.value + " movement for " + str(movement_duration) + " seconds.")

    txt_filename = "./" + gest.value + "_" + str(filenum) + ".txt"
    comb_data = ""
    try:
        while time.time() - start < movement_duration:
            #Each line lists: acce acce_x acce_y acce_z gyro gyro_x gyro_y gyro_z
            #We will extract the data values from the line and save them to our txt file
            line = ser.readline().decode().strip()
            if len(line.split()) >= 8:
                num_tokens = line.split()[-8:]
                curr_line = ""
                if(num_tokens[0] == "acce"):
                    acce = ' '.join(num_tokens[1:4])
                    if acce:
                        curr_line += acce
                if(num_tokens[4] == "gyro"):
                    gyro = ' '.join(num_tokens[5:8])
                    if gyro:
                        curr_line += " " + gyro + "\n"
                comb_data += curr_line
    except KeyboardInterrupt:
        print("Recording Interrupted")
        print()

    with open(txt_filename, "w") as f:
        f.write(comb_data)
        print("Saved as " + txt_filename + " in: " + os.getcwd())
        print()

if __name__ == "__main__":
    #Note: Delete any txt file from an improper recording prior to starting a new recording to avoid filenames from becoming out of order
    os.chdir("data")
    print(os.getcwd())

    # Comment out the line for the desired gesture to be measured.
    # Note: If an error occurs, the file will not be saved, simply redo the recording

    # record(MOVEMENT_DURATION, Gesture.NEUTRAL)
    # record(MOVEMENT_DURATION, Gesture.UP)
    # record(MOVEMENT_DURATION, Gesture.DOWN)
    # record(MOVEMENT_DURATION, Gesture.LEFT)
    # record(MOVEMENT_DURATION, Gesture.RIGHT)
    # record(MOVEMENT_DURATION, Gesture.FORWARDS)
    # record(MOVEMENT_DURATION, Gesture.BACKWARDS)
    # record(MOVEMENT_DURATION, Gesture.FLIP)
    # record(MOVEMENT_DURATION, Gesture.LAND)

    ser.close()