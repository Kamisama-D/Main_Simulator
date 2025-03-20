import numpy as np
import pandas as pd

from Classes.Circuit import Circuit
from system_setting import SystemSettings


class PowerFlowSolver:
    def __init__(self, solver: int, circuit, do_one_iteration: bool = False):
        self.solver = solver
        self.Circuit = circuit

        # Debugging bus type classification
        print("\n[DEBUG] Bus Type Classification (Before Fix):")
        for bus in self.Circuit.bus_order():
            print(f"  {bus}: {self.Circuit.bus_type[bus]}")

        self.flat_start()

        # Solve Method
        self.initialize_x()
        self.y = self.initialize_y()

        #Real Power
        Px = self.calc_Px()


        #Reactive Power
        Qx = self.calc_Qx()


        #Mistmatch
        self.yx = self.calculate_yx()
        self.del_y = self.calculate_power_mismatch(self.y,self.yx)


        # Compute Jacobian for first iteration
        self.J1 = self.calculate_J1()
        self.J2 = self.calculate_J2()
        self.J3 = self.calculate_J3()
        self.J4 = self.calculate_J4()
        self.J = self.construct_jacobian(self.J1, self.J2, self.J3, self.J4)

        #Change in the angle and voltage
        self.update_angles_voltages()

    def flat_start(self):
        """Initializes flat start with delta=0 and voltage=1 p.u."""
        self.delta = {bus: 0 for bus in self.Circuit.bus_order()}
        self.voltage = {bus: 1 for bus in self.Circuit.bus_order()}

    def initialize_x(self):
        """Constructs state variable vector x (delta and voltage magnitudes)."""
        delta_vector = [
            self.delta[bus] for bus in self.Circuit.bus_order()
            if self.Circuit.bus_type[bus] != 'Slack Bus'
        ]  # Excludes δ1 (Slack Bus)

        voltage_vector = [
            self.voltage[bus] for bus in self.Circuit.bus_order()
            if self.Circuit.bus_type[bus] not in ['Slack Bus', 'PV Bus']
        ]  # Excludes V1 (Slack Bus) and V7 (PV bus)

        x = np.array(delta_vector + voltage_vector, dtype=float).reshape(-1, 1)

        # Debugging output
        print(f"[DEBUG] x initialized with shape {x.shape}")

        return x

    def initialize_y(self):
        """Initializes y vector by extracting per-unit real and reactive power values, excluding Slack and PV buses."""

        # Extract per-unit real and reactive power values
        real_power_vector = np.array(list(self.Circuit.real_power_vector().values()), dtype=float) / float(
            self.Circuit.get_base_power())
        reactive_power_vector = np.array(list(self.Circuit.reactive_power_vector().values()), dtype=float) / float(
            self.Circuit.get_base_power())

        # Initialize y vectors
        y_real = []
        y_reactive = []

        # Collect real power values for non-slack buses (excluding P1)
        for bus in self.Circuit.bus_order():
            if self.Circuit.bus_type[bus] != "Slack Bus":  # Exclude Slack bus (P1)
                y_real.append(real_power_vector[self.Circuit.bus_order().index(bus)])

        # Collect reactive power values for PQ buses (excluding Q1, Q7)
        for bus in self.Circuit.bus_order():
            if self.Circuit.bus_type[bus] not in ["Slack Bus", "PV Bus"]:  # Exclude Slack and PV buses
                y_reactive.append(reactive_power_vector[self.Circuit.bus_order().index(bus)])

        # Convert lists to NumPy array with correct shape (11, 1)
        y = np.array(y_real + y_reactive, dtype=float).reshape(-1, 1)

        print(f"DEBUG: y initialized with shape {y.shape}")  # Debugging print
        return y

    def calculate_yx(self):
        """
        Calculates expected power injections yx (P and Q) using Ybus and voltage values,
        excluding P1, Q1, and Q7.
        """
        # Compute voltage vector
        V = np.array([self.voltage[bus] * np.exp(1j * self.delta[bus]) for bus in self.Circuit.bus_order()])

        # Convert Ybus DataFrame to NumPy array
        Ybus = self.Circuit.ybus.values

        # Compute power injections
        S = V * np.dot(Ybus, np.conjugate(V))
        P = S.real  # Active power
        Q = S.imag  # Reactive power

        # Filter out P1, Q1, and Q7
        bus_order = self.Circuit.bus_order()
        P_filtered = [P[i] for i, bus in enumerate(bus_order) if bus not in ["Bus 1"]]
        Q_filtered = [Q[i] for i, bus in enumerate(bus_order) if bus not in ["Bus 1", "Bus 7"]]

        # Concatenate filtered active and reactive power values
        yx = np.concatenate((P_filtered, Q_filtered))

        return yx

    def calculate_power_mismatch(self, y, yx):
        y = np.array(y).reshape(-1, 1)  # Ensure proper shape
        yx = np.array(yx).reshape(-1, 1)  # Ensure proper shape

        if y.shape != yx.shape:
            raise ValueError(f"Shape mismatch: y has shape {y.shape}, yx has shape {yx.shape}")

        del_y = y - yx
        return del_y

    def calc_Px(self):
        """Computes real power (P) injections for each bus."""
        Px = {bus: 0.0 for bus in self.Circuit.bus_order()}
        Power_tolerance = 0.001  # Define numerical tolerance

        for k, bus_k in enumerate(self.Circuit.bus_order()):
            P_k = 0.0
            for j, bus_j in enumerate(self.Circuit.bus_order()):
                Y_kj = self.Circuit.ybus.at[bus_k, bus_j]
                P_k += self.voltage[bus_k] * self.voltage[bus_j] * abs(Y_kj) * np.cos(
                    self.delta[bus_k] - self.delta[bus_j] - np.angle(Y_kj)
                )

            # Enforce tolerance: If P_k is too small, replace with a default value (6.0 in your case)
            Px[bus_k] = P_k if abs(P_k) > Power_tolerance else 6.0

        return Px

    def calc_Qx(self):
        """Computes reactive power (Q) injections for each bus."""
        Qx = {bus: 0.0 for bus in self.Circuit.bus_order()}
        Power_tolerance = 0.001  # Define numerical tolerance

        for k, bus_k in enumerate(self.Circuit.bus_order()):
            Q_k = 0.0
            for j, bus_j in enumerate(self.Circuit.bus_order()):
                Y_kj = self.Circuit.ybus.at[bus_k, bus_j]
                Q_k += self.voltage[bus_k] * self.voltage[bus_j] * abs(Y_kj) * np.sin(
                    self.delta[bus_k] - self.delta[bus_j] - np.angle(Y_kj)
                )

            # Enforce tolerance: If Q_k is too small, replace with a default value (6.0 in your case)
            Qx[bus_k] = Q_k if abs(Q_k) > Power_tolerance else 6.0

        return Qx

    def calculate_J1(self):
        """Computes J1: Partial derivatives of active power with respect to voltage angles."""

        # Exclude Slack Bus (P1 derivatives removed)
        bus_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Bus 1"]]
        n = len(bus_order)  # Should be 6 (P2 to P7)
        J1 = np.zeros((n, n), dtype=float)

        for k, bus_k in enumerate(bus_order):
            for j, bus_j in enumerate(bus_order):
                Y_kj = self.Circuit.ybus.at[bus_k, bus_j]
                θ_kj = np.angle(Y_kj)
                V_k = self.voltage[bus_k]
                δ_k = self.delta[bus_k]

                if k == j:  # Diagonal elements J1_kk
                    J1[k, j] = -V_k * sum(
                        self.voltage[bus_m] * abs(self.Circuit.ybus.at[bus_k, bus_m]) *
                        np.sin(δ_k - self.delta[bus_m] - np.angle(self.Circuit.ybus.at[bus_k, bus_m]))
                        for bus_m in self.Circuit.bus_order() if bus_m not in ["Bus 1", bus_k]  # Exclude slack bus
                    )
                else:  # Off-diagonal elements J1_kn
                    V_n = self.voltage[bus_j]
                    δ_n = self.delta[bus_j]
                    J1[k, j] = V_k * V_n * abs(Y_kj) * np.sin(δ_k - δ_n - θ_kj)

        return J1

    def calculate_J2(self):
        """Computes J2: Partial derivatives of active power with respect to voltage magnitudes."""

        bus_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Bus 1"]]
        voltage_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Bus 1", "Bus 7"]]
        n = len(bus_order)  # 6 (P2 to P7)
        m = len(voltage_order)  # 5 (V2 to V6)

        J2 = np.zeros((n, m), dtype=float)

        for k, bus_k in enumerate(bus_order):
            for j, bus_j in enumerate(voltage_order):
                Y_kj = self.Circuit.ybus.at[bus_k, bus_j]
                θ_kj = np.angle(Y_kj)
                V_k = self.voltage[bus_k]
                V_j = self.voltage[bus_j]

                if k == j:
                    J2[k, j] = V_k * abs(Y_kj) * np.cos(θ_kj)
                else:
                    J2[k, j] = V_k * V_j * abs(Y_kj) * np.cos(self.delta[bus_k] - self.delta[bus_j] - θ_kj)

        return J2

    def calculate_J3(self):
        """Computes J3: Partial derivatives of reactive power with respect to voltage angles."""

        reactive_bus_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Bus 1", "Bus 7"]]
        angle_bus_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Bus 1"]]

        n = len(reactive_bus_order)  # 5 (Q2 to Q6)
        m = len(angle_bus_order)  # 6 (δ2 to δ7)

        J3 = np.zeros((n, m), dtype=float)

        for k, bus_k in enumerate(reactive_bus_order):
            for j, bus_j in enumerate(angle_bus_order):
                Y_kj = self.Circuit.ybus.at[bus_k, bus_j]
                θ_kj = np.angle(Y_kj)
                V_k = self.voltage[bus_k]
                V_j = self.voltage[bus_j]

                if k == j:
                    J3[k, j] = V_k * sum(
                        V_j * abs(Y_kj) * np.cos(self.delta[bus_k] - self.delta[bus_j] - θ_kj)
                        for bus_j in self.Circuit.bus_order() if bus_j not in ["Bus 1", bus_k]
                    )
                else:
                    J3[k, j] = -V_k * V_j * abs(Y_kj) * np.cos(self.delta[bus_k] - self.delta[bus_j] - θ_kj)

        return J3

    def calculate_J4(self):
        """Computes J4: Partial derivatives of reactive power with respect to voltage magnitudes."""

        reactive_bus_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Bus 1", "Bus 7"]]
        voltage_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Bus 1", "Bus 7"]]

        n = len(reactive_bus_order)  # 5 (Q2 to Q6)
        m = len(voltage_order)  # 5 (V2 to V6)

        J4 = np.zeros((n, m), dtype=float)

        for k, bus_k in enumerate(reactive_bus_order):
            for j, bus_j in enumerate(voltage_order):
                Y_kj = self.Circuit.ybus.at[bus_k, bus_j]
                θ_kj = np.angle(Y_kj)
                V_k = self.voltage[bus_k]
                V_j = self.voltage[bus_j]

                if k == j:
                    J4[k, j] = -V_k * abs(Y_kj) * np.sin(θ_kj) + sum(
                        V_j * abs(Y_kj) * np.sin(self.delta[bus_k] - self.delta[bus_j] - θ_kj)
                        for bus_j in self.Circuit.bus_order() if bus_j not in ["Bus 1", bus_k]
                    )
                else:
                    J4[k, j] = V_k * V_j * abs(Y_kj) * np.sin(self.delta[bus_k] - self.delta[bus_j] - θ_kj)

        return J4

    def construct_jacobian(self, J1, J2, J3, J4):
        """Constructs the full Jacobian matrix."""
        J_top = np.hstack((J1, J2))
        J_bottom = np.hstack((J3, J4))
        return np.vstack((J_top, J_bottom))

    def calculate_delta_x(self):
        if not hasattr(self, 'del_y'):
            raise ValueError("Mismatch vector Δy has not been computed.")
        J = self.construct_jacobian(self.J1, self.J2, self.J3, self.J4)
        delta_x = np.linalg.solve(J, self.del_y)
        return delta_x

    # def update_angles_voltages(self):
    #     delta_x = self.calculate_delta_x()
    #
    #     num_angles = len([bus for bus in self.Circuit.bus_order() if self.Circuit.bus_type[bus] != 'slack'])
    #     delta_angles = delta_x[:num_angles]
    #     delta_voltages = delta_x [num_angles:]
    #
    #     angle_index = 0
    #     voltage_index = 0
    #
    #     for bus in self.Circuit.bus_order():
    #         if self.Circuit.bus_type[bus] != 'slack':
    #             self.delta[bus] += delta_angles[angle_index]
    #             angle_index += 1
    #         if self.Circuit.bus_type[bus] not in ['slack', 'PV']:
    #             self.voltage[bus] += delta_voltages[voltage_index]
    #             voltage_index += 1
    #     print(self.delta)

    def update_angles_voltages(self):
        delta_x = self.calculate_delta_x()

        num_angles = sum(1 for bus in self.Circuit.bus_order() if self.Circuit.bus_type[bus] != 'slack')
        num_voltages = sum(1 for bus in self.Circuit.bus_order() if self.Circuit.bus_type[bus] not in ['slack', 'PV'])

        delta_angles = delta_x[:num_angles]  # First num_angles elements
        delta_voltages = delta_x[num_angles:num_angles + num_voltages]  # Remaining elements

        # Debugging output
        print(f"[DEBUG] delta_x.shape={delta_x.shape}, num_angles={num_angles}, num_voltages={num_voltages}")
        print(f"[DEBUG] delta_angles.shape={delta_angles.shape}, delta_voltages.shape={delta_voltages.shape}")

        angle_index = 0
        voltage_index = 0

        for bus in self.Circuit.bus_order():
            if self.Circuit.bus_type[bus] != 'slack':
                self.delta[bus] += delta_angles[angle_index]
                angle_index += 1
            if self.Circuit.bus_type[bus] not in ['slack', 'PV']:
                self.voltage[bus] += delta_voltages[voltage_index]
                voltage_index += 1


























