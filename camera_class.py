from vimba import *
from typing import Optional
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class CAMERA:
    
    def __init__(self):
        self.cams = None
        self.i = 1
        #self.camera_in_use = 0
    
    def print_camera(cam: Camera):
        print('/// Camera Name   : {}'.format(cam.get_name()))
        print('/// Model Name    : {}'.format(cam.get_model()))
        print('/// Camera ID     : {}'.format(cam.get_id()))
        print('/// Serial Number : {}'.format(cam.get_serial()))
        print('/// Interface ID  : {}\n'.format(cam.get_interface_id()))

    # get camera by ID
    # -> Camera: function returns an instance of the 'Camera' class
    def get_camera(self, camera_id: str) -> Camera:
        with Vimba.get_instance() as vimba:
            try:
                return vimba.get_camera_by_id(camera_id)

            except self.VimbaCameraError:
                self.abort('Failed to access Camera {}. Abort.'.format(camera_id))

    # choose camera from camera list
    def list_choose_cameras(self):
        with Vimba.get_instance() as vimba:
            self.cams = vimba.get_all_cameras()
            for cam in self.cams:
                CAMERA.print_camera(cam)  # Call the static method

        if (len(self.cams)> 1):
            try:
                camera_in_use = input("Enter the number of camera: ")
                return int(camera_in_use)
            except ValueError:
                print("You did not enter a valid number.")
        else:
            return int(0)
               
    def abort(self, reason: str, return_code: int = 1, usage: bool = False):
        print(reason + '\n')
        if usage:
            self.print_usage()
        sys.exit(return_code)
        
    def parse_args(self) -> Optional[str]:
        args = sys.argv[1:]
        argc = len(args)
        print(argc, "***********")
 
        for arg in args:
            if arg in ('/h', '-h'):
                self.print_usage()
                sys.exit(0)

        if argc > 1:
            self.abort(reason="Invalid number of arguments. Abort.", return_code=2, usage=True)

        return None if argc == 0 else args[0]

    def plot_frame(self, frame):
        plt.clf() #clear the current figure
        plt.imshow(frame.as_numpy_ndarray()) 
        plt.show()
  
    def save_image_data(self, frame, image_folder_path):
        # Convert the frame to an image array
        image_array = np.copy(frame.as_numpy_ndarray())

        #Reshape the image array to 2D
        width, height, _ = image_array.shape
        reshaped_array = image_array.reshape(width * height, -1)
        image_array_2D = image_array[:,:,0]
        
        # Save the image array as a file in the folder
        file_name = f'image_{self.i}.csv'
        self.i = self.i + 1
        np.savetxt(f'{image_folder_path}/{file_name}', image_array_2D.astype(int), fmt='%i', delimiter=',')
                
    def single_frame_capture(self, camera_id):
        with Vimba.get_instance(): #ensure vimba API is started
            with self.cams[camera_id] as cam:
                # Aquire single frame synchronously
                frame = cam.get_frame() 
                return frame
                #print(frame)
                #self.plot_frame(frame)
                #self.save_image_data(frame, image_folder_path)

    def multi_frames_capture(self, camera_id, frame_limit, folder_path):
        with Vimba.get_instance(): #ensure vimba API is started
            with self.cams[camera_id] as cam:
                # Aquire multi frames synchronously
                for frame in cam.get_frame_generator(limit=frame_limit, timeout_ms=3000): #default is 2000ms
                    #self.plot_frame(frame)
                    print(frame)
                    self.save_image_data(frame, folder_path)
                    pass
            
    def convert_to_array(self, frame):
        image_array = np.copy(frame.as_numpy_ndarray())
        return image_array
        


# Usage
#camera_handler = CAMERA()  # Instantiate the CAMERA class
#camera_id = camera_handler.list_choose_cameras()
#print(camera_id)
#camera_handler.single_frame_capture(camera_id,)
# camera_handler.multi_frames_capture(camera_id, 5)
   
