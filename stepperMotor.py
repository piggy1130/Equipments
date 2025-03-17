import time
from time import sleep
import RPi.GPIO as GPIO

class StepperMotor:

    def __init__(self, pulse_pin=23, direction_pin=24, position_file="position.txt", max_position=200):
        self.pulse_pin = pulse_pin
        self.direction_pin = direction_pin
        self.position_file = position_file
        self.max_position = max_position
        with open(self.position_file, 'r') as file:
            self.current_position = int(file.read().strip())

        # Stepper motor movement parameters
        self.pulses_per_rev = 200  # User-defined
        self.distance_per_rev = 5   # 5mm per revolution
        self.distance_per_pulse = self.distance_per_rev / self.pulses_per_rev
        self.sleep_time = 0.01  # Delay per step

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pulse_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.direction_pin, GPIO.OUT, initial=GPIO.LOW)

    def read_position(self):
        with open(self.position_file, 'r') as file:
            return int(file.read().strip())

    def write_position(self, position):
        with open(self.position_file, 'w') as file:
            file.write(str(position))

    def validate_move(self, direction, distance):
        new_position = self.current_position + distance * direction
        if new_position > self.max_position or new_position < 0:
            print("Invalid Input - Can not move that much!")
            self.cleanup()
            exit()
        return new_position

    def move(self, direction, distance):
        # Set direction
        if direction == 1:
            GPIO.output(self.direction_pin, True)
        else:
            GPIO.output(self.direction_pin, False)
        # set move
        total_number_pulses = int(distance / self.distance_per_pulse)
        pulse_count = 0
        try:
            while pulse_count < total_number_pulses:
                GPIO.output(self.pulse_pin, True)
                time.sleep(self.sleep_time)
                GPIO.output(self.pulse_pin, False)
                time.sleep(self.sleep_time)
                pulse_count += 1
        except KeyboardInterrupt:
            self.cleanup()
            print("\nMovement interrupted!")
            exit()  
        # update motor position          
        self.current_position = self.current_position + distance * direction

    def cleanup(self):
        GPIO.cleanup()


# Main script for user interaction
if __name__ == "__main__":
    motor = StepperMotor()
    print(f"Current position of Stepper Motor: {motor.read_position()} mm")

    direction = input("Direction (-1 forward with less pace / 1 backford with more space): ")
    direction = int(direction)
    distance = input("Distance you want to move(mm): ")
    distance = int(distance)
    motor.pvalidate_move(direction, distance)
    motor.move(direction, distance)
    motor.cleanup()    
