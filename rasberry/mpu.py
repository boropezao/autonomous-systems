from time import sleep

ACCEL_CONFIG = 0x1C
PWR_MGMT_1 = 0x6B
CONFIG = 0x1A

ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F

GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

class MPUSensor:
    
    device_Address = 0x68
    g = 32768/2
    
    def __init__(self, bus):
        self.bus = bus
        
    def config(self):
        self.bus.write_byte_data(self.device_Address, CONFIG, 3)
        self.bus.write_byte_data(self.device_Address, PWR_MGMT_1, 0)
        self.bus.write_byte_data(self.device_Address, ACCEL_CONFIG, 0) 
    
    def read_raw_data(self, addr):
        high = self.bus.read_byte_data(self.device_Address, addr)
        low = self.bus.read_byte_data(self.device_Address, addr+1)
        
        value = (( high << 8 ) | low)
        
        if(value > 32768):
            value = value - 65536
        
        return value
    
    
    def read_data(self):
        acc_x = self.read_raw_data(ACCEL_XOUT_H)
        acc_y = self.read_raw_data(ACCEL_YOUT_H)
        acc_z = self.read_raw_data(ACCEL_ZOUT_H)
        ac_x = acc_x / self.g 
        ac_y = acc_y / self.g
        ac_z = acc_z / self.g
        
        return (ac_x, ac_y, ac_z)
    
    
    

