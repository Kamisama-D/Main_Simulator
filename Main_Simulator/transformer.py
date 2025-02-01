class Transformer:
    def __init__(self, name:str, bus1:str, bus2:str, power_rating:float, impedance_percent, x_over_r_ratio:float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio
        self.impedance = None
        self.admittance = None
        self.calc_impedance()
        self.calc_admittance()

    def calc_impedance(self): # this will be implemented in milestone 3
        z_base = (self.power_rating / 100) * self.impedance_percent
        r = z_base / (1 + self.x_over_r_ratio**2) ** 0.5
        x = r * self.x_over_r_ratio
        self.impedance = complex(r, x)

    def calc_admittance(self): # this will be implemented in milestone 3
        self.admittance = 1 / self.impedance

# Validation
if __name__ == '__main__':
    transformer1 = Transformer("T1", "Bus 1", "Bus 2", 125,
                               8.5, 10)
    print(transformer1.name, transformer1.bus1, transformer1.bus2, transformer1.power_rating)
    # print(transformer1.zt, transformer1.yt)
    # print(transformer1.yprim)

