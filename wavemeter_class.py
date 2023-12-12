import time
from wlm import *
import serial
import datetime
import numpy as np
import pandas as pd

class WAVEMETER:
    wavemeter = serial.Serial('COM4', 115200)

    def Read_Wavemeter (self):
        self.wavemeter.write(b'I1 1\r\n')
        time.sleep(0.05)
        # print("In function - Read Wavemeter")
        wlm = WavelengthMeter()
        current_wavelength = float(wlm.wavelength)
        print(f'Current Locking wavelength is: {current_wavelength}')
        return current_wavelength
