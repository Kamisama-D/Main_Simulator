from Classes.bus import Bus
from Classes.system_setting import Settings
import numpy as np
import pandas as pd

def test_bus_class():
    """Function to test the Bus class."""

    # Test Slack Bus
    bus1 = Bus("Bus 1", 20, 'Slack Bus')
    print(bus1)
    assert bus1.P is None, "Slack Bus P should be None (Not Calculated)"
    assert bus1.Q is None, "Slack Bus Q should be None (Not Calculated)"
    assert bus1.bus_type == "Slack Bus", "Bus 1 should be a Slack Bus"
    assert bus1.vpu == 1.0, "Slack Bus vpu should be 1.0"
    assert bus1.delta == 0.0, "Slack Bus delta should be 0.0"

    # Test PQ Bus
    bus2 = Bus("Bus 2", 230, 'PQ Bus', P=50, Q=30)
    print(bus2)
    assert bus2.P == 50, "PQ Bus P should be 50 as input"
    assert bus2.Q == 30, "PQ Bus Q should be 30 as input"
    assert bus2.bus_type == "PQ Bus", "Bus 2 should be a PQ Bus"
    assert bus2.vpu == 1.0, "PQ Bus initial vpu should be 1.0 (default)"
    assert bus2.delta == 0.0, "PQ Bus initial delta should be 0.0 (default)"

    # Simulate voltage and angle calculation for PQ Bus (as done in power flow solver)
    bus2.vpu = 0.98  # Example of calculated vpu
    bus2.delta = -5.0  # Example of calculated delta
    print(bus2)
    assert bus2.vpu == 0.98, "PQ Bus vpu should be calculated during power flow"
    assert bus2.delta == -5.0, "PQ Bus delta should be calculated during power flow"

    # Test PV Bus
    bus3 = Bus("Bus 3", 500, 'PV Bus', P=100)
    print(bus3)
    assert bus3.P == 100, "PV Bus P should be 100 as input"
    assert bus3.Q is None, "PV Bus Q should be None (Not Calculated)"
    assert bus3.bus_type == "PV Bus", "Bus 3 should be a PV Bus"
    assert bus3.Q_min == -40.0, "PV Bus Q_min should be -40.0"
    assert bus3.Q_max == 40.0, "PV Bus Q_max should be 40.0"

    # Simulate Q calculation for PV Bus (as done in power flow solver)
    bus3.Q = 35  # Example of calculated Q within limits
    print(bus3)
    assert bus3.Q == 35, "PV Bus Q should be calculated during power flow"
    assert bus3.bus_type == "PV Bus", "Bus 3 should remain PV Bus within Q limits"

    # Test reactive power limits for PV Bus
    bus3.Q = 50  # Exceeds Q_max (40)
    bus3.check_reactive_limits()  # Should switch to PQ and set Q to Q_max
    print(bus3)
    assert bus3.Q == 40.0, "Q should be limited to Q_max for PV Bus"
    assert bus3.bus_type == "PQ Bus", "PV Bus should switch to PQ if Q exceeds limits"

    # Test switching back to PV Bus (should not happen automatically)
    bus3.bus_type = "PV Bus"  # Manually switch back to PV for testing
    bus3.Q = -50  # Below Q_min (-40)
    bus3.check_reactive_limits()  # Should switch to PQ and set Q to Q_min
    print(bus3)
    assert bus3.Q == -40.0, "Q should be limited to Q_min for PV Bus"
    assert bus3.bus_type == "PQ Bus", "PV Bus should switch to PQ if Q below limits"

    # Verify unique indices
    assert bus1.index == 0, "Bus 1 index should be 0"
    assert bus2.index == 1, "Bus 2 index should be 1"
    assert bus3.index == 2, "Bus 3 index should be 2"

    # Verify the total bus count
    print(f"Total buses created: {Bus.count}")  # Expected: 3
    assert Bus.count == 3, "Bus count should be 3"

    print("All Bus class tests passed!")

def test_power_mismatch():
    # Reset Bus static variables to allow creation of new buses without conflicts.
    Bus.count = 0
    Bus.slack_assigned = False

    # Create three buses: one Slack, one PQ bus, and one PV bus.
    bus_slack = Bus("Slack Bus", 230, 'Slack Bus')
    bus_pq = Bus("PQ Bus", 230, 'PQ Bus', P=100, Q=50)
    bus_pv = Bus("PV Bus", 230, 'PV Bus', P=150)

    # Construct a simple Ybus matrix for a 3-bus system.
    bus_names = [bus_slack.name, bus_pq.name, bus_pv.name]
    Ybus = pd.DataFrame([[0+0j, 0+0j, 0+0j],
                         [0+0j, 0+0j, 0+0j],
                         [0+0j, 0+0j, 0+0j]],
                        index=bus_names, columns=bus_names)

    # Define the voltage dictionary as (magnitude, angle_in_degrees)
    voltages = {bus_slack.name: (1.0, 0.0),
                bus_pq.name: (1.0, 0.0),
                bus_pv.name: (1.0, 0.0)}

    settings = Settings()
    mismatch = settings.compute_power_mismatch([bus_slack, bus_pq, bus_pv], Ybus, voltages)

    # Expected mismatch: ΔP = 100, ΔQ = 50.
    expected_mismatch = np.array([100, 150, 50])

    print("Computed mismatch:", mismatch)
    print("Expected mismatch:", expected_mismatch)
    assert np.allclose(mismatch, expected_mismatch), "Mismatch values do not match expected values."
    print("Power mismatch test passed!")

if __name__ == "__main__":
    test_bus_class()
    test_power_mismatch()

