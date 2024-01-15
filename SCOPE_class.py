import serial
import vxi11
import time

class BaseSCOPEChannel:
    def __init__(self, channel_number):
        self.channel_number = channel_number
        self.state = None

    def set_state(self, state_status, info_dict, connection):
        self.state = state_status
        # "SCOPE_channel_1.state"
        info_dict[f"SCOPE_channel_{self.channel_number}.state"] = state_status
        # "SELect:CH2 " + state_status
        msg = f"SELect:CH{self.channel_number} {state_status}"
        connection.write(msg)

class SCOPEChannel1(BaseSCOPEChannel):
    def __init__(self):
        super().__init__(1)

class SCOPEChannel2(BaseSCOPEChannel):
    def __init__(self):
        super().__init__(2)

class SCOPEChannel3(BaseSCOPEChannel):
    def __init__(self):
        super().__init__(3)

class SCOPEChannel4(BaseSCOPEChannel):
    def __init__(self):
        super().__init__(4)


class SCOPE:
    connection = vxi11.Instrument("10.246.8.106")

    def __init__(self):
        self.channels = {
            1: SCOPEChannel1(),
            2: SCOPEChannel2(),
            3: SCOPEChannel3(),
            4: SCOPEChannel4()
        }
        self.SCOPE_Initialization()

    def SCOPE_Initialization(self, info_dict):
        points = 5000
        self.connection.write("HORizontal:MAIn:SCAle 200e-9")
        self.connection.write("DATa:ENCdg ASCii") # Set the data format, ASCII here 
        self.connection.write("WFMOutpre:BYT_Nr 1") 
        self.connection.write("DATa:STARt 1") # data start point, first position is 1 
        self.connection.write("DATa:STOP {}".format(points)) # data end point 
        self.connection.write("DATa:SOUrce CH3") # pick up channel
        self.connection.write("ACQuire:STOPAfter SEQuence") 
      
        # channel 2 & 3 ON
        # channel 1 & 4 OFF
        self.channels[1].set_state("OFF", info_dict, self.connection)
        self.channels[2].set_state("ON", info_dict, self.connection)
        self.channels[3].set_state("ON", info_dict, self.connection)
        self.channels[4].set_state("OFF", info_dict, self.connection)

    def SCOPE_StartToAcquireData(self):
        self.connection.write("HORizontal:FASTframe:STATE ON")
        self.connection.write("HORizontal:FASTframe:COUNt 20")
        self.connection.write("ACQuire:STATE RUN") # when acquiring data: STATE == 1

    def SCOPE_GetandUpdate_Data(self, info_dict):
        # when acquiring data process is DOEN, STATE == 0
        need_state = ":ACQUIRE:STATE 1" 
        test_state = self.connection.ask("ACQuire:STATE?")
        while(test_state == need_state):
            test_state = self.connection.ask("ACQuire:STATE?")
            time.sleep(0.1)
        self.raw_data = self.connection.ask("CURVe?") # transfer data to us
        
        #update the raw_data
        data_arr = self.raw_data.split()
        data_arr.pop(0) #take off "curve:"
        data_str = data_arr[0] #datatype is string
        data_list = data_str.split(',') #splite str based on ','
        data_float_list = [float(i) for i in data_list]
        #get X_zero - XZE_num
        XZE = self.connection.ask("WFMO:XZE?")
        XZE_arr = XZE.split()
        XZE_num = float(XZE_arr[1])
        # print("XZE_num is: ", XZE_num)
        #get x increase step - XIN_num
        XIN = self.connection.ask("WFMO:XIN?")
        XIN_arr = XIN.split()
        XIN_num = float(XIN_arr[1])
        # print("X increase step is: ", XIN_num)
        #get y off value - YOF_num
        YOF = self.connection.ask("WFMO:YOF?") 
        YOF_arr = YOF.split()
        YOF_num = float(YOF_arr[1])
        # print("Y off amount is: ", YOF_num)
        #get y multiplier - YMU_num
        YMU = self.connection.ask("WFMO:YMU?") 
        YMU_arr = YMU.split()
        YMU_num = float(YMU_arr[1])
        # print("Y off amount is: ", YMU_num)
        #get y zero point - YZE_num
        YZE = self.connection.ask("WFMO:YZE?")
        YZE_arr = YZE.split()
        YZE_num = float(YZE_arr[1])
        #Calculation formula: 
        # y = (data-YOF_num)*YMU_num + YZE_num
        # x = 0 + XIN_num * i
        self.updated_scope_data = []
        for i in data_float_list:
            self.updated_scope_data.append((i-YOF_num)*YMU_num+YZE_num)

        # size = len(self.updated_scope_data)
        # print(size)

        # updated_x = []
        # for i in range(size):
        #     updated_x.append(i*XIN_num)
        #print(update_x)
        # write to dictionary    
        info_dict["scope.data"] = self.updated_scope_data

    def SCOPE_BackToNormalMode(self):
        self.connection.write("HORizontal:FASTframe:STATE OFF") # get the scope back to the normal mode

