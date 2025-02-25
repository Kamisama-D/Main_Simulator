from Classes.bus import Bus


class Generator:
    def __init__(self, name:str, bus:Bus, voltage_setpoint:float, mw_setpoint:float):
        self.name = name
        self.bus = bus
        self.voltage_setpoint = voltage_setpoint # Target voltage magnitude in per unit.
        self.mw_setpoint = mw_setpoint # Real power generation in MW.

    def __repr__(self):
        return (f"Generator(name='{self.name}', bus='{self.bus.name}', "
                f"voltage_setpoint={self.voltage_setpoint} p.u., mw_setpoint={self.mw_setpoint} MW)")