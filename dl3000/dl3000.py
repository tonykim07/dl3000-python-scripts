
# Programming Manual for DL3000 Electronic Load
# https://www.batronix.com/files/Rigol/Elektronische-Lasten/DL3000/DL3000_ProgrammingManual_EN.pdf

from pyvisa import ResourceManager
from time import sleep

class DL3000(): 

    def __init__(self, resource): 
        self.resource = resource
        self.inst = ResourceManager().open_resource(self.resource)

    def __enter__(self): 
        self.inst = ResourceManager().open_resource(self.resource)
        return self
    
    def __exit__(self):
        if self.inst: 
            self.inst.close() 

    # Common Commands
    def reset(self): 
        return self.inst.write("*RST")
    
    # Measurement Commands
    def read_voltage(self): 
         return float(self.inst.query(":MEAS:VOLT?").partition("\n")[0])
    
    def read_current(self): 
        return float(self.inst.query(":MEAS:CURR?").partition("\n")[0])
    
    def read_resistance(self): 
        return float(self.inst.query(":MEAS:RES?").partition("\n")[0])
    
    def read_power(self): 
        return float(self.inst.query(":MEAS:POW?").partition("\n")[0])
    
    def read_battery_capacity(self): 
        return float(self.inst.query(":MEAS:CAP?").partition("\n")[0])
    
    def read_watt_hours(self): 
        return float(self.inst.query(":MEAS:WATT?").partition("\n")[0])
    
    def read_discharge_time(self):
        return float(self.inst.query(":MEAS:DISCT?").partition("\n")[0])
    
    def read_integration_time(self): 
        return float(self.inst.query(":MEAS:TIME?").partition("\n")[0])
    
    # # returns 400 consecutive data points
    # def read_wave_data(self): 
    #     return float(self.inst.query(":MEAS:WAV?").partition("\n")[0])

    # Source commands
    def enable(self):
        self.inst.write(":SOURCE:INPUT:STAT ON")

    def disable(self):
        self.inst.write(":SOURCE:INPUT:STAT OFF")

    def is_enabled(self):
        return self.inst.query(":SOURCE:INPUT:STAT?").strip() == "1"

    # (CURR, VOLT, RES, POW)
    def set_mode(self, mode="CURR"): 
        self.inst.write(":SOURCE:FUNCTION {}".format(mode))

    def get_mode(self): 
        return self.inst.query(":SOURCE:FUNCTION?").strip()
    
    # CC
    def set_cc_current(self, current):
        return self.inst.write(":SOURCE:CURRENT:LEV:IMM {}".format(current))

    def set_cc_slew_rate(self, slew):
        self.inst.write(f":SOURCE:CURRENT:SLEW {slew}")

    def set_cc_voltage_limit(self, voltage): 
        self.inst.write(f":SOURCE:CURRENT:VLIM {voltage}")

    def set_cc_current_limit(self, current): 
        self.inst.write(f":SOURCE:CURRENT:ILIM {current}")

    # CV
    def set_cv_voltage(self, voltage): 
        return self.inst.write(":SOURCE:VOLTAGE:LEV:IMM {}".format(voltage))
    
    def set_cv_voltage_limit(self, voltage): 
        self.inst.write(f":SOURCE:VOLTAGE:VLIM {voltage}")

    def set_cv_current_limit(self, current):
        self.inst.write(f":SOURCE:VOLTAGE:ILIM {current}")

    # CR
    def set_cr_resistance(self, resistance): 
        return self.inst.write(":SOURCE:RES:LEV:IMM {}".format(resistance))
    
    def set_cr_voltage_limit(self, voltage):
        self.inst.write(f":SOURCE:RES:VLIM {voltage}")

    def set_cr_current_limit(self, current): 
        self.inst.write(f":SOURCE:RES:ILIM {current}")

    # CP 
    def set_cp_power(self, power):
        return self.inst.write(":SOURCE:POWER:LEV:IMM {}".format(power))
    
    def set_cp_voltage_limit(self, voltage):
        self.inst.write(f":SOURCE:POWER:VLIM {voltage}")

    def set_cp_current_limit(self, current): 
        self.inst.write(f":SOURCE:POWER:ILIM {current}")

    def set_to_list_mode(self, mode="CC"): 
        self.inst.write(":SOURCE:LIST:MODE {}".format(mode))

    # System commands
    # See page 58 of the programming manual for mapping of key values
    def sim_key(self, key_value): 
        self.inst.write(":SYSTEM:KEY {}".format(key_value))
        sleep(1)

    def read_error(self): 
        return self.inst.query(":SYSTEM:ERR")
