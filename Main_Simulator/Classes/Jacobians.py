
def calculate_J1(self):
    """Computes J1: Partial derivatives of active power with respect to voltage angles."""

    # Exclude Slack Bus (P1 derivatives removed)
    bus_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Slack Bus"]]
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
                    for bus_m in self.Circuit.bus_order() if bus_m not in ["Slack Bus", bus_k]  # Exclude slack bus
                )
            else:  # Off-diagonal elements J1_kn
                V_n = self.voltage[bus_j]
                δ_n = self.delta[bus_j]
                J1[k, j] = V_k * V_n * abs(Y_kj) * np.sin(δ_k - δ_n - θ_kj)

    return J1

def calculate_J2(self):
    """Computes J2: Partial derivatives of active power with respect to voltage magnitudes."""

    bus_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Slack Bus"]]
    voltage_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Slack Bus", "PV Bus"]]
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

    reactive_bus_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Slack Bus", "PV Bus"]]
    angle_bus_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Slack Bus"]]

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
                    for bus_j in self.Circuit.bus_order() if bus_j not in ["Slack Bus", bus_k]
                )
            else:
                J3[k, j] = -V_k * V_j * abs(Y_kj) * np.cos(self.delta[bus_k] - self.delta[bus_j] - θ_kj)

    return J3

def calculate_J4(self):
    """Computes J4: Partial derivatives of reactive power with respect to voltage magnitudes."""

    reactive_bus_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Slack Bus", "PV Bus"]]
    voltage_order = [bus for bus in self.Circuit.bus_order() if bus not in ["Slack Bus", "PV Bus"]]

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
                    for bus_j in self.Circuit.bus_order() if bus_j not in ["Slack Bus", bus_k]
                )
            else:
                J4[k, j] = V_k * V_j * abs(Y_kj) * np.sin(self.delta[bus_k] - self.delta[bus_j] - θ_kj)

    return J4

def construct_jacobian(self, J1, J2, J3, J4):
    """Constructs the full Jacobian matrix."""
    J_top = np.hstack((J1, J2))
    J_bottom = np.hstack((J3, J4))
    return np.vstack((J_top, J_bottom))