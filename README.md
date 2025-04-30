# Project 3: Power System Simulation GUI – Seven Bus System Enhancement

## 🧩 Purpose and Theoretical Background

This enhancement introduces a graphical user interface (GUI) to the Seven Bus System simulator using Python’s `tkinter` library. The GUI provides a user-friendly environment to perform power flow analysis and fault studies (SLG, LL, DLG, 3-phase faults) without requiring code modification. This interface simulates professional tools such as PowerWorld and facilitates interactive learning and testing for students and power system engineers.

Power flow analysis determines the steady-state voltage magnitude and angle at each bus in a power system and is essential for operation, planning, and economic dispatch. Fault analysis evaluates the response of a power system under different fault types by computing fault currents and post-fault voltages using symmetrical component theory and network impedance matrices. These tools help engineers design protection schemes and assess system reliability.

The GUI enhancement makes these complex analyses accessible to users unfamiliar with scripting and supports educational use cases by improving usability, interaction, and error reduction.

---

## 🛠️ How It Works

- Users can view system configuration (buses, generators, loads, transformers, and lines).
- Two analysis modes:
  - **Power Flow**: Computes voltage magnitudes and angles at each bus.
  - **Fault Study**: Simulates fault conditions (SLG, LL, DLG, 3ph) at selected buses and returns fault current and post-fault voltages.
- Inputs are collected via dropdown menus and radiobuttons.
- Results are displayed in a scrollable text area in the GUI.

---

## 🧾 Inputs and Outputs

### Inputs

| Parameter     | Description                            |
|---------------|----------------------------------------|
| Analysis Mode | `Power Flow` or `Fault Study`          |
| Fault Type    | SLG, LL, DLG, 3PH (for Fault Study)    |
| Faulted Bus   | Any of the defined buses (e.g., Bus 5) |

### Outputs

- **Power Flow Mode**:
  - Bus voltage magnitudes (p.u.)
  - Bus voltage angles (degrees)
- **Fault Study Mode**:
  - Fault current magnitude and angle
  - Post-fault phase voltages (Va, Vb, Vc)
  - Per-phase fault current (if applicable)

---

## ▶️ How to Run

1. Ensure you have Python and `tkinter` installed.
2. Define the circuit and all components in `Seven_Bus_System.py`.
3. At the end of `Seven_Bus_System.py`, run the following line:

```python
launch_gui(circuit)
