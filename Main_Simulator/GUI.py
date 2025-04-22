import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from MainSolver import Solver

class PowerSimGUI:
    def __init__(self, root, circuit):
        self.root = root
        self.circuit = circuit
        self.root.title("Power System Simulation GUI")

        self.mode_var = tk.StringVar(value="pf")
        self.fault_type_var = tk.StringVar()
        self.fault_bus_var = tk.StringVar()

        self.fault_type_display_map = {
            "Single Line to Ground (SLG)": "slg",
            "Three Phase (3ph)": "3ph",
            "Line to Line (LL)": "ll",
            "Double Line to Ground (DLG)": "dlg"
        }

        self._build_widgets()

    def _build_widgets(self):
        mode_label = ttk.Label(self.root, text="Select Analysis Mode:")
        mode_label.pack(pady=5)

        mode_frame = ttk.Frame(self.root)
        mode_frame.pack(pady=5)

        ttk.Radiobutton(mode_frame, text="Power Flow", variable=self.mode_var, value="pf", command=self.update_mode).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Fault Study", variable=self.mode_var, value="fault", command=self.update_mode).pack(side=tk.LEFT, padx=10)

        self.fault_frame = ttk.LabelFrame(self.root, text="Fault Study Options")

        ttk.Label(self.fault_frame, text="Fault Type:").grid(row=0, column=0, padx=5, pady=5)
        self.fault_type_menu = ttk.Combobox(self.fault_frame, textvariable=self.fault_type_var,
                                       values=list(self.fault_type_display_map.keys()), state="readonly")
        self.fault_type_menu.grid(row=0, column=1, padx=5, pady=5)
        self.fault_type_menu.set("")  # start with no default selection

        ttk.Label(self.fault_frame, text="Faulted Bus:").grid(row=1, column=0, padx=5, pady=5)
        self.fault_bus_menu = ttk.Combobox(self.fault_frame, textvariable=self.fault_bus_var,
                                           values=self.circuit.bus_order(), state="readonly")
        self.fault_bus_menu.grid(row=1, column=1, padx=5, pady=5)

        run_button = ttk.Button(self.root, text="Run Simulation", command=self.run_simulation)
        run_button.pack(pady=10)

        self.result_box = scrolledtext.ScrolledText(self.root, width=100, height=25, wrap=tk.WORD)
        self.result_box.pack(padx=10, pady=10)

        self.update_mode()

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

        if hasattr(fault_module, "phase_fault_current"):
            results += "--- Phase Fault Currents (Ia, Ib, Ic) ---\n"
            for phase, (mag, ang) in fault_module.phase_fault_current.items():
                results += f"    {phase} = {mag:.4f} ∠ {ang:.2f}°\n"

        results += "\n--- Phase Voltages (Va, Vb, Vc) ---\n"
        for bus, ((Va_mag, Va_ang), (Vb_mag, Vb_ang), (Vc_mag, Vc_ang)) in fault_module.phase_voltages.items():
            results += f"{bus}:\n"
            results += f"    Va = {Va_mag:.4f} ∠ {Va_ang:.2f}°\n"
            results += f"    Vb = {Vb_mag:.4f} ∠ {Vb_ang:.2f}°\n"
            results += f"    Vc = {Vc_mag:.4f} ∠ {Vc_ang:.2f}°\n"

        return results


def launch_gui(circuit):
    root = tk.Tk()
    app = PowerSimGUI(root, circuit)
    root.mainloop()
