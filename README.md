# ⚡ DC Power Flow Enhancement – Project 3 (ECE 2774)

This project enhances a Python-based power system simulator by implementing a **DC Power Flow** module using the linearized \( B\theta = P \) model. The enhancement enables scalable analysis of real power flows across buses with high computational efficiency, and has been validated through manual calculations and comparison with PowerWorld simulations.

---

## 📘 Purpose and Theory

DC Power Flow is a simplified model used widely in planning and analysis. It is based on the following assumptions:

- Flat voltage profile: \( |V| = 1.0 \) p.u.
- Small angle differences: \( \sin(\delta_i - \delta_j) \approx \delta_i - \delta_j \)
- Negligible resistance
- Only real power is modeled

### Core Equation:
\[
\boldsymbol{\delta} = B'^{-1} \cdot \mathbf{P}
\]
Where:
- \( B' \) is the reduced susceptance matrix (imaginary part of Ybus without the slack bus),
- \( P \) is the net real power injection vector (in p.u.),
- \( \delta \) is the bus voltage angle vector.

---

## 🛠 Implementation Overview

### 🧱 New Class: `DCPowerFlowSolver`
- Automatically builds \( B' \) and \( P \)
- Solves for \( \delta \) using NumPy
- Prints voltage angles in radians and degrees

### 🔄 Circuit Class Enhancements
Added methods to retrieve total power per bus:
```python
def get_bus_generation(self, bus_name)
def get_bus_load(self, bus_name)
```

### 🧪 Running the Solver
To run the DC power flow for any system:
```python
dc_solver = DCPowerFlowSolver(circuit)
dc_solver.solve()
dc_solver.display_results()
```

---

## 🧪 Testing and Validation

### ✅ Test Case 1: 3-Bus System (Manual Validation)
- Small test system manually solved using MATLAB
- Matrix B′ and vector P were defined explicitly
- Python simulation output matched manual solution:
  - \( \theta_2 = -4.3409^\circ \)
  - \( \theta_3 = -6.3111^\circ \)
- Error < 0.005°

### ✅ Test Case 2: 7-Bus System (PowerWorld Validation)
- Full 7-bus network (same from Project 2) tested
- DC Power Flow mode used in PowerWorld
- Python and PowerWorld angle results matched exactly
- Error < 0.01° at all buses


### 📂 File Overview
- `DCPowerFlowSolver.py`: DC flow module
- `Circuit.py`: System manager
- `Seven_Bus_System.py`: Main example test case
- `Three_Bus_Test.py`: Manual validation case

### ▶️ Run
```bash
python Seven_Bus_System.py
```

---

## 📚 References

- J. D. Glover, T. J. Overbye, M. S. Sarma, *Power System Analysis and Design*, 6th ed.
- IEEE Std 399-1997 (Brown Book)
- PowerWorld Simulator Documentation
