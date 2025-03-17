class Settings:
    def __init__(self, frequency:float = 60, base_power:float = 100):
        self.frequency = frequency # default = 60 Hz
        self.base_power = base_power # default = 100 MVA

    def __repr__(self):
        return f"Settings(frequency={self.frequency} Hz, base_power={self.base_power} MVA)"