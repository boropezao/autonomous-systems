from time import sleep
import smbus 

ACCEL_CONFIG = 0x1C
PWR_MGMT_1 = 0x6B
CONFIG = 0x1A

ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F

GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47


def write(i2c_addr, register, value):
    i2c.write_byte_data(i2c_addr, register, value)
    
def read(i2c_addr, register):
    return i2c.read_byte_data(i2c_addr, register)

def MPU_Init():
    write(Device_Address, CONFIG, 3)
    write(Device_Address, PWR_MGMT_1, 0)
    write(Device_Address, ACCEL_CONFIG, 0)    
    
def read_raw_data(addr):
    high = read(Device_Address, addr)
    low = read(Device_Address, addr+1)
        
    value = (( high << 8 ) | low)
    
    if(value > 32768):
        value = value - 65536
        
    return value

i2c = smbus.SMBus(1)
Device_Address = 0x68
g = 32768/2

MPU_Init()

while True:
    
    
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    
    ac_x = acc_x / g 
    ac_y = acc_y / g
    ac_z = acc_z /g
    
    print("\tAx = %.4f,\tAy = %.4f,\tAz = %.4f" % (ac_x, ac_y, ac_z))
    
    sleep(0.5)
    
    
