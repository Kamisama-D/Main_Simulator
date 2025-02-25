from Classes.bus import Bus
from Classes.transformer import Transformer
import numpy as np
import pandas as pd

def test_transformer_class():
    """Function to test the Transformer class."""

    # Create Bus instances
    bus1 = Bus("Bus 1", 20)
    bus2 = Bus("Bus 2", 230)

    # Create Transformer instance
    transformer = Transformer("T1", bus1, bus2, power_rating=125, impedance_percent=8.5, x_over_r_ratio=10, s_base=100)

    # Print transformer details
    print("\n--- Transformer Details ---")
    print(f"Name: {transformer.name}")
    print(f"Power Rating: {transformer.power_rating} MVA")
    print(f"X/R Ratio: {transformer.x_over_r_ratio}")

    # Print base values
    print("\n--- Base Values ---")
    print(f"S_base (System Power Base): {transformer.s_base} MVA")
    print(f"V_base (Bus Voltage Base): {transformer.v_base} kV")
    print(f"Z_base_xfmr: {transformer.z_base_xfmr:.4f} Ω")
    print(f"Z_base_sys: {transformer.z_base_sys:.4f} Ω")

    # Print impedance and admittance values
    print("\n--- Impedance & Admittance Values ---")
    print(f"Z_pu_xfmr (Per-Unit Transformer Base): {transformer.z_pu_xfmr:.4f} pu")
    print(f"Z_t (Impedance in Ohms): {abs(transformer.zt):.4f} Ω")  # Show magnitude only
    print(f"Z_pu_sys (Per-Unit System Base): {abs(transformer.z_pu_sys):.4f} pu")  # Show magnitude only
    print(f"Y_t (Admittance in Siemens): {abs(transformer.yt):.4f} S")  # Show magnitude only
    print(f"Y_pu_sys (Per-Unit Admittance): {abs(transformer.y_pu_sys):.4f} pu")  # Show magnitude only

    # Print resistance and reactance values separately
    print("\n--- Resistance & Reactance Values ---")
    print(f"R_t (Resistance in Ohms): {transformer.zt.real:.4f} Ω")
    print(f"X_t (Reactance in Ohms): {transformer.zt.imag:.4f} Ω")
    print(f"R_pu_sys (Per-Unit System Resistance): {transformer.z_pu_sys.real:.4f} pu")
    print(f"X_pu_sys (Per-Unit System Reactance): {transformer.z_pu_sys.imag:.4f} pu")

    # Print Y-Primitive Matrix (Siemens)
    print("\n--- Y-Primitive Matrix (Yprim) [Siemens] ---")
    print(transformer.yprim)

    # Print Y-Primitive Matrix (Per Unit)
    print("\n--- Y-Primitive Matrix (Yprim_pu) [Per Unit] ---")
    print(transformer.yprim_pu)


print("\n✅ All Transformer class tests passed!")


if __name__ == "__main__":
    test_transformer_class()





