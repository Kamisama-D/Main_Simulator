# ⚡ Modular Power System Simulator

## Overview

The **Modular Power System Simulator** is a Python-based application designed to model and analyze multi-bus transmission networks under both balanced and unbalanced operating conditions. Developed with an object-oriented programming (OOP) approach, the simulator emphasizes modularity, accuracy, and extensibility.

It supports detailed power flow studies and fault simulations using per-unit modeling and the method of symmetrical components. This tool is ideal for academic research, education, and prototyping of power system behavior.

---

## Features

- **Power Flow Analysis**: Solves nonlinear power flow equations using the Newton-Raphson method with PV, PQ, and slack bus support.
- **Fault Study Engine**: Simulates 3-phase, SLG, LL, and DLG faults using sequence networks and Zbus matrices.
- **Sequence Network Modeling**: Automatically constructs Ybus/Zbus matrices for all three symmetrical components.
- **Transformer Grounding & Shift Modeling**: Handles complex transformer configurations and grounding impedances.
- **Scalable Architecture**: Easy to add new buses, lines, transformers, and custom models.
- **Validated Results**: Matched against PowerWorld outputs for steady-state voltages and fault currents.

---

## Project Structure

### Circuit Definition Layer

- `bus.py` – Bus model with voltage and type tracking.
- `load.py` – Constant power load modeling.
- `generator.py` – Generator model with sequence impedance and grounding.
- `transformer.py` – Delta/Wye transformers with impedance and shift behavior.
- `transmission_line.py` – Line model with bundled conductors and geometry.
- `conductor.py`, `bundle.py`, `geometry.py` – Physical models for impedance calculation.
- `Circuit.py` – System manager: buses, components, and Ybus calculation.

### Circuit Computation Layer

- `system_setting.py` – Base values and global tolerances.
- `Newton_Raphson.py`, `Jacobians.py` – Power flow algorithm.
- `PowerFlowSolver.py` – Orchestrates full NR power flow.
- `FaultStudySolver.py` – Executes 3ph, SLG, LL, and DLG fault simulations.

### Execution Layer

- `Seven_Bus_System.py` – Main file for defining the case and executing analyses.
- `MainSolver.py` – Dispatches solver logic per selected analysis mode.

---

## Usage Guide

1. **Define the system** in `Seven_Bus_System.py` using the `Circuit` class.
2. **Choose analysis mode**:
   ```python
   solver = Solver(circuit, analysis_mode='pf')  # for power flow
   solver = Solver(circuit, analysis_mode='fault', faulted_bus="Bus 5", fault_type="slg")

## Documentation

The complete technical manual is available in the repository under **Documentation.pdf**. This document includes:

- **Theoretical background**
- **Project architecture**
- **Implementation details**
- **Usage examples**
- **Test case**

---

## Contributing

Contributions are welcome! Fork the repository, create a branch, and submit a pull request.

---

## References

1. *Learning Python, 5th Edition*, Mark Lutz.
2. *A Novel Approach to Teaching Power Systems Analysis and Design Using Software Development*, IEEE paper.
3. [How to Write Software Documentation](https://technicalwriterhq.com/documentation/software-documentation/how-to-write-software-documentation/)
4. Milestone-specific details: **Seven Bus System - Milestone 1 through 11**.
