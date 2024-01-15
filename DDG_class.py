import serial

class BaseDDGChannel:
    def __init__(self, channel_number):
        self.channel_number = channel_number
        self.state = None
        self.delay = None
        self.sync_channel = None
        self.width = None

    def set_state(self, state_status, connection, info_dict):
        self.state = state_status
        info_dict[f"DDG_channel_{self.channel_number}.state"] = state_status
        # msg = ":PULSE1:STAT ON\r\n"
        msg = f":PULSE{self.channel_number}:STAT {state_status}\r\n"
        connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        connection.readline()

    def set_delay(self, delay_value, connection, info_dict):
        self.delay = delay_value
        info_dict[f"DDG_channel_{self.channel_number}.delay"] = delay_value
        # msg = ":PULSE1:DEL -135e-6\r\n"
        msg = f":PULSE{self.channel_number}:DEL {delay_value}\r\n"
        connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        connection.readline()

    def set_sync_channel(self, channel, connection, info_dict):
        self.sync_channel = channel
        info_dict[f"DDG_channel_{self.channel_number}.sync_channel"] = channel
        msg = f":PULSE{self.channel_number}:SYNC {channel}\r\n"
        connection.write(str.encode(msg))
        connection.readline()

    def set_width(self, width_val, connection, info_dict):
        self.width = width_val
        info_dict[f"DDG_channel_{self.channel_number}.width"] = width_val
        # msg = ":PULSE1:WIDT 10e-6\r\n"
        msg = f":PULSE{self.channel_number}:WIDT {width_val}\r\n"
        connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        connection.readline()

# Specific channel classes inheriting from BaseDDGChannel
class DDG_channel_1(BaseDDGChannel):
    def __init__(self):
        super().__init__(1)

class DDG_channel_2(BaseDDGChannel):
    def __init__(self):
        super().__init__(2)

class DDG_channel_3(BaseDDGChannel):
    def __init__(self):
        super().__init__(3)

class DDG_channel_4(BaseDDGChannel):
    def __init__(self):
        super().__init__(4)

class DDG_channel_5(BaseDDGChannel):
    def __init__(self):
        super().__init__(5)

class DDG_channel_6(BaseDDGChannel):
    def __init__(self):
        super().__init__(6)

class DDG_channel_7(BaseDDGChannel):
    def __init__(self):
        super().__init__(7)

class DDG_channel_8(BaseDDGChannel):
    def __init__(self):
        super().__init__(8)


class DDG:
    connection = serial.Serial('/dev/ttyUSB0', 115200)

    def __init__(self):
        self.channels = {
            1: DDG_channel_1(),
            2: DDG_channel_2(),
            3: DDG_channel_3(),
            4: DDG_channel_4(),
            5: DDG_channel_5(),
            6: DDG_channel_6(),
            7: DDG_channel_7(),
            8: DDG_channel_8(),                               
        }
        self.DDG_Initialization()

    # channel 1 & 2 ON
    # channel 3 & 5 & 6 & 7 & 8 OFF
    # channel 4(D) - nothing 
    def DDG_Initialization(self, info_dict):
        # ****************************************************************
        # channel A - Nd: YAG flashlamp
        # state on
        self.channels[1].set_state("ON", self.connection, info_dict)
        # channel A SYNC channel B   
        self.channels[1].set_sync_channel("CHB", self.connection, info_dict)
        # set channel A delay: -135e-6 (-135um)    
        self.channels[1].set_delay("-135e-6", self.connection, info_dict)
        # set channel A width to 10e-6    
        self.channels[1].set_width("10e-6", self.connection, info_dict)
        # ****************************************************************
        # channel B - Nd: YAG Q-switch
        # state on
        self.channels[2].set_state("ON", self.connection, info_dict)
        # channel B SYNC channel F
        self.channels[2].set_sync_channel("CHF", self.connection, info_dict)
        # set channel B delay: 470e-6 
        self.channels[2].set_delay("470e-6", self.connection, info_dict)
        # set channel B width to 10e-6
        self.channels[2].set_width("10e-6", self.connection, info_dict)
        # ****************************************************************
        # channel C - Scope trigger
        # state on
        self.channels[3].set_state("OFF", self.connection, info_dict)
        # channel C SYNC channel B
        self.channels[3].set_sync_channel("CHB", self.connection, info_dict)
        # set channel C delay: 0
        self.channels[3].set_delay("0", self.connection, info_dict)
        # set channel C width to 10e-6
        self.channels[3].set_width("10e-6", self.connection, info_dict)
        # ****************************************************************
        # channel D - NOTHING RIGHT NOW
        # state on
        self.channels[4].set_state("OFF", self.connection, info_dict)
        # channel C SYNC channel B
        self.channels[4].set_sync_channel("CHB", self.connection, info_dict)
        # set channel C delay: 0
        self.channels[4].set_delay("0", self.connection, info_dict)
        # set channel C width to 10e-6
        self.channels[4].set_width("10e-6", self.connection, info_dict)
        # ****************************************************************
        # channel E - ablation flashlamp
        # state off
        self.channels[5].set_state("OFF", self.connection, info_dict)
        # channel E SYNC channel T0
        self.channels[5].set_sync_channel("T0", self.connection, info_dict)
        # set channel E delay: 10e-3 
        self.channels[5].set_delay("10e-3", self.connection, info_dict)
        # set channel E width to 10e-6
        self.channels[5].set_width("10e-6", self.connection, info_dict)
        # ****************************************************************
        # channel F - ablation Q-switch
        # state off
        self.channels[6].set_state("OFF", self.connection, info_dict)
        # channel F SYNC channel E
        self.channels[6].set_sync_channel("CHE", self.connection, info_dict)
        # set channel F delay: 110e-6 
        self.channels[6].set_delay("110e-6", self.connection, info_dict)
        # set channel F width to 10e-6
        self.channels[6].set_width("10e-6", self.connection, info_dict)
        # ****************************************************************
        # channel G - nozzle
        # state oFF
        self.channels[7].set_state("OFF", self.connection, info_dict)
        self.channels[7].set_sync_channel("CHF", self.connection, info_dict)
        self.channels[7].set_delay("-460e-6", self.connection, info_dict)
        self.channels[7].set_width("250e-6", self.connection, info_dict)
        # ****************************************************************
        # channel H - PMT switch
        self.channels[8].set_state("OFF", self.connection, info_dict)
        self.channels[8].set_sync_channel("CHB", self.connection, info_dict)
        self.channels[8].set_delay("-680e-9", self.connection, info_dict)
        self.channels[8].set_width("1e-6", self.connection, info_dict)

    # All channel ON 
    def DDG_Start(self, info_dict):
        self.channels[3].set_state("ON", self.connection, info_dict)
        self.channels[5].set_state("ON", self.connection, info_dict)
        self.channels[6].set_state("ON", self.connection, info_dict)
        self.channels[7].set_state("ON", self.connection, info_dict)
        self.channels[8].set_state("ON", self.connection, info_dict)

    # channel 1 & 2 ON
    # channel 3 & 5 & 6 & 7 & 8 OFF
    def DDG_End(self, info_dict):
        self.channels[3].set_state("OFF", self.connection, info_dict)
        self.channels[5].set_state("OFF", self.connection, info_dict)
        self.channels[6].set_state("OFF", self.connection, info_dict)
        self.channels[7].set_state("OFF", self.connection, info_dict)
        self.channels[8].set_state("OFF", self.connection, info_dict)


# Usage example
# ddg = DDG()
# ddg.channels[1].set_state("ON", ddg.connection, info_dict)
        
