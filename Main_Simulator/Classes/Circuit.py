from Classes.transformer import Transformer
from Classes.transmission_line import TransmissionLine
from Classes.bus import Bus
from Classes.bundle import Bundle
from Classes.geometry import Geometry
from Classes.conductor import Conductor
# import pandas as pd

class Circuit:
    """Represents a power system circuit, storing all components and managing configuration."""

    def __init__(self, name):
        """Initializes the circuit with a name and empty dictionaries for components."""
        self.name = name
        self.buses = {}  # Stores Bus objects
        self.transformers = {}  # Stores Transformer objects
        self.transmission_lines = {}  # Stores TransmissionLine objects
        self.y_bus = [[0 for _ in range(7)] for _ in range(7)] # Method 1: Not using pandas.
        #self.y_bus2 = pd.DataFrame([[0 for _ in range(7)] for _ in range(7)], columns = list('1234567'), index = list('1234567')) # Method 2: Using pandas.
        self.calc_ybus()

    def add_bus(self, bus):
        """Adds a bus object to the circuit. Raises an error if the bus already exists."""
        if bus.name in self.buses:
            raise ValueError(f"Bus '{bus.name}' already exists in the circuit.")
        self.buses[bus.name] = bus

    def add_transformer(self, transformer):
        """Adds a transformer object to the circuit. Raises an error if the transformer already exists."""
        if transformer.name in self.transformers:
            raise ValueError(f"Transformer '{transformer.name}' already exists in the circuit.")
        self.transformers[transformer.name] = transformer

    def add_transmission_line(self, transmission_line):
        """Adds a transmission line object to the circuit. Raises an error if the line already exists."""
        if transmission_line.name in self.transmission_lines:
            raise ValueError(f"Transmission Line '{transmission_line.name}' already exists in the circuit.")
        self.transmission_lines[transmission_line.name] = transmission_line


    def calc_ybus(self):
        """ Define Seven Bus System """
        # Define Buses
        bus1 = Bus("Bus 1", 20)
        bus2 = Bus("Bus 2", 230)
        bus3 = Bus("Bus 3", 230)
        bus4 = Bus("Bus 4", 230)
        bus5 = Bus("Bus 5", 230)
        bus6 = Bus("Bus 6", 230)
        bus7 = Bus("Bus 7", 18)

        # Add Buses to Circuit
        self.add_bus(bus1)
        self.add_bus(bus2)
        self.add_bus(bus3)
        self.add_bus(bus4)
        self.add_bus(bus5)
        self.add_bus(bus6)
        self.add_bus(bus7)

        # Define Transformers
        transformer1 = Transformer("T1", bus1, bus2, power_rating=125, impedance_percent=8.5, x_over_r_ratio=10,
                                   s_base=100)
        transformer2 = Transformer("T2", bus7, bus6, power_rating=200, impedance_percent=10.5, x_over_r_ratio=12,
                                   s_base=100)

        # Add Transformers to Circuit
        self.add_transformer(transformer1)
        self.add_transformer(transformer2)

        # Define Conductor & Bundle
        conductor = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)
        bundle = Bundle("Double", num_conductors=2, spacing=1.5, conductor=conductor)

        # Define Geometry
        geometry = Geometry("Standard_3Phase", xa=0, ya=0, xb=19.5, yb=0, xc=39, yc=0)
        # Define Transmission Lines
        L1 = TransmissionLine("L1", bus2, bus4, bundle, geometry, length=10, s_base=100, frequency=60)
        L2 = TransmissionLine("L2", bus2, bus3, bundle, geometry, length=25, s_base=100, frequency=60)
        L3 = TransmissionLine("L3", bus3, bus5, bundle, geometry, length=20, s_base=100, frequency=60)
        L4 = TransmissionLine("L4", bus4, bus6, bundle, geometry, length=20, s_base=100, frequency=60)
        L5 = TransmissionLine("L5", bus5, bus6, bundle, geometry, length=10, s_base=100, frequency=60)
        L6 = TransmissionLine("L6", bus4, bus5, bundle, geometry, length=35, s_base=100, frequency=60)

        # Add Transmission Lines to Circuit
        self.add_transmission_line(L1)
        self.add_transmission_line(L2)
        self.add_transmission_line(L3)
        self.add_transmission_line(L4)
        self.add_transmission_line(L5)
        self.add_transmission_line(L6)

        """ Method 1: Not using pandas. """
        # Extract pu admittance of Transformers
        y_pu_T1 = transformer1.y_pu_sys
        y_pu_T2 = transformer2.y_pu_sys

        # Extract pu admittance of Transmission lines
        y_pu_L1 = L1.y_pu_sys
        y_pu_L2 = L2.y_pu_sys
        y_pu_L3 = L3.y_pu_sys
        y_pu_L4 = L4.y_pu_sys
        y_pu_L5 = L5.y_pu_sys
        y_pu_L6 = L6.y_pu_sys

        self.y_bus[0][1] = -y_pu_T1
        self.y_bus[1][2] = -y_pu_L2
        self.y_bus[1][3] = -y_pu_L1
        self.y_bus[2][4] = -y_pu_L3
        self.y_bus[3][4] = -y_pu_L6
        self.y_bus[3][5] = -y_pu_L4
        self.y_bus[4][5] = -y_pu_L5
        self.y_bus[5][6] = -y_pu_T2

        for i in range(7):
            for j in range(i+1):
                if i != j:
                    self.y_bus[i][j] = self.y_bus[j][i]
        for i in range(7):
            self.y_bus[i][i] = -sum(self.y_bus[i][:])


        # """ Method 2: Using pandas. """
        # # Extract Yprim of Transformers
        # y_T1 = transformer1.yprim_pu
        # y_T2 = transformer2.yprim_pu
        #
        # # Extract Yprim of Transmission lines
        # y_L1 = L1.yprim_pu
        # y_L2 = L2.yprim_pu
        # y_L3 = L3.yprim_pu
        # y_L4 = L4.yprim_pu
        # y_L5 = L5.yprim_pu
        # y_L6 = L6.yprim_pu
        #
        # self.y_bus2.loc['1':'2', '1':'2'] += y_T1 # T1 connecting Bus 1 and Bus 2
        # self.y_bus2.loc['6':'7', '6':'7'] += y_T2 # T2 connecting Bus 6 and Bus 7
        # self.y_bus2.iat['2', '2'] += y_L1[0][0] # L1 connecting Bus 2 and Bus 4
        # self.y_bus2.iat['2', '4'] += y_L1[0][1]
        # self.y_bus2.iat['4', '2'] += y_L1[1][0]
        # self.y_bus2.iat['4', '4'] += y_L1[1][1]
        # self.y_bus2.loc['2':'3', '2':'3'] += y_L2 # L2 connecting Bus 2 and Bus 3
        # self.y_bus2.iat['3', '3'] += y_L3[0][0] # L3 connecting Bus 3 and Bus 5
        # self.y_bus2.iat['3', '5'] += y_L3[0][1]
        # self.y_bus2.iat['5', '3'] += y_L3[1][0]
        # self.y_bus2.iat['5', '5'] += y_L3[1][1]
        # self.y_bus2.iat['4', '4'] += y_L4[0][0] # L4 connecting Bus 4 and Bus 6
        # self.y_bus2.iat['4', '6'] += y_L4[0][1]
        # self.y_bus2.iat['6', '4'] += y_L4[1][0]
        # self.y_bus2.iat['6', '6'] += y_L4[1][1]
        # self.y_bus2.loc['5':'6', '5':'6'] += y_L5 # L5 connecting Bus 5 and Bus 6
        # self.y_bus2.loc['4':'5', '4':'5'] += y_L6 # L6 connecting Bus 4 and Bus 5

    def show_network(self):
        """Displays the network configuration."""
        print(f"\nCircuit Name: {self.name}")
        print("Buses:", list(self.buses.keys()))
        print("Transformers:", list(self.transformers.keys()))
        print("Transmission Lines:", list(self.transmission_lines.keys()))
        print("Ybus:")
        for row in self.y_bus:
            print(row)
        # print(self.y_bus2)

if __name__ == "__main__":
    my_circuit = Circuit("example circuit")
    my_circuit.show_network()