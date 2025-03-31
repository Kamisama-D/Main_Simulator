from Classes.Circuit import Circuit
from Classes.bus import Bus
from Classes.transformer import Transformer
from Classes.transmission_line import TransmissionLine
from Classes.bundle import Bundle
from Classes.geometry import Geometry
from Classes.conductor import Conductor
from Classes.system_setting import SystemSettings
from Classes.PowerFlowSolver import PowerFlowSolver  # Import power flow solver
from Classes.generator import Generator  # Import Generator
from Classes.load import Load
from Classes.Newton_Raphson import NewtonRaphson
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Initialize System Settings
system_settings = SystemSettings(frequency=60, base_power=100)

# Create the Seven Bus Power System
circuit = Circuit("Seven Bus Power System", system_settings)

# Retrieve system settings from the circuit
s_base = system_settings.base_power
frequency = system_settings.frequency

# Define Buses
bus1 = Bus("Bus 1", 20)  # Slack Bus
bus2 = Bus("Bus 2", 230)
bus3 = Bus("Bus 3", 230)
bus4 = Bus("Bus 4", 230)
bus5 = Bus("Bus 5", 230)
bus6 = Bus("Bus 6", 230)
bus7 = Bus("Bus 7", 18)  # PV Bus

# Add Buses to Circuit
for bus in [bus1, bus2, bus3, bus4, bus5, bus6, bus7]:
    circuit.add_bus(bus)

# Define Loads
load3 = Load("Load 3", bus3, real_power=110, reactive_power=50)
load4 = Load("Load 4", bus4, real_power=100, reactive_power=70)
load5 = Load("Load 5", bus5, real_power=100, reactive_power=65)

# Add Loads to Circuit
for load in [load3, load4, load5]:
    circuit.add_load(load.name, load.bus.name, load.real_power, load.reactive_power)

# Define Generators
circuit.add_generator("G1", "Bus 1", per_unit=1.0, real_power=0)     # Slack
circuit.add_generator("G2", "Bus 7", per_unit=1.0, real_power=200)   # PV


# Define Transformers
transformer1 = Transformer("T1", bus1, bus2, power_rating=125, impedance_percent=8.5, x_over_r_ratio=10, s_base=s_base)
transformer2 = Transformer("T2", bus7, bus6, power_rating=200, impedance_percent=10.5, x_over_r_ratio=12, s_base=s_base)

# Add Transformers to Circuit
for transformer in [transformer1, transformer2]:
    circuit.add_transformer(transformer)

# Define Conductor & Bundle
conductor = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)
bundle = Bundle("Double", num_conductors=2, spacing=1.5, conductor=conductor)

# Define Geometry
geometry = Geometry("Standard_3Phase", xa=0, ya=0, xb=19.5, yb=0, xc=39, yc=0)

# Define Transmission Lines
lines = [
    TransmissionLine("L1", bus2, bus4, bundle, geometry, length=10, s_base=s_base, frequency=frequency),
    TransmissionLine("L2", bus2, bus3, bundle, geometry, length=25, s_base=s_base, frequency=frequency),
    TransmissionLine("L3", bus3, bus5, bundle, geometry, length=20, s_base=s_base, frequency=frequency),
    TransmissionLine("L4", bus4, bus6, bundle, geometry, length=20, s_base=s_base, frequency=frequency),
    TransmissionLine("L5", bus5, bus6, bundle, geometry, length=10, s_base=s_base, frequency=frequency),
    TransmissionLine("L6", bus4, bus5, bundle, geometry, length=35, s_base=s_base, frequency=frequency)
]

# Add Transmission Lines to Circuit
for line in lines:
    circuit.add_transmission_line(line)

# Calculate Ybus and Display It
circuit.calc_ybus()
circuit.show_ybus()

# Run Power Flow Solver
power_flow_solver = PowerFlowSolver(1, circuit)

# Show key power flow vectors
print("\nVector x (State Variables):", power_flow_solver.initialize_x())
print("\nVector y (Expected Power Injections):", power_flow_solver.initialize_y())
print("\nVector yx (Calculated Power Injections):", power_flow_solver.calc_Px(), power_flow_solver.calc_Qx())
print("\nMismatch Vector Δy:", power_flow_solver.del_y)

# Newton-Raphson Solution
newton_solver = NewtonRaphson(power_flow_solver)
converged = newton_solver.solve(tol=0.001, max_iter=50)
if converged:
    print("\nNewton-Raphson converged successfully.")
else:
    print("\nNewton-Raphson did not converge.")

# Display final state variables after convergence:
print("\nFinal Voltage Magnitudes:")
for bus in circuit.bus_order():
    print(f"{bus}: {power_flow_solver.voltage[bus]:.4f}")

print("\nFinal Voltage Angles (radians):")
for bus in circuit.bus_order():
    print(f"{bus}: {power_flow_solver.delta[bus]:.4f}")