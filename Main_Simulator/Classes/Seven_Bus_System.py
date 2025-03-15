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
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Create the Seven Bus Power System (Without Generators)
circuit = Circuit("Seven Bus Power System")

# Define Buses
bus1 = Bus("Bus 1", 20, vpu=1.0, delta=0.0)  # Slack Bus
bus2 = Bus("Bus 2", 230, P=0, Q=0)
bus3 = Bus("Bus 3", 230, P=110, Q=50)
bus4 = Bus("Bus 4", 230, P=100, Q=70)
bus5 = Bus("Bus 5", 230, P=100, Q=65)
bus6 = Bus("Bus 6", 230, P=0, Q=0)
bus7 = Bus("Bus 7", 18, P=0, vpu=1.0)  # PV Bus

# Add Buses to Circuit
circuit.add_bus(bus1)
circuit.add_bus(bus2)
circuit.add_bus(bus3)
circuit.add_bus(bus4)
circuit.add_bus(bus5)
circuit.add_bus(bus6)
circuit.add_bus(bus7)

# Define Transformers
transformer1 = Transformer("T1", bus1, bus2, power_rating=125, impedance_percent=8.5, x_over_r_ratio=10, s_base=100)
transformer2 = Transformer("T2", bus7, bus6, power_rating=200, impedance_percent=10.5, x_over_r_ratio=12, s_base=100)

# Add Transformers to Circuit
circuit.add_transformer(transformer1)
circuit.add_transformer(transformer2)

# Define Conductor & Bundle
conductor = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)
bundle = Bundle("Double", num_conductors=2, spacing=1.5, conductor=conductor)

# Define Geometry
geometry = Geometry("Standard_3Phase", xa=0, ya=0, xb=19.5, yb=0, xc=39, yc=0)

# Define Transmission Lines
L1 = TransmissionLine("L1", bus2, bus4, bundle, geometry, length=10, s_base=100, frequency=60)
L2 = TransmissionLine("L2", bus2, bus3, bundle, geometry, length=25, s_base=100, frequency=60)
L3 = TransmissionLine("L3", bus3, bus5, bundle, geometry, length=20, s_base=100, frequency=60)
L4 = TransmissionLine("L4", bus4, bus6, bundle, geometry, length=20, s_base=100, frequency=60)
L5 = TransmissionLine("L5", bus5, bus6, bundle, geometry, length=10, s_base=100, frequency=60)
L6 = TransmissionLine("L6", bus4, bus5, bundle, geometry, length=35, s_base=100, frequency=60)

# Add Transmission Lines to Circuit
circuit.add_transmission_line(L1)
circuit.add_transmission_line(L2)
circuit.add_transmission_line(L3)
circuit.add_transmission_line(L4)
circuit.add_transmission_line(L5)
circuit.add_transmission_line(L6)

# Define Generators
gen1 = Generator("G1", bus1, voltage_setpoint=1.0, mw_setpoint=0)  # Slack Generator
gen2 = Generator("G2", bus7, voltage_setpoint=1.0, mw_setpoint=200)

# Define System Settings
settings = SystemSettings(circuit.ybus, list(circuit.buses.values()))

circuit.calc_ybus()

# Display Circuit Ybus
circuit.show_ybus()

# Run Power Flow Solver
power_flow_solver = PowerFlowSolver(circuit)
success = power_flow_solver.solve_power_flow(tolerance=0.0001)

if success:
    print("[INFO] Power Flow Analysis Completed Successfully")
else:
    print("[WARNING] Power Flow Did Not Converge")







