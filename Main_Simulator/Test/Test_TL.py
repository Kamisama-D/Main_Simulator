import math
from Classes.bus import Bus
from Classes.conductor import Conductor
from Classes.bundle import Bundle
from Classes.geometry import Geometry
from Classes.transmission_line import TransmissionLine


def test_transmission_line_class():
    """Function to test the TransmissionLine class."""

    # Create bus instances (Voltage rating must be the same)
    bus1 = Bus("Bus 1", 230)  # 230 kV base voltage
    bus2 = Bus("Bus 2", 230)

    # Create conductor instance
    conductor1 = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)

    # Create bundle instance
    bundle1 = Bundle("Double", num_conductors=2, spacing=1.5, conductor=conductor1)

    # Create geometry instance
    geometry1 = Geometry("Standard_3Phase", xa=0, ya=0, xb=19.5, yb=0, xc=39, yc=0)

    # Define system base power (explicitly set instead of estimating)
    s_base = 100  # MVA
    f_base = 60  # Hz

    # Create transmission line instance
    line1 = TransmissionLine("Line 1", bus1, bus2, bundle1, geometry1, length=10, s_base=s_base, frequency=f_base)

    # Print transmission line details
    print("\n--- Transmission Line Details ---")
    print(f"Name: {line1.name}")
    print(f"Connected Buses: {line1.bus1.name} - {line1.bus2.name}")
    print(f"Length: {line1.length:.2f} mi")
    print(f"System Base Power: {line1.s_base:.2f} MVA")
    print(f"Operating Frequency: {line1.frequency} Hz")

    # Print base values
    print("\n--- Base Values ---")
    print(f"Z_base (System Base Impedance): {line1.z_base_sys:.4f} Ω")
    print(f"Y_base (System Base Admittance): {line1.y_base_sys:.4f} S")

    # Print impedance and admittance values
    print("\n--- Impedance & Admittance Values ---")
    print(f"Z_series (Total Impedance): {line1.z_series:.4f} Ω")
    print(f"Z_pu (Per-Unit Impedance): {line1.z_pu_sys:.4f} pu")
    print(f"Y_series (Total Admittance): {line1.y_series:.4f} S")
    print(f"Y_pu (Per-Unit Admittance): {line1.y_pu_sys:.4f} pu")
    print(f"B_shunt (Shunt Susceptance in Siemens): {line1.b_shunt:.4f} S")
    print(f"B_shunt_pu (Shunt Susceptance in PU): {line1.b_shunt_pu:.4f} pu")

    # Print Resistance and Reactance separately
    print("\n--- Resistance & Reactance Values ---")
    print(f"R_series: {line1.r_series:.4f} Ω")
    print(f"X_series: {line1.x_series:.4f} Ω")
    print(f"R_pu: {line1.z_pu_sys.real:.4f} pu")
    print(f"X_pu: {line1.z_pu_sys.imag:.4f} pu")

    # Print Y-Primitive Matrix (Siemens)
    print("\n--- Y-Primitive Matrix (Yprim) [Siemens] ---")
    print(line1.yprim)

    # Print Y-Primitive Matrix (Per Unit)
    print("\n--- Y-Primitive Matrix (Yprim_pu) [Per Unit] ---")
    print(line1.yprim_pu)

    # Assertions to verify correctness
    assert line1.bus1.base_kv == line1.bus2.base_kv, "Bus voltage ratings must match."
    assert abs(line1.s_base - s_base) < 1e-6, "Incorrect S_base calculation"

    expected_z_base = (bus1.base_kv * 1e3) ** 2 / (s_base * 1e6)
    expected_y_base = 1 / expected_z_base

    assert abs(line1.z_base_sys - expected_z_base) < 1e-6, "Incorrect Z_base calculation"
    assert abs(line1.y_base_sys - expected_y_base) < 1e-6, "Incorrect Y_base calculation"

    print("\n✅ All TransmissionLine class tests passed!")


if __name__ == "__main__":
    test_transmission_line_class()

