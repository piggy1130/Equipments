import time
import datetime
import csv
import shutil
import sys
import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class DOCUMENT:

    def create_folder (self, base_path, prefix):
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            print(f"Folder created at {base_path}")

        folder_num = 1
        folder_name = f"{prefix}_v{folder_num}" #"data_v1"
        folder_path = os.path.join(base_path, folder_name)

        # check whether folder exists or not
        while os.path.exists(folder_path):
            folder_num += 1
            folder_name = f"{prefix}_v{folder_num}"
            folder_path = os.path.join(base_path, folder_name)

        os.makedirs(folder_path)
        print(f'Created folder: {folder_path}')
        return folder_path

    def create_file (self, folder_path, file_name, file_extension):
        file_num = 1
        # Construct new file path
        new_file_path = os.path.join(folder_path, f"{file_name}{file_num}.{file_extension}")    
        # Check if the file exists, if it does, create new one with an incremented suffix
        while os.path.isfile(new_file_path):
            file_num += 1
            new_file_path = os.path.join(folder_path, f"{file_name}{file_num}.{file_extension}")
        
        # Create a new file
        open(new_file_path, 'a').close()
        print(f'Created file: {new_file_path}')
        return new_file_path

    #write temperature into the file
    def write_to_file(self, filename, voltage, wavelength):
        fileObject = open(filename, "a")
        fileObject.write(str(datetime.datetime.now()))
        fileObject.write('\t')
        fileObject.write(str(voltage))
        fileObject.write('\t')
        fileObject.write(str(wavelength))
        fileObject.write('\n')
        fileObject.flush()

    # save dictionary into file
    def write_dict_to_file (self, file_path, dictionary):
        with open(file_path, 'wb') as f:
            pickle.dump(dictionary, f)
            
    # read dictionary from file
    def read_dict(self, file_path):
        with open(file_path, 'rb') as file:
            my_dict = pickle.load(file)
            return my_dict
            #print(my_dict)
            
    def convert_array_to_frame(self, array):
        frame = np.copy(array)
        return frame
        
        
    def plot_image(self, image_array):
        plt.clf() #clear the current figure
        plt.imshow(image_array) 
        plt.show()

        