import numpy as np
from Classes.Newton_Raphson import NewtonRaphson
from FaultStudySolver import FaultStudySolver
from pprint import pprint
from numpy import angle, abs, degrees

class Solver:
    def __init__(self, circuit, analysis_mode='pf', faulted_bus=None, fault_type='3ph', fault_impedance=0.0):
        self.circuit = circuit
        self.analysis_mode = analysis_mode.lower()
        self.faulted_bus = faulted_bus
        self.fault_type = fault_type.lower()
        self.fault_impedance = fault_impedance

    def run(self):
        # Calculate Ybus and Display It
        self.circuit.calc_ybus()
        self.circuit.show_ybus()

        if self.analysis_mode == 'pf':
            self.run_power_flow()
            return
        elif self.analysis_mode == 'fault':
            if self.faulted_bus is None:
                raise ValueError("For fault analysis, a faulted_bus must be specified.")
            return self.run_fault_study()
        else:
            raise ValueError("Invalid analysis mode. Choose 'pf' or 'fault'.")

    def run_power_flow(self):
        from Classes.PowerFlowSolver import PowerFlowSolver
        power_flow_solver = PowerFlowSolver(1, self.circuit)

        self.circuit.power_flow_solver = power_flow_solver

        newton_solver = NewtonRaphson(power_flow_solver)
        converged = newton_solver.solve(tol=0.001, max_iter=50)

        if converged:
            print("\nNewton-Raphson converged successfully.")
        else:
            print("\nNewton-Raphson did not converge.")

        print("\nFinal Voltage Magnitudes:")
        for bus in self.circuit.bus_order():
            print(f"{bus}: {power_flow_solver.voltage[bus]:.4f}")

        print("\nFinal Voltage Angles (degrees):")
        for bus in self.circuit.bus_order():
            print(f"{bus}: {np.degrees(power_flow_solver.delta[bus]):.4f}")

        # viz = GraphVisualizer(self.circuit)
        # viz.plot_bus_voltages(power_flow_solver.voltage, power_flow_solver.delta)
        # viz.plot_line_flows(power_flow_solver)
        # viz.draw_network_topology(show_voltage=True, voltage_dict=power_flow_solver.voltage)


    def run_fault_study(self):
        fault_module = FaultStudySolver(self.circuit, self.faulted_bus, self.fault_type, self.fault_impedance)
        fault_current, voltages = fault_module.run()

        I_mag, I_ang = fault_current
        print(f"\n--- Fault Study Results ({self.fault_type.upper()} Fault at {self.faulted_bus}) ---")
        print(f"Fault Current: {I_mag:.4f} ∠ {I_ang:.2f}° p.u.")

        # print("\n--- Bus Voltages (post-fault, per unit) ---")
        # for bus, (mag, ang) in voltages.items():
        #     print(f"{bus}: {mag:.4f} ∠ {ang:.2f}°")

        if hasattr(fault_module, "phase_fault_current"):
            print("\n--- Phase Fault Currents (Ia, Ib, Ic) ---")
            for phase, (mag, ang) in fault_module.phase_fault_current.items():
                print(f"    {phase} = {mag:.4f} ∠ {ang:.2f}°")

        print("\n--- Phase Voltages (Va, Vb, Vc) ---")
        for bus, ((Va_mag, Va_ang), (Vb_mag, Vb_ang), (Vc_mag, Vc_ang)) in fault_module.phase_voltages.items():
            print(f"{bus}:")
            print(f"    Va = {Va_mag:.4f} ∠ {Va_ang:.2f}°")
            print(f"    Vb = {Vb_mag:.4f} ∠ {Vb_ang:.2f}°")
            print(f"    Vc = {Vc_mag:.4f} ∠ {Vc_ang:.2f}°")

        self.fault_module = fault_module
        return fault_current, voltages







