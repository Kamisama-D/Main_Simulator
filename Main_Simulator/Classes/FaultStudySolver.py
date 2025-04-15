import numpy as np

from Classes.Circuit import Circuit
from Classes.generator import Generator

class FaultStudySolver:
    def __init__(self, circuit:Circuit, faulted_bus:str):
        self.circuit = circuit
        self.faulted_bus = faulted_bus
        self.fault_current = None
        self.voltages = {}

    def run(self):

        '''

        system base in the setting: Q of Generator1 = 100 Mvar, Q of Generator2 is 200 Mvar

        pu S = sqrt(Q**2 + P**2)

        '''

        # For fault study, we use the augmented positive-sequence Ybus.
        Ybus_positive_df = self.circuit.calc_ybus_positive()
        Ybus_positive = Ybus_positive_df.values

        Zbus = np.linalg.inv(Ybus_positive)

        # Determine the index corresponding to the faulted bus.
        bus_order = list(Ybus_positive_df.index)
        try:
            n = bus_order.index(self.faulted_bus)
        except ValueError:
            raise ValueError(f"Faulted bus '{self.faulted_bus}' not found in the augmented Ybus.")

        # Calculate fault current (V_F is 1.0 p.u. pre-fault voltage)
        V_F = 1.0    # pre-fault voltage in per-unit
        Z_nn = Zbus[n, n]
        I_complex = V_F / Z_nn
        I_mag = np.abs(I_complex)
        I_ang = np.degrees(np.angle(I_complex))
        if I_ang > 180:
            I_ang -= 360
        self.fault_current = (I_mag, I_ang)  # ⬅️ store tuple, fully formatted

        # Calculate post-fault bus voltages; at the faulted bus, E_n becomes 0.
        for k, node in enumerate(bus_order):
            E_k_complex = (1 - (Zbus[k, n] / Z_nn)) * V_F
            magnitude = np.abs(E_k_complex)
            angle_deg = np.degrees(np.angle(E_k_complex))
            self.voltages[node] = (magnitude, angle_deg)

        # updates: result should use voltage magnitude and degree
        return self.fault_current, self.voltages  # where fault_current = (magnitude, angle)


    def __repr__(self):
        return f"FaultStudySolver(faulted_bus='{self.faulted_bus}')"