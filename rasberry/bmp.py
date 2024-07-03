#Data del sensor digital BMP180
#datos obtenidos de BMP180 Digital Pressure Sensor Data Sheet de Bosch
#Esta archivo es la declaración del BMP180 (modulo) para que el archivo bmp180_lalo pueda immportar este 
#  modulo y con ello iniciar correspondiente 


import time
from ctypes import c_short
 

class BMPSensor:
    
    DEVICE = 0x77 #Ocupamos el puerto I2c (debe estar activado en nuestra raspberry) se localiza en el canal 77
    
    def __init__(self, bus):
        self.bus = bus

    #Para convertir la función binaria a un string ocupamos hacer lo siguiente:
    def convertToString(self, data):
      return str((data[1] + (256 * data[0])) / 1.2)

    def getShort(self, data, index):
        #Nos regresa 2 bytes de la data que son asignados a un valor de 16-bits
      return c_short((data[index] << 8) + data[index + 1]).value

    def getUshort(self, data, index):
      #Nos regresa 2 bytes de la data que son asignados a un valor sin signo de 16-bits
      return (data[index] << 8) + data[index + 1]
  
    def readBmp180(self, addr=0x77):
      # Dirección de Registro
      REG_CALIB  = 0xAA
      REG_MEAS   = 0xF4
      REG_MSB    = 0xF6
      REG_LSB    = 0xF7
      # Control de Dirección de Registro
      CRV_TEMP   = 0x2E
      CRV_PRES   = 0x34 
      # Oversample setting
      OVERSAMPLE = 3    # 0 - 3
  
  # Lectura de calibración de data
  # Lectura de calibración de data desde EEPROM
      cal = self.bus.read_i2c_block_data(addr, REG_CALIB, 22)

  # Converción de los byte de data a valores alfanuméricos
  # Calibración de coeficientes
  
      AC1 = self.getShort(cal, 0)
      AC2 = self.getShort(cal, 2)
      AC3 = self.getShort(cal, 4)
      AC4 = self.getUshort(cal, 6)
      AC5 = self.getUshort(cal, 8)
      AC6 = self.getUshort(cal, 10)
      B1  = self.getShort(cal, 12)
      B2  = self.getShort(cal, 14)
      MB  = self.getShort(cal, 16)
      MC  = self.getShort(cal, 18)
      MD  = self.getShort(cal, 20)

  # Lectura de la temperatura
      self.bus.write_byte_data(addr, REG_MEAS, CRV_TEMP)
      time.sleep(0.005)
      (msb, lsb) = self.bus.read_i2c_block_data(addr, REG_MSB, 2)
      UT = (msb << 8) + lsb

  # Lectura de la presión
      self.bus.write_byte_data(addr, REG_MEAS, CRV_PRES + (OVERSAMPLE << 6))
      time.sleep(0.04)
      (msb, lsb, xsb) = self.bus.read_i2c_block_data(addr, REG_MSB, 3)
      UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - OVERSAMPLE)

  # vamos a redefinir la temperatura
      X1 = ((UT - AC6) * AC5) >> 15
      X2 = (MC << 11) / (X1 + MD)
      B5 = X1 + X2
      temperature = int(B5 + 8) >> 4
      temperature = temperature / 10.0

  # vamos a redefinir la presión
      B6  = B5 - 4000
      B62 = int(B6 * B6) >> 12
      X1  = (B2 * B62) >> 11
      X2  = int(AC2 * B6) >> 11
      X3  = X1 + X2
      B3  = (((AC1 * 4 + X3) << OVERSAMPLE) + 2) >> 2

      X1 = int(AC3 * B6) >> 13
      X2 = (B1 * B62) >> 16
      X3 = ((X1 + X2) + 2) >> 2
      B4 = (AC4 * (X3 + 32768)) >> 15
      B7 = (UP - B3) * (50000 >> OVERSAMPLE)

      P = (B7 * 2) / B4

      X1 = (int(P) >> 8) * (int(P) >> 8)
      X1 = (X1 * 3038) >> 16
      X2 = int(-7357 * P) >> 16
      pressure = int(P + ((X1 + X2 + 3791) >> 4))
  #presión datos obtenidos de la hoja técnica BOSCH para bmp180
  
  
      altitude = 44330.0 * (1.0 - pow(pressure / 101325.0, (1.0/5.255)))
      altitude = round(altitude,2)

      return (temperature,pressure,altitude)

