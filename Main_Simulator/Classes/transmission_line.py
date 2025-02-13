import math
import cmath
from Classes.bus import Bus
from Classes.bundle import Bundle
from Classes.geometry import Geometry

class TransmissionLine:
    """Represents a high-voltage transmission line between two buses."""

    def __init__(self, name: str, bus1, bus2, bundle, geometry, length: float, s_base: float, frequency=float):
        """
        Initializes a TransmissionLine object.

        Parameters:
        - name (str): Name of the transmission line.
        - bus1 (Bus): First connected bus.
        - bus2 (Bus): Second connected bus.
        - bundle (Bundle): The Bundle object (providing DSL, DSC, resistance).
        - geometry (Geometry): The Geometry object (providing Deq).
        - length (float): Length of the transmission line in miles.
        - s_base (float): System base power in MVA.
        - frequency (float, optional): Operating frequency in Hz (default = 60 Hz).
        """

        # Validation that bus voltages have the same value
        if bus1.base_kv != bus2.base_kv:
            raise ValueError("Buses must have the same voltage rating.")

        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length
        self.frequency = frequency

        # Assign base values
        self.s_base = s_base
        self.v_base = bus1.base_kv

        # Calculate base values
        self.z_base_sys, self.y_base_sys = self.calc_base_values()

        # Calculate electrical parameters
        self.r_series = self.calc_resistance()
        self.x_series = self.calc_reactance()
        self.b_shunt = self.calc_bshunt()  # Shunt susceptance calculation
        self.z_series = complex(self.r_series, self.x_series)
        self.z_pu_sys = self.z_series / self.z_base_sys
        self.y_series = self.calc_yseries()  # Updated calculation for y_series
        self.y_pu_sys = 1 / self.z_pu_sys if self.z_pu_sys != 0 else complex(0, 0)
        self.b_shunt_pu = self.b_shunt / self.y_base_sys if self.y_base_sys != 0 else complex(0, 0)

        # Compute Y-primitive matrices
        self.yprim = self.calc_yprim()
        self.yprim_pu = self.calc_yprim_pu()

    def calc_base_values(self):
        """Calculates the base impedance and base admittance."""
        v_base = self.v_base * 1e3  # Convert kV to V
        z_base = (v_base ** 2) / (self.s_base * 1e6)  # Base impedance in ohms
        y_base = 1 / z_base if z_base != 0 else 0  # Base admittance in Siemens
        return z_base, y_base

    def calc_resistance(self):
        """Calculates the series resistance (Ω)."""
        return (self.bundle.conductor.resistance / self.bundle.num_conductors) * self.length

    def calc_reactance(self):
        """Calculates the series reactance (Ω)."""
        return (2 * math.pi * self.frequency * 2e-7 *
                math.log(self.geometry.Deq / self.bundle.DSL) * 1609.34 * self.length)

    def calc_bshunt(self):
        """Calculates the shunt susceptance (B_shunt) in Siemens."""
        return ((2 * math.pi * self.frequency * (2 * math.pi * 8.854e-12)) /
                math.log(self.geometry.Deq / self.bundle.DSC) * 1609.34 * self.length)

    def calc_yseries(self):
        """Calculates the series admittance (Y_series)."""
        return 1 / self.z_series if self.z_series != 0 else complex(0, 0)

    def calc_yprim(self):
        """Calculates the Y-primitive matrix for the transmission line."""
        return [
            [self.y_series + (1j * self.b_shunt / 2), -self.y_series],
            [-self.y_series, self.y_series + (1j * self.b_shunt / 2)]
        ]

    def calc_yprim_pu(self):
        """Calculates the Y-primitive matrix in per-unit."""
        return [
            [self.y_pu_sys + (1j * self.b_shunt_pu / 2), -self.y_pu_sys],
            [-self.y_pu_sys, self.y_pu_sys + (1j * self.b_shunt_pu / 2)]
        ]

    def __repr__(self):
        """Returns a detailed string representation of the TransmissionLine object."""
        return (f"""
                    --- Transmission Line Details ---
                    Name: {self.name}
                    Buses: {self.bus1.name} - {self.bus2.name}
                    Bundle: {self.bundle}
                    Geometry: {self.geometry}
                    Length: {self.length} mi
                    Frequency: {self.frequency} Hz

                    --- Base Values ---
                    s_base: {self.s_base} MVA
                    v_base: {self.v_base} kV
                    z_base_sys: {self.z_base_sys:.4f} Ω
                    
                     --- Resistance and Reactance Values ---
                    r_series: {abs(self.r_series):.4f} Ω
                    r_series_pu: {abs(self.z_pu_sys.real):.4f} pu
                    x_series: {abs(self.x_series):.4f} Ω
                    x_series_pu: {abs(self.z_pu_sys.imag):.4f} pu

                    --- Impedance and Admittance Values ---
                    z_series: {abs(self.z_series):.4f} Ω
                    z_pu_sys: {abs(self.z_pu_sys):.4f} pu
                    y_series: {abs(self.y_series):.4f} S
                    y_pu_sys: {abs(self.y_pu_sys):.4f} pu
                    b_shunt: {abs(self.b_shunt):.4f} S
                    b_shunt_pu: {abs(self.b_shunt_pu):.4f} pu
                   
                    --- Y-Primitive Matrix (Yprim) [Siemens] ---
                    [{self.yprim[0][0]:.4f}, {self.yprim[0][1]:.4f}]
                    [{self.yprim[1][0]:.4f}, {self.yprim[1][1]:.4f}]

                    --- Y-Primitive Matrix (Yprim_pu) [Per Unit] ---
                    [{self.yprim_pu[0][0]:.4f}, {self.yprim_pu[0][1]:.4f}]
                    [{self.yprim_pu[1][0]:.4f}, {self.yprim_pu[1][1]:.4f}]
                """)



