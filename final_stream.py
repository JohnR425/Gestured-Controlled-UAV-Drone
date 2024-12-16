import serial
import time
import pandas as pd
import numpy as np
from collections import deque
import pickle
from djitellopy import Tello
import sys

### This script streams in live data and performs classification every second, sending the appropriate movement command based on the classification.

#Change port value based on personal machine settings
PORT = "/dev/tty.usbserial-11130"
ser = serial.Serial(PORT, baudrate=115200)
DATA_LENGTH = 100

lines_buffer = deque(maxlen=DATA_LENGTH)

def stream(model):
    curr_iter = 1
    countdown = 1
    print()
    print("Recording START: ", curr_iter)
    try:
        while True:
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
                if(num_tokens[0] == "acce" and num_tokens[4] == "gyro"):
                    lines_buffer.append(curr_line)

            #When the current recording window has ended, classify the gesture with the data collected
            if len(lines_buffer) == DATA_LENGTH:
                with open("output.txt", "w") as f:
                    f.write("".join(lines_buffer))
                features = []
                column_headings = ['acce_x', 'acce_y', 'acce_z', 'gyro_x', 'gyro_y', 'gyro_z']
                df = pd.read_csv("output.txt", header = None, delimiter = " ") 
                df.columns = column_headings
                df.to_csv("output.csv", index = None)
                df = pd.read_csv("output.csv")

                # Keep only accelerometer and gyroscope signals
                data = df[['acce_x', 'acce_y', 'acce_z', 'gyro_x', 'gyro_y', 'gyro_z']].values.astype(np.float32)

                # Normalize data
                epsilon = 0.000000001
                data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0) + epsilon) 

                # Populate lists with normalized data and labels
                features.append(data.flatten())

                X = np.array(features)
                X = np.nan_to_num(X, nan=0)
                label = model.predict(X)[0]
                direction = ''
                if label == 0:
                    direction = 'neutral'
                    print("Prediction: " + direction)
                elif label == 1:
                    direction = 'up'
                    print("Prediction: " + direction)
                    tello.move_up(100)
                    while (countdown < 4):
                        print(countdown)
                        time.sleep(1)
                        countdown += 1
                elif label == 2:
                    direction = 'down'
                    tello.move_down(100)
                    print("Prediction: " + direction)
                    while (countdown < 4):
                        print(countdown)
                        time.sleep(1)
                        countdown += 1
                elif label == 3:
                    direction = 'left'
                    tello.move_left(100)
                    print("Prediction: " + direction)
                    while (countdown < 4):
                        print(countdown)
                        time.sleep(1)
                        countdown += 1
                elif label == 4:
                    direction = 'right'
                    tello.move_right(100)
                    print("Prediction: " + direction)
                    while (countdown < 4):
                        print(countdown)
                        time.sleep(1)
                        countdown += 1
                elif label == 5:
                    direction = 'forwards'
                    tello.move_forward(100)
                    print("Prediction: " + direction)
                    while (countdown < 4):
                        print(countdown)
                        time.sleep(1)
                        countdown += 1
                elif label == 6:
                    direction = 'backwards'
                    tello.move_back(100)
                    print("Prediction: " + direction)
                    while (countdown < 4):
                        print(countdown)
                        time.sleep(1)
                        countdown += 1
                elif label == 7:
                    direction = 'flip'
                    tello.flip_back()
                    print("Prediction: " + direction)
                    while (countdown < 4):
                        print(countdown)
                        time.sleep(1)
                        countdown += 1
                elif label == 8:
                    direction = 'land'
                    print("Prediction: " + direction)
                    tello.land()
                    sys.exit()


                #Clear buffer in preparation for next recording window
                lines_buffer.clear()
                curr_iter += 1
                print()
                print("Recording START: ", curr_iter)
                countdown = 1
    except KeyboardInterrupt:
        print("Stream Interrupted")
    finally:
        # Close the serial connection on exit
        ser.close()

if __name__ == "__main__":
    #Loading model
    with open("model.pkl", "rb") as f:  # 'rb' mode means read binary
        loaded_model = pickle.load(f)
    #Begin streaming data
    tello = Tello()

    tello.connect()
    print(tello.get_battery())
    tello.takeoff()

    #time.sleep(1)

    stream(loaded_model)
    ser.close()