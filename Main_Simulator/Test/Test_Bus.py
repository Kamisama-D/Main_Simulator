# Import the Bus class from the bus module
from Classes.bus import Bus

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

if __name__ == "__main__":
    test_bus_class()


