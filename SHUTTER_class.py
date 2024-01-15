import serial

class SHUTTER:
    def __init__(self, port='/dev/Shutter_UNO', baudrate=115200, timeout=10):
        # Initialize the serial connection to the shutter device
        self.shutter = serial.Serial(port, baudrate, timeout=timeout)

    def control_shutter(self, msg):
        # Send a message to the shutter device
        self.shutter.write(str.encode(msg))

        # Read the response from the shutter device
        line = self.shutter.read_until()
        # Optional: Process the line (decode, strip newlines, etc.)
        # line = line.decode().strip('\r\n')

        # Optional: Print the response or return it
        # print(line)
        # return line

# Usage example:
# shutter = SHUTTER()
# shutter.control_shutter("open")  # or any other command