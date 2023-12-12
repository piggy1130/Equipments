from toptica.lasersdk.dlcpro.v2_4_0 import DLCpro, NetworkConnection
from toptica.lasersdk.utils.dlcpro import *

class LASER:

    __LASER_ID__ = '729 nm'
    network_connection = NetworkConnection( __LASER_ID__)
    
    def __init__(self):
        print("Laser is ready to use!")


    def set_voltage(self, voltage):
        # note: the with-statement automatically calls open() and close () of the connection class
        # at the appropriate times.
        with DLCpro(self.network_connection) as dlc:
            dlc.laser1.dl.pc.voltage_set.set(voltage) 

  