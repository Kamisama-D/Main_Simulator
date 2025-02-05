import cmath
import math


class Transformer:
    """Represents a transformer in a power system network."""

    def __init__(self, name: str, bus1, bus2, power_rating: float, impedance_percent: float, x_over_r_ratio: float):
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

        # Calculate impedance and admittance
        self.zt = self.calc_impedance()
        self.yt = self.calc_admittance()
        self.yprim = self.calc_yprim()

    def calc_impedance(self):
        """Calculates the transformer's impedance using per-unit system."""
        z_base = (self.bus1.base_kv ** 2) / self.power_rating  # Base impedance in ohms
        z_pu = self.impedance_percent / 100  # Per-unit impedance magnitude

        # Compute angle from X/R ratio
        theta = math.atan(self.x_over_r_ratio)  # Angle in radians

        # Convert to complex form
        z_pu_complex = z_pu * cmath.exp(complex(0, theta))  # Using Euler's formula

        # Convert to ohms
        zt = z_pu_complex * z_base
        return zt

    def calc_admittance(self):
        """Calculates the transformer's admittance (1/Z)."""
        return 1 / self.zt if self.zt != 0 else complex(0, 0)

    def calc_yprim(self):
        """
        Calculates the transformer's Y-primitive matrix.
        This is a 2x2 matrix representing the transformer in admittance form.
        """
        yprim = [
            [self.yt, -self.yt],
            [-self.yt, self.yt]
        ]
        return yprim

    def __repr__(self):
        """Returns a string representation of the Transformer object."""
        return (f"Transformer(name='{self.name}', bus1='{self.bus1.name}', bus2='{self.bus2.name}', "
                f"power_rating={self.power_rating} MVA, impedance_percent={self.impedance_percent}%, "
                f"x_over_r_ratio={self.x_over_r_ratio}, "
                f"zt={self.zt:.4f} Ω, yt={self.yt:.4f} S)")




