import numpy as np

from Classes.Circuit import Circuit


class PowerFlowSolver:
    def __init__(self, solver: int, Circuit:Circuit):
        self.solver = solver
        self.Circuit = Circuit

        self.flat_start()

        # Solve Method
        self.initialize_x()
        y = self.initialize_y()

        #Real Power
        Px = self.calc_Px()
        Px = {bus: float(Px[bus]) for bus in Px} #Convert np.float64 to a Python Float

        #Reactive Power
        Qx = self.calc_Qx()
        Qx = {bus: float(Qx[bus]) for bus in Qx} #Convert np.float64 to a Python Float

        #Mistmatch
        yx = self.calculate_yx(Px, Qx)
        self.del_y = self.calculate_power_mismatch(y,yx)

        #Jacobian
        self.J1 = self.calculate_J1()
        self.J2 = self.calculate_J2()
        self.J3 = self.calculate_J3()
        self.J4 = self.calculate_J4()
        self.J = self.construct_jacobian(self.J1, self.J2, self.J3, self.J4)

        #Change in the angle and voltage
        self.update_angles_voltages()

    def flat_start(self):
        self.delta = {bus:0 for bus in self.Circuit.bus_order}
        self.voltage = {bus:1 for bus in self.Circuit.bus_order}

    def initialize_x(self):
        delta_vector = np.array(list(self.delta.values()))
        voltage_vector = np.array(list(self.voltage.values()))
        x = np.concatenate((delta_vector, voltage_vector))
        return x

    def initialize_y(self):
        real_power_vector = np.array(list(self.Circuit.real_power_vector()))/s.mva_base #we need to check what is the name of s.mva_base in our project

        #Initialize y vectors
        y_real = []
        y_reactive = []

        for bus in self.Circuit.bus_order:
            if self.Circuit.bus_type[bus] != 'slack':
                y_real.append(real_power_vector[self.Circuit.bus_order,index(bus)])

        for bus in self.Circuit.bus_order:
            if self.Circuit.bus_Type [bus] not in ['slack','PV']:
                y_reactive.append(reactive_power_vector[self.Cicuit.bus_order.index(bus)])

        y = np.concatenate(y_real, y_reactive)
        return y

    def calc_Px(self):










    # def initialize_voltages(self):
    #     """Initializes the voltage magnitudes and angles based on the bus types."""
    #     for bus in self.buses:
    #         if bus.bus_type == "Slack Bus":
    #             bus.vpu = 1.0
    #             bus.delta = 0.0
    #         elif bus.bus_type == "PV Bus":
    #             bus.delta = None  # To be computed
    #         elif bus.bus_type == "PQ Bus":
    #             bus.vpu = 1.0  # Initial estimate
    #             bus.delta = 0.0  # Initial estimate
    #
    # def get_voltage_vector(self):
    #     """
    #     Returns the complex voltage vector (V) for the system.
    #     Ensures all voltage values are properly initialized before computation.
    #     """
    #     voltage_vector = []
    #     for bus in self.buses:
    #         if bus.vpu is None:
    #             raise ValueError(f"[ERROR] Voltage magnitude not initialized for Bus '{bus.name}'")
    #
    #         if bus.delta is None:
    #             bus.delta = 0.0  # Assign default delta if not set
    #
    #         voltage_vector.append(bus.vpu * np.exp(1j * np.radians(bus.delta)))
    #
    #     return np.array(voltage_vector)
    #
    # def compute_power_injection(self, bus):
    #     """Computes real and reactive power injections using the Ybus matrix."""
    #     index = bus.index
    #     V = self.get_voltage_vector()
    #     Vk = V[index]
    #
    #     Pk = 0
    #     Qk = 0
    #     for n in range(len(self.buses)):
    #         Ykn = self.ybus.loc[bus.name, self.buses[n].name]
    #         Vn = V[n]
    #         theta_kn = np.angle(Ykn)
    #         Ykn_mag = np.abs(Ykn)
    #
    #         Pk += Vk.real * Vn.real * Ykn_mag * np.cos(
    #             np.radians(bus.delta) - np.radians(self.buses[n].delta) - theta_kn)
    #         Qk += Vk.real * Vn.real * Ykn_mag * np.sin(
    #             np.radians(bus.delta) - np.radians(self.buses[n].delta) - theta_kn)
    #
    #     return Pk, Qk
    # def compute_power_mismatch(self):
    #     """Computes the power mismatch vector for Newton-Raphson iterations."""
    #     buses = self.system.buses
    #     ybus = self.system.ybus
    #     voltages = self.system.get_voltage_vector()
    #
    #     mismatch_vector = []
    #     pq_indices = []
    #
    #     for bus in buses:
    #         if bus.bus_type in ["PV Bus", "PQ Bus"]:
    #             P_calc, Q_calc = self.system.compute_power_injection(bus)
    #
    #             P_mismatch = bus.P - P_calc if bus.P is not None else 0
    #             Q_mismatch = bus.Q - Q_calc if bus.Q is not None else 0
    #
    #             mismatch_vector.append(P_mismatch)
    #             if bus.bus_type == "PQ Bus":
    #                 mismatch_vector.append(Q_mismatch)
    #                 pq_indices.append(bus.index)
    #
    #     return np.array(mismatch_vector), pq_indices
    #
    # def compute_jacobian(self):
    #     """Compute the Jacobian matrix for Newton-Raphson iterations."""
    #     buses = self.system.buses
    #     ybus = self.system.ybus
    #     J = np.zeros((len(buses) - 1, len(buses) - 1))  # Adjust Jacobian size
    #     return J  # Replace with actual Jacobian computation
    #
    # def solve_power_flow(self, max_iters=10, tolerance=0.0001):
    #     """Solves the power flow equations using Newton-Raphson."""
    #     for iteration in range(max_iters):
    #         mismatch_vector, pq_indices = self.compute_power_mismatch()
    #
    #         if np.max(np.abs(mismatch_vector)) < tolerance:
    #             print("[INFO] Power flow converged!")
    #             return True  # Convergence achieved
    #
    #         # Compute Jacobian
    #         J = self.compute_jacobian()
    #         if np.linalg.det(J) == 0:
    #             print("[ERROR] Jacobian is singular. Power flow cannot proceed.")
    #             return False
    #
    #         # Solve for voltage corrections
    #         delta_x = np.linalg.solve(J, -mismatch_vector)
    #
    #         # Update bus voltages and angles
    #         for i, bus_idx in enumerate(pq_indices):
    #             bus = self.system.buses[bus_idx]
    #             if bus.bus_type in ["PQ Bus", "PV Bus"]:
    #                 bus.delta += delta_x[i]  # Update delta (angle)
    #             if bus.bus_type == "PQ Bus":
    #                 bus.vpu += delta_x[i + len(pq_indices)]  # Update voltage magnitude
    #
    #     print("[WARNING] Power flow did not converge.")
    #     return False

