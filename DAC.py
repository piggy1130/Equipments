import board
import busio
import adafruit_mcp4725

class DACController:
    def __init__(self, vcc=3.3, max_dac_value=4095):
        self.vcc = vcc
        self.max_dac_value = 4095 # 12-bit DAC (0-4095)
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.dac = adafruit_mcp4725.MCP4725(self.i2c)

    def set_voltage(self, voltage):
        if voltage < 0 or voltage > self.vcc:
            print("Voltage out of range")
            return

        dac_value = int((voltage / self.vcc) * self.max_dac_value)
        self.dac.raw_value = dac_value  # Set DAC output
        print(f"Setting Voltage(DAC): {voltage}V")

# Main script for user interaction
if __name__ == "__main__":
    dac = DACController()
    dac.set_voltage(2.5)
    