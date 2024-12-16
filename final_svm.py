import os
import pickle
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix

### This script trains and evaluates a SVC model by generating accuracy metrics and a confusion matrix.

gesture_names = ["neutral", "up", "down", "left", "right", "forwards", "backwards", "flip", "land"]

# Function to load dataset (Modified from provided example notebook in Canvas)
def load_data(label_df):
    # Empty lists to store features and labels
    features = []
    labels = []
    for _, row in label_df.iterrows():
        filename = row['filename']
        column_headings = ['acce_x', 'acce_y', 'acce_z', 'gyro_x', 'gyro_y', 'gyro_z']
        df = pd.read_csv(filename, header = None, delimiter = " ") 
        df.columns = column_headings
        csv_name = filename.split('.')[0] + ".csv"
        df.to_csv(csv_name, index = None)

        # Read file into pandas dataframe
        df = pd.read_csv(csv_name)

        # Keep only accelerometer and gyroscope signals
        data = df[['acce_x', 'acce_y', 'acce_z', 'gyro_x', 'gyro_y', 'gyro_z']].values.astype(np.float32)

        # Normalize data
        epsilon = 0.000000001
        data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0) + epsilon) 

        direction = filename.split('_')[0]
        label = -1
        if direction == 'neutral':
            label = 0
        elif direction == 'up':
            label = 1
        elif direction == 'down':
            label = 2
        elif direction == 'left':
            label = 3
        elif direction == 'right':
            label = 4
        elif direction == 'forwards':
            label = 5
        elif direction == 'backwards':
            label = 6
        elif direction == 'flip':
            label = 7    
        elif direction == 'land':
            label = 8  
        

        # Populate lists with normalized data and labels
        features.append(data.flatten())
        labels.append(label)
    X = np.array(features)
    X = np.nan_to_num(X, nan=0)

    y = np.array(labels)
    y = np.nan_to_num(y, nan=0)

    return X, y

def train_and_evaluate_svm(X_train, y_train, X_test, y_test):
    # Create the SVM classifier
    svm_classifier = SVC(kernel='rbf')

    # Train the classifier
    svm_classifier.fit(X_train, y_train)

    # Perform prediction on the test set
    y_pred = svm_classifier.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f'SVM accuracy: {accuracy:.3%}')

    # Plot the confusion matrix
    conf_matrix = confusion_matrix(y_true=y_test, y_pred=y_pred)
    fig, ax = plt.subplots(figsize=(9, 9))
    disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=gesture_names)
    disp.plot(cmap="Blues", ax=ax)
    plt.title('train')
    plt.xlabel('pred')
    plt.ylabel('actual')
    plt.xticks(rotation=45, ha='right')
    plt.savefig('confusion_matrix.png')
    print("Confusion matrix saved in: " + os.getcwd())
    plt.close()

    return svm_classifier

if __name__ == "__main__":
    os.chdir("data")
    train_labels = pd.read_csv("train.csv")
    test_labels = pd.read_csv("test.csv")
    X_train, y_train = load_data(train_labels)
    X_test, y_test = load_data(test_labels)

    os.chdir("..")
    # Perform training and testing with SVM
    model = train_and_evaluate_svm(X_train, y_train, X_test, y_test)

    # Save model
    with open('model.pkl','wb') as f:
        pickle.dump(model,f)
    print("Model saved in: " + os.getcwd())

