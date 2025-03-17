from Classes.bus import Bus
from Classes.generator import Generator

def test_generator_class():
    """Function to test the Generator class with detailed output."""

    print("\n=== Test 1: Slack Bus with Generator ===")
    # 1. Test with Slack Bus
    slack_bus = Bus("Slack Bus", 230, 'Slack Bus')
    gen_slack = Generator("Gen Slack", slack_bus, voltage_setpoint=1.05, mw_setpoint=100)
    print(slack_bus)
    print(gen_slack)
    assert slack_bus.bus_type == "Slack Bus", "Slack Bus type should remain Slack"
    assert slack_bus.P is None, "Slack Bus P should be calculated during power flow"
    assert slack_bus.Q is None, "Slack Bus Q should be calculated during power flow"
    print("[PASS] Slack Bus with Generator Test Passed.\n")

    print("=== Test 2: Single PV Bus with Generator ===")
    # 2. Test with PV Bus (Single Generator)
    bus2 = Bus("Bus 2", 230, 'PQ Bus', P=50, Q=30)
    gen2 = Generator("Gen 2", bus2, voltage_setpoint=1.02, mw_setpoint=80)
    print(bus2)
    print(gen2)
    assert bus2.bus_type == "PV Bus", "Bus 2 should be set to PV Bus by the Generator"
    assert bus2.P == 80, "Bus 2 P should be set by the Generator's mw_setpoint"
    assert bus2.vpu == 1.02, "Bus 2 vpu should be set to Generator's voltage_setpoint"

    # Simulate Q calculation for PV Bus
    gen2.Q = 25  # Simulate power flow calculation for Q
    bus2.Q = gen2.Q  # Update the bus's Q value
    print(bus2)
    assert bus2.Q == 25, "PV Bus Q should be updated by the Generator"
    print("[PASS] Single PV Bus with Generator Test Passed.\n")

    print("=== Test 3: Multiple Generators on One Bus ===")
    # 3. Test with Multiple Generators on One Bus
    bus3 = Bus("Bus 3", 500, 'PQ Bus', P=20, Q=15)
    gen3a = Generator("Gen 3A", bus3, voltage_setpoint=1.01, mw_setpoint=60)
    gen3b = Generator("Gen 3B", bus3, voltage_setpoint=1.01, mw_setpoint=40)
    print(bus3)
    print(gen3a)
    print(gen3b)
    assert bus3.bus_type == "PV Bus", "Bus 3 should be set to PV Bus by the Generators"
    assert bus3.P == 100, "Bus 3 P should be the sum of all connected Generators"

    # Simulate Q calculation and accumulation
    gen3a.Q = 15
    gen3b.Q = 20
    bus3.Q = gen3a.Q + gen3b.Q
    print(bus3)
    assert bus3.Q == 35, "Bus 3 Q should be the sum of Q from all connected Generators"
    print("[PASS] Multiple Generators on One Bus Test Passed.\n")

    print("=== Test 4: PV to PQ Switching (Q Limits Exceeded) ===")
    # 4. Test PV to PQ Switching (Integration with Bus Class)
    bus4 = Bus("Bus 4", 230, 'PQ Bus', P=50, Q=20)
    gen4 = Generator("Gen 4", bus4, voltage_setpoint=1.03, mw_setpoint=70)
    print(bus4)
    print(gen4)
    assert bus4.bus_type == "PV Bus", "Bus 4 should be set to PV Bus by the Generator"

    # Simulate Q exceeding Q_max
    gen4.Q = 50  # Exceeds Q_max (0.4 * mw_setpoint = 28)
    bus4.Q = gen4.Q  # Update the bus's Q value
    bus4.check_reactive_limits()  # Should switch to PQ
    print(bus4)
    assert bus4.Q == 28.0, "Bus 4 Q should be limited to Q_max"
    assert bus4.bus_type == "PQ Bus", "Bus 4 should switch to PQ if Q exceeds limits"
    print("[PASS] PV to PQ Switching Test Passed.\n")

    print("=== All Generator Class Tests Passed! ===")

if __name__ == "__main__":
    test_generator_class()
