
from pyvisa import ResourceManager

class DL3000(): 

    def __init__(self, inst): 
        self.inst = inst

    def read_voltage(self): 
        return float(self.inst.query(":MEAS:VOLT?").partition("\n")[0])

    def read_current(self): 
        return float(self.inst.query(":MEAS:CURR?").partition("\n")[0])

    def read_power(self): 
        return float(self.inst.query(":MEAS:POW?").partition("\n")[0])

    def read_resistance(self): 
        return float(self.inst.query(":MEAS:RES?").partition("\n")[0])

    def is_enabled(self): 
        return self.inst.query(":SOURCE:INPUT:STAT?").strip() == "1"

    def enable(self): 
        self.inst.write(":SOURCE:INPUT:STAT ON")

    def disable(self): 
        self.inst.write(":SOURCE:INPUT:STAT OFF")

    def set_mode(self, mode="CC"): 
        self.inst.write(":SOURCE:FUNCTION {}".format(mode))

    def query_mode(self): 
        return self.inst.query(":SOURCE:FUNCTION?").strip()

    def set_cc_current(self, current): 
        return self.inst.write(":SOURCE:CURRENT:LEV:IMM {}".format(current))

    def set_cv_voltage(self, voltage): 
        pass

    def set_cp_power(self, power): 
        return self.inst.write(":SOURCE:POWER:LEV:IMM {}".format(power))

    def set_cr_resistance(self, resistance): 
        pass






