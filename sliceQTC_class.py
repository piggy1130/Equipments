import serial

class SLICE_QTC:
    
    # we are using channel 3 now
    slice_qtc = serial.Serial('COM8', 9600, timeout=10)

    def __init__(self):
        if self.slice_qtc.isOpen():
            print(f"Connected to {self.slice_qtc.name}")
    
    def set_temp(self, temp):
        msg = "TempSet 3 " + str(temp) + " \r"
        self.slice_qtc.write(str.encode(msg))
        print(self.slice_qtc.readline())
    
    def read_temp(self):
        msg = "Temp? 3\r"
        self.slice_qtc.write(str.encode(msg))
        current_temp = self.slice_qtc.readline()
        current_temp = current_temp.decode('utf-8')
        return current_temp
        #print(current_temp) # b'21.049957\r\n'
        #print(current_temp.decode('utf-8')) # 21.049957
    
    def end_slice(self):
        self.slice_qtc.close()

# slice_qtc.write(b'TempSet 3 21.05\r');
# print(slice_qtc.readline())
# slice_qtc.write(b'Temp? 3\r');
# print(slice_qtc.readline())

# slice_qtc.close()

# slice = SLICE_QTC()
# slice.set_temp("21.03")
# print("*****")
# slice.read_temp()