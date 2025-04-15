import numpy as np
from Classes.Newton_Raphson import NewtonRaphson
from FaultStudySolver import FaultStudySolver

class Solver:
    def __init__(self, circuit, analysis_mode='pf', faulted_bus=None):
        self.circuit = circuit
        self.analysis_mode = analysis_mode.lower()
        self.faulted_bus = faulted_bus

    def run(self):
        # Calculate Ybus and Display It
        self.circuit.calc_ybus()
        self.circuit.show_ybus()

        if self.analysis_mode == 'pf':
            self.run_power_flow()
        elif self.analysis_mode == 'fault':
            if self.faulted_bus is None:
                raise ValueError("For fault analysis, a faulted_bus must be specified.")
            self.run_fault_study()
        else:
            raise ValueError("Invalid analysis mode. Choose 'pf' or 'fault'.")

    def run_power_flow(self):
        from Classes.PowerFlowSolver import PowerFlowSolver
        power_flow_solver = PowerFlowSolver(1, self.circuit)
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

    def run_fault_study(self):
        fault_solver = FaultStudySolver(self.circuit, self.faulted_bus)
        fault_current, voltages = fault_solver.run()

        I_mag, I_ang = fault_current  # Already processed
        print(f"\nFault Study Results:")
        print(f"Fault current at {self.faulted_bus}: {I_mag:.4f} ∠ {I_ang:.2f}° p.u.")

        print("\nFinal Voltage Magnitudes:")
        for node, (mag, _) in voltages.items():
            print(f"{node}: {mag:.4f}")

        print("\nFinal Voltage Angles (degrees):")
        for node, (_, ang) in voltages.items():
            print(f"{node}: {ang:.4f}")






