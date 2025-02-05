import math
from Classes.bus import Bus
from Classes.conductor import Conductor
from Classes.bundle import Bundle
from Classes.geometry import Geometry
from Classes.transmission_line import TransmissionLine

def test_transmission_line_class():
    """Function to test the TransmissionLine class with voltage and ampacity-based S_base."""

    # Create bus instances
    bus1 = Bus("Bus 1", 230)  # 230 kV base voltage
    bus2 = Bus("Bus 2", 230)

    # Create conductor instance
    conductor1 = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)

    # Create bundle instance
    bundle1 = Bundle("Double", num_conductors=2, spacing=10.0, conductor=conductor1)

    # Create geometry instance
    geometry1 = Geometry("Standard_3Phase", xa=0, ya=0, xb=5, yb=8, xc=10, yc=0)

    # Create transmission line instance (S_base will be estimated from Bus Voltage & Ampacity)
    line1 = TransmissionLine("Line 1", bus1, bus2, bundle1, geometry1, length=10)

    # Print transmission line details
    print("\n--- Transmission Line Details ---")
    print(line1)

    # Print base values
    print(f"\nBase Power (S_base): {line1.s_base:.2f} MVA")
    print(f"Base Impedance (Z_base): {line1.z_base:.4f} Ω")
    print(f"Base Admittance (Y_base): {line1.y_base:.6e} S")

    # Print admittance matrix
    print("\n--- Y-Primitive Matrix (Yprim) ---")
    for row in line1.yprim:
        print([f"{elem:.4f}" for elem in row])  # Formatting values

    # Expected calculations for verification
    expected_s_base = (math.sqrt(3) * bus1.base_kv * 1e3 * conductor1.ampacity) / 1e6  # MVA
    expected_z_base = (bus1.base_kv * 1e3) ** 2 / (expected_s_base * 1e6)
    expected_y_base = 1 / expected_z_base

    # Assertions to verify correctness
    assert abs(line1.s_base - expected_s_base) < 1e-6, "Incorrect S_base calculation"
    assert abs(line1.z_base - expected_z_base) < 1e-6, "Incorrect Z_base calculation"
    assert abs(line1.y_base - expected_y_base) < 1e-6, "Incorrect Y_base calculation"

    print("\n✅ All TransmissionLine class tests passed!")

if __name__ == "__main__":
    test_transmission_line_class()

