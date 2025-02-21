import socket
import json
import re

class OSCILLOSCOPE:
    BNC_IP = "10.246.8.58"
    BNC_PORT = 3000

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((OSCILLOSCOPE.BNC_IP, OSCILLOSCOPE.BNC_PORT))

    def send_command(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((OSCILLOSCOPE.BNC_IP, OSCILLOSCOPE.BNC_PORT))
            s.sendall((command + "\n").encode())
            #response = s.recv(4096).decode().strip()
            response = s.recv(4096)
            return response
        
    def get_voltage(self, command=":MEASUrement:CH2?"):
        # read voltage
        voltage = self.send_command(command)
        # Convert binary response to string
        decoded_str = voltage.decode(errors='ignore')
        # Extract JSON part using regex
        json_match = re.search(r'\{.*\}', decoded_str)

        if json_match:
            json_str = json_match.group()  # Extract JSON-like content

            try:
                # Parse JSON
                json_data = json.loads(json_str)
                # Extract the average value from CH2
                avg_value_str = json_data.get("CH2", {}).get("AVERage", "N/A")

                # Convert to numerical value
                if "mV" in avg_value_str:
                    avg_value = float(avg_value_str.replace("mV", "").strip()) / 1000  # Convert mV to V
                elif "V" in avg_value_str:
                    avg_value = float(avg_value_str.replace("V", "").strip())
                else:
                    avg_value = "N/A"

                #print(f"Extracted Average Value (CH2): {avg_value} V")
                return avg_value

            except json.JSONDecodeError:
                print("Error: Could not parse JSON data.")
                return None
        else:
            print("Error: JSON data not found in response.")
            return None
    
    def close(self):
        # close the socket connection when done
        self.s.close()


# Example Usage:
if __name__ == '__main__':
    osc = OSCILLOSCOPE()

    response = osc.send_command("*IDN?")
    print("Instrument ID: ", response)

    voltage = osc.get_voltage()
    print("Current Voltage: ", voltage)


