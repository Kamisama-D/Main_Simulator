# ⚡ DC Power Flow Enhancement – Project 3 (ECE 2774)

This project enhances a Python-based power system simulator by implementing a **DC Power Flow** module using the linearized Bθ = P model. The enhancement enables scalable analysis of real power flows across buses with high computational efficiency, and has been validated through manual and PowerWorld simulations.

---

## 📘 Purpose and Theory

DC Power Flow is a simplified model based on the assumptions:

- Flat voltage profile: |V| = 1.0 p.u.
- Small angle differences: sin(δi - δj) ≈ δi - δj
- Negligible resistance
- Real power flow only (no reactive power or voltage magnitude equations)

**Equation:**
\[
\boldsymbol{\delta} = -B'^{-1} \cdot \mathbf{P}
\]

Where B' is the reduced susceptance matrix and P is the net real power injection vector.

---

## 🛠 Implementation

### 🔹 New Class: `DCPowerFlowSolver`
- Constructs B′ from the Ybus imaginary part
- Builds the P vector using new methods in `Circuit.py`
- Solves for θ, restores slack bus angle, and prints results in degrees

### 🔹 Circuit Class Enhancements
```python
def get_bus_generation(self, bus_name)
def get_bus_load(self, bus_name)

