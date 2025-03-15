import numpy as np
from Classes.bus import Bus
from Classes.generator import Generator
from Classes.load import Load
from Classes.system_setting import SystemSettings


def test_power_system():
    print("\n=== Initializing Test Buses ===")

    # Define Test Buses
    slack_bus = Bus("Bus 1", base_kv=230, bus_type="Slack Bus")
    pv_bus = Bus("Bus 2", base_kv=230, bus_type="PV Bus", P=100)
    pq_bus = Bus("Bus 3", base_kv=230, bus_type="PQ Bus", P=50, Q=30)

    # Display Bus Information
    print(slack_bus)
    print(pv_bus)
    print(pq_bus)

    print("\n=== Initializing Generators and Loads ===")
    gen1 = Generator(bus=slack_bus, P=150)
    gen2 = Generator(bus=pv_bus, P=100)
    load1 = Load(bus=pq_bus, P=50, Q=30)

    print(gen1)
    print(gen2)
    print(load1)

    print("\n=== Defining Ybus Matrix ===")
    Ybus = np.array([
        [10 - 5j, -5 + 2j, -5 + 3j],
        [-5 + 2j, 10 - 6j, -5 + 4j],
        [-5 + 3j, -5 + 4j, 10 - 7j]
    ])

    settings = SystemSettings(Ybus)

    print("\n=== Assigning Voltage Magnitudes (Except PQ Bus) ===")
    voltages = np.array([
        1.0 + 0j,  # Slack Bus (V=1 p.u.)
        1.02 + 0j,  # PV Bus (Voltage Set)
        None  # PQ Bus (To be calculated)
    ])

    print("\n=== Computing Power Injections ===")
    P_slack, Q_slack = settings.compute_power_injection(slack_bus, voltages)
    _, Q_pv = settings.compute_power_injection(pv_bus, voltages)
    V_pq, delta_pq = settings.compute_voltage_angle(pq_bus, voltages)  # Compute PQ bus values

    pq_bus.vpu = V_pq
    pq_bus.delta = delta_pq

    print(f"\nSlack Bus: P={P_slack}, Q={Q_slack}")
    print(f"PV Bus: Q={Q_pv}, Delta={pv_bus.delta}")
    print(f"PQ Bus: V={pq_bus.vpu}, Delta={pq_bus.delta}")

    print("\n=== Test Completed Successfully ===")


if __name__ == "__main__":
    test_power_system()






