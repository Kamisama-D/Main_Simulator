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
    bundle1 = Bundle("Double", num_conductors=2, spacing=10.0, conductor=conductor1)

    # Create geometry instance
    geometry1 = Geometry("Standard_3Phase", xa=0, ya=0, xb=5, yb=8, xc=10, yc=0)

    # Define system base power (explicitly set instead of estimating)
    s_base = 100  # MVA

    # Create transmission line instance
    line1 = TransmissionLine("Line 1", bus1, bus2, bundle1, geometry1, length=10, s_base=s_base)

    # Print transmission line details
    print(line1)

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

