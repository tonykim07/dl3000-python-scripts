
from dl3000.dl3000 import DL3000
from serial import Serial
import time, csv

serial = Serial("COM5", 115200, timeout=0.002)
eload_resource = "USB0::0x1AB1::0x0E11::DL3A192600119::INSTR"

eload = DL3000(eload_resource)

class PSM_Logger(): 

    def __init__(self): 
        self.current_min = 0
        self.current_max = 20
        self.interval = 1000
        self.num_samples = 20
        self.filename = None
        self.file = None

    def argument_parser(self):
        pass
    
    def create_csv(self): 
        self.filename = "PSM_Calibration.csv"

    def init_eload(self): 
        eload.reset()
        eload.set_mode("CURR")
        eload.set_cc_current(0)
        eload.enable()

    def run_current_test(self): 
        
        with open(self.filename, "w") as file:
            
            logger = csv.writer(file, delimiter=",")

            for i in range(self.num_samples):
                eload.set_cc_current((i * self.current_max - self.current_min)/self.num_samples + self.current_min)

                serial_data = ""
                while(serial_data == ""): 
                    serial_data = serial.readline().decode("utf-8")
                    time.sleep(0.001)
                
                logger.writerow([serial_data, eload.read_current()])

                time.sleep(self.interval / 1000)
            
        eload.set_cc_current(0)
        eload.disable()
        
    def characterize(self):
        pass # calculate line of best fit from data

