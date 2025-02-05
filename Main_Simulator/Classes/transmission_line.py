import math
from Classes.bus import Bus
from Classes.bundle import Bundle
from Classes.geometry import Geometry

class TransmissionLine:
    """Represents a high-voltage transmission line between two buses."""

    def __init__(self, name: str, bus1: Bus, bus2: Bus, bundle: Bundle, geometry: Geometry, length: float, frequency=60):
        """
        Initializes a TransmissionLine object.

        Parameters:
        - name (str): Name of the transmission line.
        - bus1 (Bus): First connected bus.
        - bus2 (Bus): Second connected bus.
        - bundle (Bundle): The Bundle object (providing DSL, DSC, resistance).
        - geometry (Geometry): The Geometry object (providing Deq).
        - length (float): Length of the transmission line in miles.
        - frequency (float, optional): Operating frequency in Hz (default = 60 Hz).
        """
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length
        self.frequency = frequency

        # Estimate S_base using Bus Voltage and Conductor Ampacity
        self.s_base = self.estimate_s_base()

        # Calculate base values
        self.z_base, self.y_base = self.calc_base_values()

        # Calculate electrical parameters
        self.r_series = self.calc_resistance()
        self.x_series = self.calc_reactance()
        self.b_shunt = self.calc_susceptance()
        self.y_series = self.calc_yseries()
        self.yprim = self.calc_yprim()

    def estimate_s_base(self):
        """Estimates base power using bus voltage and conductor ampacity."""
        v_base_kv = self.bus1.base_kv  # Base voltage in kV
        i_max = self.bundle.conductor.ampacity  # Maximum conductor ampacity in A

        if v_base_kv and i_max:
            return (math.sqrt(3) * v_base_kv * 1e3 * i_max) / 1e6  # Convert to MVA
        return 100  # Default if no data available

    def calc_base_values(self):
        """Calculates the base impedance and base admittance."""
        v_base_kv = self.bus1.base_kv  # Base voltage in kV
        v_base = v_base_kv * 1e3  # Convert kV to V
        z_base = (v_base ** 2) / (self.s_base * 1e6)  # Base impedance in ohms
        y_base = 1 / z_base if z_base != 0 else 0  # Base admittance in Siemens
        return z_base, y_base

    def calc_resistance(self):
        """Calculates the series resistance (Ω/mile)."""
        return self.bundle.conductor.resistance / self.bundle.num_conductors

    def calc_reactance(self):
        """Calculates the series reactance (Ω/mile)."""
        return (2 * math.pi * self.frequency * 2e-7 *
                math.log(self.geometry.Deq / self.bundle.DSL) * 1609.34)

    def calc_susceptance(self):
        """Calculates the shunt susceptance (S/mile)."""
        return (2 * math.pi * self.frequency *
                (2 * math.pi * 8.854e-12) /
                math.log(self.geometry.Deq / self.bundle.DSC) * 1609.34)

    def calc_yseries(self):
        """Calculates the series admittance."""
        z_series = complex(self.r_series, self.x_series)
        return 1 / z_series if z_series != 0 else complex(0, 0)

    def calc_yprim(self):
        """Calculates the Y-primitive matrix for the transmission line."""
        yprim = [
            [self.y_series + (self.b_shunt / 2) * 1j, -self.y_series],
            [-self.y_series, self.y_series + (self.b_shunt / 2) * 1j]
        ]
        return yprim

    def __repr__(self):
        """Returns a detailed string representation of the TransmissionLine object."""
        return (f"TransmissionLine(name='{self.name}', length={self.length} mi, "
                f"z_base={self.z_base:.4f} Ω, y_base={self.y_base:.6e} S, "
                f"r_series={self.r_series:.4f} Ω/mi, x_series={self.x_series:.4f} Ω/mi, "
                f"b_shunt={self.b_shunt:.6e} S/mi, y_series={self.y_series:.4f} S, "
                f"bus1='{self.bus1.name}', bus2='{self.bus2.name}')")



