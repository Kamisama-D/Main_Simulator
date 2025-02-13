import cmath
import math

class Transformer:
    """Represents a transformer in a power system network."""

    def __init__(self, name: str, bus1, bus2, power_rating: float, impedance_percent: float, x_over_r_ratio: float, s_base: float):
        """
        Initializes a Transformer object.

        Parameters:
        - name (str): The name of the transformer.
        - bus1 (Bus): The first bus connected to the transformer.
        - bus2 (Bus): The second bus connected to the transformer.
        - power_rating (float): Transformer power rating in MVA.
        - impedance_percent (float): Transformer impedance as a percentage.
        - x_over_r_ratio (float): Transformer X/R ratio.
        """
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating  # In MVA
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio

        # Assign base values
        self.s_base = s_base  # System base power
        self.v_base = bus1.base_kv  # Use bus voltage as base voltage

        # Compute base impedances
        self.z_base_xfmr = self.calc_base_impedance_xfmr()
        self.z_base_sys = self.calc_base_impedance_sys()

        # Compute per-unit impedance on transformer base
        self.z_pu_xfmr = self.calc_pu_impedance_xfmr()

        # Compute impedance in ohms using Euler's formula
        self.zt = self.calc_impedance()

        # Compute per-unit impedance on system base
        self.z_pu_sys = self.calc_pu_impedance_sys()

        # Compute admittances
        self.yt = self.calc_admittance()
        self.y_pu_sys = self.calc_pu_admittance_sys()

        # Compute resistance and reactance
        self.rt = self.zt.real
        self.xt = self.zt.imag
        self.r_pu_sys = self.z_pu_sys.real
        self.x_pu_sys = self.z_pu_sys.imag

        # Compute Y-primitive matrices
        self.yprim = self.calc_yprim()
        self.yprim_pu = self.calc_yprim_pu()

    def calc_base_impedance_xfmr(self):
        """Calculates the base impedance for the transformer rating."""
        return (self.v_base ** 2) / self.power_rating

    def calc_base_impedance_sys(self):
        """Calculates the base impedance for the system."""
        return (self.v_base ** 2) / self.s_base

    def calc_pu_impedance_xfmr(self):
        """Calculates the transformer's per-unit impedance based on its rating."""
        return self.impedance_percent / 100

    def calc_impedance(self):
        """Calculates the transformer's impedance in ohms using Euler's formula."""
        theta = math.atan(self.x_over_r_ratio)  # Compute angle from X/R ratio
        z_pu_complex = self.z_pu_xfmr * cmath.exp(complex(0, theta))  # Euler’s formula
        return z_pu_complex * self.z_base_xfmr  # Convert to ohms

    def calc_pu_impedance_sys(self):
        """Calculates the transformer's per-unit impedance on the system base."""
        return self.zt / self.z_base_sys  # Uses the complex value of zt

    def calc_admittance(self):
        """Calculates the transformer's admittance in siemens."""
        return 1 / self.zt if abs(self.zt) > 1e-9 else complex(0, 0)

    def calc_pu_admittance_sys(self):
        """Calculates the transformer's per-unit admittance on the system base."""
        return 1 / self.z_pu_sys if abs(self.z_pu_sys) > 1e-9 else complex(0, 0)

    def calc_yprim(self):
        """Calculates the Y-primitive matrix in siemens."""
        return [
            [self.yt, -self.yt],
            [-self.yt, self.yt]
        ]

    def calc_yprim_pu(self):
        """Calculates the Y-primitive matrix in per-unit."""
        return [
            [self.y_pu_sys, -self.y_pu_sys],
            [-self.y_pu_sys, self.y_pu_sys]
        ]

    def __repr__(self):
        """Returns a string representation of the Transformer object with magnitudes only."""
        return (
            f"--- Transformer Details ---\n"
            f"Name: {self.name}\n"
            f"Power Rating: {self.power_rating} MVA\n"
            f"X/R Ratio: {self.x_over_r_ratio}\n\n"

            f"--- Base Values ---\n"
            f"S_base (System Power Base): {self.s_base} MVA\n"
            f"V_base (Bus Voltage Base): {self.v_base} kV\n"
            f"Z_base_xfmr: {self.z_base_xfmr:.4f} Ω\n"
            f"Z_base_sys: {self.z_base_sys:.4f} Ω\n\n"
            
             f"--- Impedance & Admittance Values ---\n"
            f"Z_pu_xfmr (Per-Unit Transformer Base): {abs(self.z_pu_xfmr):.4f} pu\n"
            f"Z_t (Impedance in Ohms): {abs(self.zt):.4f} Ω\n"
            f"Z_pu_sys (Per-Unit System Base): {abs(self.z_pu_sys):.4f} pu\n"
            f"Y_t (Admittance in Siemens): {abs(self.yt):.4f} S\n"
            f"Y_pu_sys (Per-Unit Admittance): {abs(self.y_pu_sys):.4f} pu\n\n"

            f"--- Resistance & Reactance Values ---\n"
            f"R_t (Resistance in Ohms): {self.rt:.4f} Ω\n"
            f"X_t (Reactance in Ohms): {self.xt:.4f} Ω\n"
            f"R_pu_sys (Per-Unit System Resistance): {abs(self.r_pu_sys):.4f} pu\n"
            f"X_pu_sys (Per-Unit System Reactance): {abs(self.x_pu_sys):.4f} pu\n\n"
         
            f"--- Y-Primitive Matrix (Yprim) [Siemens] ---\n"
            f"[{abs(self.yprim[0][0]):.4f}, {abs(self.yprim[0][1]):.4f}]\n"
            f"[{abs(self.yprim[1][0]):.4f}, {abs(self.yprim[1][1]):.4f}]\n\n"

            f"--- Y-Primitive Matrix (Yprim_pu) [Per Unit] ---\n"
            f"[{abs(self.yprim_pu[0][0]):.4f}, {abs(self.yprim_pu[0][1]):.4f}]\n"
            f"[{abs(self.yprim_pu[1][0]):.4f}, {abs(self.yprim_pu[1][1]):.4f}]\n"
        )



