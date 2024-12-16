import os
import glob
import pandas as pd 

### This script partitions the dataset into the training and test datasets by creating corresponding txt and csv files.

gesture_names = ["neutral", "up", "down", "left", "right", "forwards", "backwards", "flip", "land"]
#Number of files per category
#Proportion of data allocated to training dataset
TRAIN_RATIO = 0.8

def contains_substrings(string, substrings):
    return any(sub in string for sub in substrings)

#Function checks if there is the same number of files for each of the gestures
def is_gest_num_consistent():
    txt_files = glob.glob("*.txt")
    gest_numbers = []
    for gest in gesture_names:
        gest_num = 0
        for filename in txt_files:
            prefix = filename.split('.')[0]
            #Check if txt file contains a gesture name in its title
            if contains_substrings(prefix, gesture_names):
                file_gesture = filename.split('_')[0]
                #Check if the txt file matches the current gesture
                if file_gesture == gest:
                    gest_num += 1
        gest_numbers.append(gest_num)
    return len(set(gest_numbers)) == 1

#Function returns the number of files recorded per gesture
def get_gest_num():
    txt_files = glob.glob("*.txt")
    gest_num = 0
    for filename in txt_files:
        prefix = filename.split('.')[0]
        #Check if txt file contains a gesture name in its title
        if contains_substrings(prefix, gesture_names):
            file_gesture = filename.split('_')[0]
            if file_gesture == gesture_names[0]:
                gest_num += 1
    return gest_num
    
        

if __name__ == "__main__":
    os.chdir("data")
    if not is_gest_num_consistent():
        print()
        print("ERROR: Inconsistent number of txt files per gesture")
        print()
        quit()

    #Number of files per category
    gest_num = get_gest_num()

    #Generating txt files which lists the filenames associated with each dataset
    train_txt = 'train.txt'
    with open(train_txt, 'w') as outfile:
        txt_files = glob.glob("*.txt")
        for filename in txt_files:
            prefix = filename.split('.')[0]
            if contains_substrings(prefix, gesture_names):
                id = filename.split('_')[1].split('.')[0]
                with open(filename, 'r') as infile:
                    if int(id) <= int(gest_num * TRAIN_RATIO):
                        outfile.write(filename + "\n")

    test_txt = 'test.txt'
    with open(test_txt, 'w') as outfile:
        txt_files = glob.glob("*.txt")
        for filename in txt_files:
            prefix = filename.split('.')[0]
            if contains_substrings(prefix, gesture_names):
                id = filename.split('_')[1].split('.')[0]
                with open(filename, 'r') as infile:
                    if int(id) > int(gest_num * TRAIN_RATIO):
                        outfile.write(filename + "\n")

    #Converting txt files to csv
    column_headings = ['filename']

    train_df = pd.read_csv("train.txt", header = None, delimiter = " ") 
    train_df.columns = column_headings
    train_df.to_csv('train.csv', index = None)

    test_df = pd.read_csv("test.txt", header = None, delimiter = " ") 
    test_df.columns = column_headings
    test_df.to_csv('test.csv', index = None)