from Classes.bus import Bus


class Load:
    def __init__(self, name:str, bus:Bus, real_power:float, reactive_power:float):
        self.name = name
        self.bus = bus
        self.reactive_power = reactive_power # in MW
        self.real_power = real_power # in Mvar

    def __repr__(self):
        return (f"Load(name='{self.name}', bus='{self.bus.name}', "
                f"real_power={self.real_power} MW, reactive_power={self.reactive_power} Mvar)")