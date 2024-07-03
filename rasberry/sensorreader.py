from time import sleep
import smbus
import mpu
import bmp

class SensorReader:
    
    
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.mpu = mpu.MPUSensor(self.bus)
        self.bmp = bmp.BMPSensor(self.bus)
        
        
    def read_sensors(self):
        
        ax, ay, az = self.mpu.read_data()
        temp, pres, alt = self.bmp.readBmp180()
        
        return (ax, ay, az, temp, pres, alt)
        