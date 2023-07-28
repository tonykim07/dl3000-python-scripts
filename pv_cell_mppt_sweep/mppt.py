
from dl3000.dl3000 import DL3000
from argparse import ArgumentParser
from serial import Serial
import time, csv

serial = Serial("COM5", 115200, timeout=0.002)
eload_resource = "USB0::6833::3601::DL3A192600119::0::INSTR"

eload = DL3000(eload_resource)

class MPPT(): 

    def __init__(self): 
        self.max_current = 0
        self.max_voltage = 0
        self.max_power = 0
        self.num_points = 10000
        self.filename = None
        self.current_range = [0, 7]
        self.interval = 1000

    def argument_parser(self): 
        pass

    def create_csv(self):
        current_time = time.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_name = "MPPT_" + current_time + ".csv"
        # self.file = open(file_name, "w")

    def init_eload(self):   
        eload.reset()
        eload.set_mode("CURR")
        eload.set_cc_current(0)

    def find_mppt(self): 

        with open(self.filename, "w") as file: 
                
                logger = csv.writer(file, newline="")
    
                for i in range(self.num_points):
                    eload.set_cc_current((i * self.current_range[1] - self.current_range[0])/self.num_points + self.current_range[0])
                    curr_voltage = eload.read_voltage()
                    curr_current = eload.read_current()

                    if curr_voltage * curr_current > self.max_current * self.max_voltage: 
                        self.max_current = curr_current
                        self.max_voltage = curr_voltage
                        self.max_power = curr_voltage * curr_current

                    logger.writerow([curr_voltage, curr_current])
                
                    time.sleep(self.interval / 1000)
        
        return self.max_current, self.max_voltage, self.max_power
    
