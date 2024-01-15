import socket

class Dye_Laser:
    HOST_DYE = '10.246.8.124'
    PORT_DYE = 65510
    laser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    laser.connect((HOST_DYE, PORT_DYE))

    def __init__(self):
        print("start to create dye laser")
        # HOST_DYE = '10.246.8.124'
        # PORT_DYE = 65510
        # self.laser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.laser.connect((HOST_DYE, PORT_DYE))
        self.BUFFER_SIZE = 1024
        self.remote_connection()
        # print("Create Dye Laser")

    def remote_connection(self):
        remote_connect_msg = "RemoteConnect\r\n"
        self.laser.send(remote_connect_msg.encode('utf-8'))
        data = self.laser.recv(self.BUFFER_SIZE)
        print(data.decode('utf-8'))

    def set_wavelength(self, wavelength, info_dict):
        msg = "SetWavelength " + str(wavelength) + "\r\n"
        self.laser.send(msg.encode('utf-8')) #convert the string to bytes
        info_dict["Dye_Laser_wavelength"] = wavelength
        data = self.laser.recv(self.BUFFER_SIZE)
        print(data.decode('utf-8'))

    def close_laser(self):
        self.laser.close()

# dye_laser = Dye_Laser()
   
        
        