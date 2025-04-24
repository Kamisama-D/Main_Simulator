import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from Classes.MainSolver import Solver

class PowerSimGUI:
    def __init__(self, root, circuit):
        self.root = root
        self.circuit = circuit
        self.root.title("Power System Simulation GUI")

        self.mode_var = tk.StringVar(value="pf")
        self.fault_type_var = tk.StringVar()
        self.fault_bus_var = tk.StringVar()

        self.fault_type_display_map = {
            "Three Phase (3ph)": "3ph",
            "Single Line to Ground (SLG)": "slg",
            "Line to Line (LL)": "ll",
            "Double Line to Ground (DLG)": "dlg"
        }

        self._build_gui()

    def _build_gui(self):
        # Main content area
        top_frame = ttk.Frame(self.root)
        top_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(top_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(top_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Simulator Info
        info_label = ttk.Label(left_frame, text="Simulator Info", font=("Arial", 12, "bold"))
        info_label.pack(anchor="w")
        self.info_box = scrolledtext.ScrolledText(left_frame, width=80, height=30, wrap=tk.NONE)
        self.info_box.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self._load_simulator_info()

        # Simulation Output and Controls
        control_label = ttk.Label(right_frame, text="Simulation Output", font=("Arial", 12, "bold"))
        control_label.pack(anchor="w")

        self.result_box = scrolledtext.ScrolledText(right_frame, width=80, height=20, wrap=tk.WORD)
        self.result_box.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        mode_label = ttk.Label(right_frame, text="Select Analysis Mode:")
        mode_label.pack(pady=5)

        mode_frame = ttk.Frame(right_frame)
        mode_frame.pack(pady=5)
        ttk.Radiobutton(mode_frame, text="Power Flow", variable=self.mode_var, value="pf", command=self.update_mode).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Fault Study", variable=self.mode_var, value="fault", command=self.update_mode).pack(side=tk.LEFT, padx=10)

        self.fault_frame = ttk.LabelFrame(right_frame, text="Fault Study Options")
        ttk.Label(self.fault_frame, text="Fault Type:").grid(row=0, column=0, padx=5, pady=5)
        self.fault_type_menu = ttk.Combobox(self.fault_frame, textvariable=self.fault_type_var,
                                       values=list(self.fault_type_display_map.keys()), state="readonly")
        self.fault_type_menu.grid(row=0, column=1, padx=5, pady=5)
        self.fault_type_menu.set("")

        ttk.Label(self.fault_frame, text="Faulted Bus:").grid(row=1, column=0, padx=5, pady=5)
        self.fault_bus_menu = ttk.Combobox(self.fault_frame, textvariable=self.fault_bus_var,
                                           values=self.circuit.bus_order(), state="readonly")
        self.fault_bus_menu.grid(row=1, column=1, padx=5, pady=5)

        self.fault_frame.pack(padx=10, pady=10, fill=tk.X)

        run_button = ttk.Button(right_frame, text="Run Simulation", command=self.run_simulation)
        run_button.pack(pady=10)

        self.update_mode()

    def _load_simulator_info(self):
        info = "--- Simulator Configuration ---\n\n"

        info += "[Buses]\n"
        info += f"{'Name':<10} {'kV':<6} {'Type':<12} {'x':<5} {'y':<5}\n"
        for name, bus in self.circuit.buses.items():
            info += f"{bus.name:<10} {bus.base_kv:<6} {bus.bus_type:<12} {getattr(bus, 'x', 0):<5.1f} {getattr(bus, 'y', 0):<5.1f}\n"

        info += "\n[Generators]\n"
        info += f"{'Name':<10} {'Bus':<8} {'P(MW)':<8} {'x1':<6} {'x2':<6} {'x0':<6}\n"
        for name, gen in self.circuit.generators.items():
            info += f"{name:<10} {gen.bus.name:<8} {gen.real_power:<8} {gen.x1:<6.2f} {gen.x2:<6.2f} {gen.x0:<6.2f}\n"

        info += "\n[Loads]\n"
        info += f"{'Name':<10} {'Bus':<8} {'P(MW)':<8} {'Q(Mvar)':<8}\n"
        for name, load in self.circuit.loads.items():
            info += f"{name:<10} {load.bus.name:<8} {load.real_power:<8} {load.reactive_power:<8}\n"

        info += "\n[Transformers]\n"
        info += f"{'Name':<10} {'Bus1':<8} {'Bus2':<8} {'Rating':<8} {'Z(%)':<6} {'X/R':<6}\n"
        for name, xfmr in self.circuit.transformers.items():
            info += f"{name:<10} {getattr(xfmr.bus1, 'name', xfmr.bus1):<8} {getattr(xfmr.bus2, 'name', xfmr.bus2):<8} {xfmr.power_rating:<8} {xfmr.impedance_percent:<6} {xfmr.x_over_r_ratio:<6}\n"

        info += "\n[Transmission Lines]\n"
        info += f"{'Name':<10} {'From':<8} {'To':<8} {'Length(mi)':<12}\n"
        for name, line in self.circuit.transmission_lines.items():
            info += f"{name:<10} {getattr(line.bus1, 'name', line.bus1):<8} {getattr(line.bus2, 'name', line.bus2):<8} {line.length:<12.1f}\n"

        self.info_box.insert(tk.END, info)
        self.info_box.configure(state="disabled")

    def update_mode(self):
        if self.mode_var.get() == "fault":
            self.fault_frame.pack(padx=10, pady=10, fill=tk.X)
        else:
            self.fault_frame.pack_forget()
            self.fault_type_var.set("")
            self.fault_bus_var.set("")

    def run_simulation(self):
        mode = self.mode_var.get()
        self.result_box.delete("1.0", tk.END)

        if mode == "pf":
            solver = Solver(self.circuit, analysis_mode='pf')
            solver.run()
            results = self.collect_power_flow_results(solver)
            self.result_box.insert(tk.END, results)

        elif mode == "fault":
            fault_type_display = self.fault_type_var.get()
            faulted_bus = self.fault_bus_var.get()

            if not fault_type_display:
                messagebox.showerror("Error", "Please select a fault type.")
                return

            if not faulted_bus:
                messagebox.showerror("Error", "Please select a faulted bus.")
                return

            fault_type = self.fault_type_display_map[fault_type_display]

            solver = Solver(self.circuit, analysis_mode='fault', faulted_bus=faulted_bus, fault_type=fault_type)
            fault_current, voltages = solver.run()
            results = self.collect_fault_study_results(solver, fault_current, voltages)
            self.result_box.insert(tk.END, results)

    def collect_power_flow_results(self, solver):
        from numpy import degrees
        power_flow_solver = solver.circuit.power_flow_solver

        results = "--- Power Flow Results ---\n"
        results += "\nFinal Voltage Magnitudes (p.u.):\n"
        for bus in solver.circuit.bus_order():
            results += f"{bus}: {power_flow_solver.voltage[bus]:.4f}\n"

        results += "\nFinal Voltage Angles (degrees):\n"
        for bus in solver.circuit.bus_order():
            results += f"{bus}: {degrees(power_flow_solver.delta[bus]):.2f}°\n"

        return results

    def collect_fault_study_results(self, solver, fault_current, voltages):
        fault_module = solver.fault_module

        I_mag, I_ang = fault_current
        results = f"--- Fault Study Results ({solver.fault_type.upper()} Fault at {solver.faulted_bus}) ---\n"
        results += f"Fault Current: {I_mag:.4f} ∠ {I_ang:.2f}° p.u.\n\n"

        if hasattr(fault_module, "phase_fault_current") and fault_module.phase_fault_current:
            results += "\n--- Phase Fault Currents (Ia, Ib, Ic) ---\n"
            for phase, (mag, ang) in fault_module.phase_fault_current.items():
                results += f"    {phase} = {mag:.4f} ∠ {ang:.2f}°\n"

        if hasattr(fault_module, "phase_voltages") and fault_module.phase_voltages:
            results += "\n--- Phase Voltages (Va, Vb, Vc) ---\n"
            for bus, ((Va_mag, Va_ang), (Vb_mag, Vb_ang), (Vc_mag, Vc_ang)) in fault_module.phase_voltages.items():
                results += f"{bus}:\n"
                results += f"    Va = {Va_mag:.4f} ∠ {Va_ang:.2f}°\n"
                results += f"    Vb = {Vb_mag:.4f} ∠ {Vb_ang:.2f}°\n"
                results += f"    Vc = {Vc_mag:.4f} ∠ {Vc_ang:.2f}°\n"
        elif hasattr(fault_module, "voltages") and fault_module.voltages:
            results += "\n--- Bus Voltages (magnitude ∠ angle) ---\n"
            for bus, (mag, ang) in fault_module.voltages.items():
                results += f"{bus}: {mag:.4f} ∠ {ang:.2f}°\n"

        return results


def launch_gui(circuit):
    root = tk.Tk()
    app = PowerSimGUI(root, circuit)
    root.mainloop()
