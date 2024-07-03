import serial
import time


class GPSModule:
    
    def __init__(self, port="/dev/ttyS0", baud_rate=9600):
        
        try:
            self.gps = serial.Serial(port, baud_rate)
            print("GPS connected")
        except:
            print("No GPS connected")
            
    def connect(self):
        
        print("Start")
        
        try:
            self.gps.flush()
            print("Connected")
        except:
            print("Connect GPS")
            
    def read_ub(self):
               
        try:
            data = self.gps.readline().decode("utf-8").strip()
            self.gps.flush()
            return data
        except:
            print("Connect GPS")
            
    def close_connection(self):
        
        try:
            self.gps.close()
            print("Done")
        except:
            print("Connect Microcontroller")



class NMEAParser:
    
    def __init__(self):
        self.data = ""
        self.nmea = ""
        self.nmea_available = False
    
    def parse(self, data):
        self.data = data.split(",")
        
    def gga(self):
        
        nmea_sentence = self.data[0]
        
        if nmea_sentence == "$GPGGA":
            self.nmea_available = True
            self.nmea = self.data
        
        else:
            self.nmea_available = False
        
            
    
    def show_time(self):
        
        if self.nmea_available:
            time = self.nmea[1]
            length = len(time)
            if length == 9:
                hours = int(time[0:2]) - 6
                minutes = int(time[2:4])
                seconds = int(time[4:6])
                
                print("The time is {} hours {} minutes {} seconds".format(hours, minutes, seconds))
                
                
            
    
    def show(self):
        print(self.nmea)
        
        
    
gps = GPSModule()
gps.connect()

nmea = NMEAParser()

try:
    while True:
        
        ub = gps.read_ub()
        
        if ub:
            nmea.parse(ub)
            nmea.gga()
            nmea.show_time()

        
except KeyboardInterrupt:
    gps.close_connection()
    exit()
except:
    gps.close_connection()

