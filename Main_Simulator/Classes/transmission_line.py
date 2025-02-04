class TransmissionLine:
    def __init__(self, name:str, bus1:str, bus2:str, bundle:str, geometry:str, length:float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length
        self.series_impedance = None
        self.shunt_admittance = None
        self.admittance_matrix = []
        # self.calc_series_impedance()
        # self.calc_shunt_admittance()
        # self.calc_admittance_matrix()

    #def calc_series_impedance(self):
        # this will be implemented in milestone 3

    #def calc_shunt_admittance(self):
        # this will be implemented in milestone 3

    #def calc_admittance_matrix(self):
        # this will be implemented in milestone 3

# Validation
if __name__ == '__main__':
    line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2",
                             "Bundle 1", "Geometry 1", 10)
    print(line1.name, line1.bus1, line1.bus2, line1.bundle, line1.geometry, line1.length)
    # print(line1.zbase, line1.ybase)
    # print(line1.zseries, line1.yshunt, line1.yseries)
    # print(line1.yprim)