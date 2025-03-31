import numpy as np
from Classes.bus import Bus
from Classes.system_setting import SystemSettings
from Classes.PowerFlowSolver import PowerFlowSolver


def test_power_flow_solver():
    print("\n=== Initializing Test Buses ===")

    # Define buses with inputs
    slack_bus = Bus("Bus 1", base_kv=230, vpu=1.0, delta=0.0)  # Slack Bus
    pv_bus = Bus("Bus 2", base_kv=230, P=100, vpu=1.02)  # PV Bus
    pq_bus = Bus("Bus 3", base_kv=230, P=50, Q=30)  # PQ Bus

    # Create bus list
    bus_list = [slack_bus, pv_bus, pq_bus]

    # Display bus classification results
    print("\n=== Bus Classification Results ===")
    for bus in bus_list:
        print(bus)

    # Define the Ybus admittance matrix (example for a 3-bus system)
    Ybus = np.array([
        [-(-5 + 2j) - (-5 + 3j), -5 + 2j, -5 + 3j],
        [-5 + 2j, -(-5 + 2j) - (-3 + 2j), -3 + 2j],
        [-5 + 3j, -3 + 2j, -(-5 + 3j) - (-3 + 2j)]
    ])

    print("\n=== Defining Ybus Matrix ===")
    print(Ybus)

    print(f"Determinant of Ybus: {np.linalg.det(Ybus)}")

    # Initialize SystemSettings with Ybus and buses
    settings = SystemSettings(Ybus, bus_list)

    # Initialize PowerFlowSolver
    solver = PowerFlowSolver(settings)

    print("\n=== Running Power Flow Solver ===")

    # Run power flow calculations
    success = solver.solve_power_flow()

    # Display results
    if success:
        print("\n=== Final Bus Voltages & Power Injections ===")
        for bus in bus_list:
            print(bus)
    else:
        print("[ERROR] Power flow solution did not converge.")


if __name__ == "__main__":
    test_power_flow_solver()


