import os
from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import glob

### This script generates figures plotting data in frequency domain and in time domain for a given ID index.

ID = '1'

def generate_raw(direction, data_type, time_arr, x_arr, y_arr, z_arr):
    os.chdir("..")
    os.chdir("figs")
    td_filename = 'raw_' + data_type + '_' + direction + '.png'
    title = data_type + " raw data with " + direction + " movement gesture data."
    N = 100

    plt.figure()
    plt.plot(time_arr, x_arr, label = "x-axis")
    plt.plot(time_arr, y_arr, label = "y-axis")
    plt.plot(time_arr, z_arr, label = "z-axis")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.savefig(td_filename)
    plt.close()
    os.chdir("..")
    os.chdir("data")

def generate_fft(direction, type, x_arr, y_arr, z_arr):
    os.chdir("..")
    os.chdir("figs")
    filename = 'fft_' + direction + '_' + type + '_fig.png'
    title = "FFT of " + type + " data with " + direction + " movement gesture data"
    
    N = 100
    T = 1.0 / 100.0
    x = np.linspace(0.0, N*T, N, endpoint=False)
    xf = fftfreq(N, T)[:N//2]
    yf_x = fft(x_arr)
    yf_y = fft(y_arr)
    yf_z = fft(z_arr)

    plt.figure()
    plt.plot(xf, 2.0/N * np.abs(yf_x[0:N//2]), label = "x-axis")
    plt.plot(xf, 2.0/N * np.abs(yf_y[0:N//2]), label = "y-axis")
    plt.plot(xf, 2.0/N * np.abs(yf_z[0:N//2]), label = "z-axis")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.savefig(filename)
    os.chdir("..")
    os.chdir("data")

if __name__ == "__main__":
    os.chdir("data")
    txt_files = glob.glob("*.txt")
for filename in txt_files:
    if not (filename.split('.')[0] == 'train' or filename.split('.')[0] == 'test'):
        id = filename.split('_')[1].split('.')[0]
        #Iterate over all gesture data for the given id index
        if id == ID:
            with open(filename, 'r') as file:
                time_arr = []
                x_acce_arr = []
                y_acce_arr = []
                z_acce_arr = []
                x_gyro_arr = []
                y_gyro_arr = []
                z_gyro_arr = []

                direction = filename.split('_')[0]
                counter = 0

                for line in file:
                    time_arr.append(0.01 * counter)
                    x_acce_arr.append(float(line.split()[0].strip()))
                    y_acce_arr.append(float(line.split()[1].strip()))
                    z_acce_arr.append(float(line.split()[2].strip()))
                    x_gyro_arr.append(float(line.split()[3].strip()))
                    y_gyro_arr.append(float(line.split()[4].strip()))
                    z_gyro_arr.append(float(line.split()[5].strip()))

                    counter += 1
                
                generate_raw(direction, "acceleration", time_arr, x_acce_arr, y_acce_arr, z_acce_arr)
                generate_fft(direction, "acceleration", x_acce_arr, y_acce_arr, z_acce_arr)
                generate_raw(direction, "gyro", time_arr, x_gyro_arr, y_gyro_arr, z_gyro_arr)
                generate_fft(direction, "gyro", x_gyro_arr, y_gyro_arr, z_gyro_arr)