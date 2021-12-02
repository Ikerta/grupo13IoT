import time,sys


import time,sys
import RPi.GPIO as GPIO
import smbus

class HeartbeatSensor(object):

    def __init__(self):
        """
        Connect to an I2C port.
        """
        rev = GPIO.RPI_REVISION
        if rev == 2 or rev == 3:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = smbus.SMBus(0)
        self.address = 0x50

    def get(self):
        """
        Returns the heart rate of the wearer.
        :return: Integer
        """
        return self.bus.read_byte(0x50)

if __name__ == "__main__":

    pulse = HeartbeatSensor()
    while True:
        try:
            rate = pulse.get()
            print(rate)
        except IOError:
            print("Error")
        time.sleep(5)
