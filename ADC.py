# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class ADCController:
    def __init__(self):
        # Hardware SPI configuration:
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.adc = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
        # CLK  = 11
        # MISO = 9
        # MOSI = 10
        # CS   = 8

    def get_voltage(self):
        value = self.adc.read_adc(0)
        adc_voltage = value/1024 * 3.3
        return adc_voltage

# Main script for user interaction
if __name__ == "__main__":
    adc = ADCController()
    voltage = adc.get_voltage()
    print(f"voltage is: {voltage} v")
