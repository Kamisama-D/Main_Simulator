import numpy as np
import pandas as pd

from Classes.Circuit import Circuit
from system_setting import SystemSettings


class PowerFlowSolver:
    def __init__(self, solver: int, circuit: Circuit, do_one_iteration: bool = False):
        self.solver = solver
        self.Circuit = circuit
        self.Circuit.calc_ybus()

        # ✅ Verify the bus classifications before proceeding
        print("\n[DEBUG] Bus Type Classification (Used in PowerFlowSolver):")
        for bus_name, bus in self.Circuit.buses.items():
            print(f"  - {bus_name}: {bus.bus_type}")

        self.flat_start()

        # Solve Method
        self.initialize_x()
        y = self.initialize_y()


        #Real Power
        Px = self.calc_Px()
        Px = {bus: float(Px[bus]) for bus in Px}


        #Reactive Power
        Qx = self.calc_Qx()
        Qx = {bus: float(Qx[bus]) for bus in Qx}

        #Mistmatch
        yx = self.calculate_yx(Px, Qx)
        self.del_y = self.calculate_power_mismatch(y, yx)

        # Compute Jacobian for first iteration
        self.J1 = self.calculate_J1()
        self.J2 = self.calculate_J2()
        self.J3 = self.calculate_J3()
        self.J4 = self.calculate_J4()
        self.J = self.construct_jacobian(self.J1, self.J2, self.J3, self.J4)




    def flat_start(self):
        """Initializes flat start with delta=0 and voltage=1 p.u."""
        self.delta = {bus: 0 for bus in self.Circuit.bus_order()}
        self.voltage = {bus: 1 for bus in self.Circuit.bus_order()}

    def initialize_x(self):
        """Constructs state variable vector x (delta and voltage magnitudes)."""
        delta_vector = np.array(list(self.delta.values()))
        voltage_vector = np.array(list(self.voltage.values()))
        print("[DEBUG] delta:", self.delta)
        print("[DEBUG] voltage:", self.voltage)

        x = np.concatenate((delta_vector, voltage_vector))


        # Debugging output
        print(f"[DEBUG] x initialized with shape {x.shape}")

        return x

    def initialize_y(self):
        """Initializes y vector by extracting per-unit real and reactive power values, excluding Slack and PV buses."""

        # Extract per-unit real and reactive power values
        real_power_vector = np.array(list(self.Circuit.real_power_vector().values())) /(self.Circuit.get_base_power())
        reactive_power_vector = np.array(list(self.Circuit.reactive_power_vector().values())) / (self.Circuit.get_base_power())

        # Initialize y vectors
        y_real = []
        y_reactive = []

        for bus in self.Circuit.bus_order():
            if self.Circuit.bus_type[bus] != "Slack Bus":
                y_real.append(real_power_vector[self.Circuit.bus_order().index(bus)])

        for bus in self.Circuit.bus_order():
            if self.Circuit.bus_type[bus] not in ["Slack Bus", "PV Bus"]:
                y_reactive.append(reactive_power_vector[self.Circuit.bus_order().index(bus)])

        y = np.concatenate((y_real,y_reactive))

        print("\n--- INITIALIZED y (Specified Power Vector) ---")
        for i, val in enumerate(y):
            print(f"y[{i}] = {val:.6f}")
        print(f"[DEBUG] y shape = {y.shape}\n")
        return y



    def calculate_yx(self, Px, Qx):
        """
        Calculates the expected power injection vector yx = [P, Q] for all buses,
        using explicitly provided Px and Qx dictionaries. Assumes all buses are included.
        """
        yx_P = [Px[bus] for bus in self.Circuit.bus_order()]
        yx_Q = [Qx[bus] for bus in self.Circuit.bus_order()]

        yx = np.concatenate((yx_P, yx_Q))

        print("\n--- CALCULATED yx (Injected Power Vector) ---")
        for i, val in enumerate(yx):
            print(f"yx[{i}] = {val:.6f}")
        print(f"[DEBUG] yx shape = {yx.shape}\n")

        return yx

    def calculate_power_mismatch(self, y, yx):
        y = np.array(y)
        yx = np.array(yx)
        del_y = y - yx
        print("\n--- MISMATCH Vector Δy = y - yx ---")
        for i, val in enumerate(del_y):
            print(f"Δy[{i}] = {val:.6f}")
        print(f"[DEBUG] del_y shape = {del_y.shape}\n")

        return del_y

    def calc_Px(self):
        """Computes real power (P) injections using polar form."""
        Px = {}
        bus_order = self.Circuit.bus_order()

        for bus_k in bus_order:
            V_k = self.voltage[bus_k]
            δ_k = self.delta[bus_k]
            P_k = 0.0

            for bus_n in bus_order:
                V_n = self.voltage[bus_n]
                δ_n = self.delta[bus_n]
                Y_kn = self.Circuit.ybus.at[bus_k, bus_n]
                θ_kn = np.angle(Y_kn)

                P_k += V_k * V_n * abs(Y_kn) * np.cos(δ_k - δ_n - θ_kn)

            Px[bus_k] = P_k

        return Px

    def calc_Qx(self):
        """Computes reactive power (Q) injections using polar form."""
        Qx = {}
        bus_order = self.Circuit.bus_order()

        for bus_k in bus_order:
            V_k = self.voltage[bus_k]
            δ_k = self.delta[bus_k]
            Q_k = 0.0

            for bus_n in bus_order:
                V_n = self.voltage[bus_n]
                δ_n = self.delta[bus_n]
                Y_kn = self.Circuit.ybus.at[bus_k, bus_n]
                θ_kn = np.angle(Y_kn)

                Q_k += V_k * V_n * abs(Y_kn) * np.sin(δ_k - δ_n - θ_kn)

            Qx[bus_k] = Q_k

        return Qx

    def calculate_J1(self):
        """J1: ∂P/∂δ for all buses including Slack and PV."""
        bus_order = self.Circuit.bus_order()
        n = len(bus_order)
        J1 = np.zeros((n, n))

        for k, bus_k in enumerate(bus_order):
            V_k = self.voltage[bus_k]
            δ_k = self.delta[bus_k]
            for j, bus_j in enumerate(bus_order):
                V_j = self.voltage[bus_j]
                δ_j = self.delta[bus_j]
                Y_kj = self.Circuit.ybus.at[bus_k, bus_j]
                θ_kj = np.angle(Y_kj)

                if k != j:
                    # Off-diagonal: J1[k, j] = Vk * Vj * |Ykj| * sin(δk - δj - θkj)
                    J1[k, j] = V_k * V_j * abs(Y_kj) * np.sin(δ_k - δ_j - θ_kj)
                else:
                    # Diagonal: J1[k, k] = -Vk * Σ_{n ≠ k} |Ykn| * Vn * sin(δk - δn - θkn)
                    J1[k, j] = -V_k * sum(
                        self.voltage[bus_m] * abs(self.Circuit.ybus.at[bus_k, bus_m]) *
                        np.sin(δ_k - self.delta[bus_m] - np.angle(self.Circuit.ybus.at[bus_k, bus_m]))
                        for m, bus_m in enumerate(bus_order) if m != k
                    )

        # Format as a DataFrame for display
        J1_df = pd.DataFrame(J1, index=bus_order, columns=bus_order)
        print("\n[DEBUG] J1 (∂P/∂δ):")
        print(J1_df)

        return J1

    def calculate_J2(self):
        """J2: ∂P/∂V for all buses including Slack and PV."""
        bus_order = self.Circuit.bus_order()
        n = len(bus_order)
        J2 = np.zeros((n, n))

        for k, bus_k in enumerate(bus_order):
            V_k = self.voltage[bus_k]
            δ_k = self.delta[bus_k]
            for j, bus_j in enumerate(bus_order):
                δ_j = self.delta[bus_j]
                Y_kj = self.Circuit.ybus.at[bus_k, bus_j]
                θ_kj = np.angle(Y_kj)

                if k != j:
                    # Off-diagonal: J2[k, j] = Vk * |Ykj| * cos(δk - δj - θkj)
                    J2[k, j] = V_k * abs(Y_kj) * np.cos(δ_k - δ_j - θ_kj)
                else:
                    # Diagonal: J2[k, k] = Vk * |Ykk| * cos(θkk) + Σ_{n} |Ykn| * Vn * cos(δk - δn - θkn)
                    Y_kk = self.Circuit.ybus.at[bus_k, bus_k]
                    θ_kk = np.angle(Y_kk)
                    diag_term = V_k * abs(Y_kk) * np.cos(θ_kk)

                    sum_term = sum(
                        abs(self.Circuit.ybus.at[bus_k, bus_m]) * self.voltage[bus_m] *
                        np.cos(δ_k - self.delta[bus_m] - np.angle(self.Circuit.ybus.at[bus_k, bus_m]))
                        for m, bus_m in enumerate(bus_order)  # NOTE: include m == k
                    )

                    J2[k, j] = diag_term + sum_term

        # Format as a DataFrame for display
        J2_df = pd.DataFrame(J2, index=bus_order, columns=bus_order)
        print("\n[DEBUG] J2 (∂P/∂V):")
        print(J2_df)

        return J2

    def calculate_J3(self):
        """J3: ∂Q/∂δ for all buses including Slack and PV."""
        bus_order = self.Circuit.bus_order()
        n = len(bus_order)
        J3 = np.zeros((n, n))

        for k, bus_k in enumerate(bus_order):
            V_k = self.voltage[bus_k]
            δ_k = self.delta[bus_k]
            for j, bus_j in enumerate(bus_order):
                V_j = self.voltage[bus_j]
                δ_j = self.delta[bus_j]
                Y_kj = self.Circuit.ybus.at[bus_k, bus_j]
                θ_kj = np.angle(Y_kj)

                if k != j:
                    # Off-diagonal: J3[k, j] = -Vk * Vj * |Ykj| * cos(δk - δj - θkj)
                    J3[k, j] = -V_k * V_j * abs(Y_kj) * np.cos(δ_k - δ_j - θ_kj)
                else:
                    # Diagonal: J3[k, k] = Vk * Σ_{n ≠ k} |Ykn| * Vn * cos(δk - δn - θkn)
                    sum_term = sum(
                        abs(self.Circuit.ybus.at[bus_k, bus_m]) * self.voltage[bus_m] *
                        np.cos(δ_k - self.delta[bus_m] - np.angle(self.Circuit.ybus.at[bus_k, bus_m]))
                        for m, bus_m in enumerate(bus_order) if m != k
                    )
                    J3[k, j] = V_k * sum_term

        # Format as a DataFrame for display
        J3_df = pd.DataFrame(J3, index=bus_order, columns=bus_order)
        print("\n[DEBUG] J3 (∂Q/∂δ):")
        print(J3_df)

        return J3

    def calculate_J4(self):
        """J4: ∂Q/∂V for all buses including Slack and PV."""
        bus_order = self.Circuit.bus_order()
        n = len(bus_order)
        J4 = np.zeros((n, n))

        for k, bus_k in enumerate(bus_order):
            V_k = self.voltage[bus_k]
            δ_k = self.delta[bus_k]
            for j, bus_j in enumerate(bus_order):
                V_j = self.voltage[bus_j]
                δ_j = self.delta[bus_j]
                Y_kj = self.Circuit.ybus.at[bus_k, bus_j]
                θ_kj = np.angle(Y_kj)

                if k != j:
                    # Off-diagonal: J4[k, j] = Vk * |Ykj| * sin(δk - δj - θkj)
                    J4[k, j] = V_k * abs(Y_kj) * np.sin(δ_k - δ_j - θ_kj)
                else:
                    # Diagonal: J4[k, k] = -Vk * |Ykk| * sin(θkk) + Σ_{n} |Ykn| * Vn * sin(δk - δn - θkn)
                    Y_kk = self.Circuit.ybus.at[bus_k, bus_k]
                    θ_kk = np.angle(Y_kk)
                    diag_term = -V_k * abs(Y_kk) * np.sin(θ_kk)
                    sum_term = sum(
                        abs(self.Circuit.ybus.at[bus_k, bus_m]) * self.voltage[bus_m] *
                        np.sin(δ_k - self.delta[bus_m] - np.angle(self.Circuit.ybus.at[bus_k, bus_m]))
                        for m, bus_m in enumerate(bus_order)
                    )
                    J4[k, j] = diag_term + sum_term

        # Format as a DataFrame for display
        J4_df = pd.DataFrame(J4, index=bus_order, columns=bus_order)
        print("\n[DEBUG] J4 (∂Q/∂V):")
        print(J4_df)

        return J4

    def construct_jacobian(self, J1, J2, J3, J4):
        """Constructs the full Jacobian matrix by stacking submatrices."""
        top = np.hstack((J1, J2))
        bottom = np.hstack((J3, J4))
        J = np.vstack((top, bottom))

        bus_order = self.Circuit.bus_order()
        labels = [f"Bus {b}" for b in bus_order]
        full_index = labels + labels
        full_columns = bus_order + bus_order
        J_df = pd.DataFrame(J, index=full_index, columns=full_columns)

        print("\n[DEBUG] Full Jacobian Matrix:")
        print(J_df)
        print(f"[DEBUG] Full Jacobian shape = {J.shape}")
        return J

    def calculate_delta_x(self):
        if not hasattr(self, 'del_y'):
            raise ValueError("Mismatch vector Δy has not been computed.")
        J = self.construct_jacobian(self.J1, self.J2, self.J3, self.J4)
        delta_x = np.linalg.solve(J, self.del_y)
        return delta_x

    def update_angles_voltages(self):
        delta_x = self.calculate_delta_x()

        num_angles = len([bus for bus in self.Circuit.bus_order() if self.Circuit.bus_type[bus] != 'Slack Bus'])
        delta_angles = delta_x[:num_angles]
        delta_voltages = delta_x [num_angles:]

        angle_index = 0
        voltage_index = 0

        for bus in self.Circuit.bus_order():
            if self.Circuit.bus_type[bus] != 'Slack Bus':
                self.delta[bus] += delta_angles[angle_index]
                angle_index += 1
            if self.Circuit.bus_type[bus] not in ['Slack Bus', 'PV Bus']:
                self.voltage[bus] += delta_voltages[voltage_index]
                voltage_index += 1
        print(self.delta)




























