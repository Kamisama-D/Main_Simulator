import numpy as np
import pandas as pd
from Classes.Circuit import Circuit


class DCPowerFlowSolver:
    """
    A simple DC power flow solver that uses the imaginary part of the Ybus matrix (susceptance matrix B).
    Assumes:
        - Flat voltage profile (1.0 p.u.)
        - Small angle differences (sin(δi - δj) ≈ δi - δj)
        - Negligible resistance (only susceptance is used)
    """

    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.buses = list(self.circuit.buses.keys())
        self.slack_bus = self.find_slack_bus()
        self.theta = None

    def find_slack_bus(self):
        for name, bus in self.circuit.buses.items():
            if bus.bus_type == "Slack Bus":
                return name
        raise ValueError("No Slack Bus defined in the circuit.")

    def build_B_matrix(self):
        Ybus = self.circuit.calc_ybus()
        B = np.imag(Ybus.values)
        idx = list(Ybus.index)

        # Remove slack bus row and column
        slack_idx = idx.index(self.slack_bus)
        B_prime = np.delete(B, slack_idx, axis=0)
        B_prime = np.delete(B_prime, slack_idx, axis=1)

        return B_prime, [bus for bus in idx if bus != self.slack_bus]

    def build_P_vector(self, bus_order):
        S_base = self.circuit.settings.base_power
        P = []
        for bus in bus_order:
            gen_P = self.circuit.get_bus_generation(bus)
            load_P = self.circuit.get_bus_load(bus)
            net_P = (gen_P - load_P) / S_base  # ✅ convert to per unit
            P.append(net_P)
        return np.array(P)



    def solve(self):
        print(">> Entered DCPowerFlowSolver.solve()")
        B, reduced_bus_order = self.build_B_matrix()
        P = self.build_P_vector(reduced_bus_order)

        # Display B matrix
        print("\n--- Susceptance Matrix B' (p.u.^-1) ---")
        B_df = pd.DataFrame(B, index=reduced_bus_order, columns=reduced_bus_order)
        print(B_df.round(4))

        # Display P vector
        print("\n--- Net Real Power Injection Vector P (p.u.) ---")
        for bus, p in zip(reduced_bus_order, P):
            print(f"{bus}: {p:.4f}")

        # Solve B * θ = P
        B_inv = np.linalg.inv(B)
        theta = np.matmul(-B_inv, P)

        # Insert slack angle (0.0) back into full vector
        full_theta = []
        for bus in self.buses:
            if bus == self.slack_bus:
                full_theta.append(0.0)
            else:
                idx = reduced_bus_order.index(bus)
                full_theta.append(theta[idx])

        self.theta = dict(zip(self.buses, full_theta))
        return self.theta

    def display_results(self):
        print("\n--- DC Power Flow Results (Voltage Angles in Degrees) ---")
        for bus, angle_rad in self.theta.items():
            angle_deg = np.degrees(angle_rad)
            print(f"{bus}: {angle_deg:.4f}°")
