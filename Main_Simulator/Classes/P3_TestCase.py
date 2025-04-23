from Classes.Circuit import Circuit
from Classes.FaultStudySolver import FaultStudySolver
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
import numpy as np
from MainSolver import Solver
from pprint import pprint
from DCPowerFlowSolver import DCPowerFlowSolver

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


# Add Buses to Circuit
for bus in [bus1, bus2, bus3]:
    circuit.add_bus(bus)

# Define Loads
load3 = Load("Load 3", bus3, real_power=110, reactive_power=50)


# Add Loads to Circuit
for load in [load3]:
    circuit.add_load(load.name, load.bus.name, load.real_power, load.reactive_power)

# Define Generators
circuit.add_generator("G1", "Bus 1", per_unit=1.0, real_power=0, x1=0.12, x2=0.14, x0=0.05, is_grounded=True, grounding_impedance_ohm=0.0, connection_type="wye")     # Slack



# Define Transformers
transformer1 = Transformer("T1", bus1, bus2, power_rating=125, impedance_percent=8.5, x_over_r_ratio=10, s_base=s_base,
                           grounding_impedance_ohm_bus1=0.0, grounding_impedance_ohm_bus2=1.0, primary_connection_type="delta", secondary_connection_type="wye",
                           is_grounded_bus1=False, is_grounded_bus2=True)


# Add Transformers to Circuit
for transformer in [transformer1]:
    circuit.add_transformer(transformer)

# Define Conductor & Bundle
conductor = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)
bundle = Bundle("Double", num_conductors=2, spacing=1.5, conductor=conductor)

# Define Geometry
geometry = Geometry("Standard_3Phase", xa=0, ya=0, xb=19.5, yb=0, xc=39, yc=0)

# Define Transmission Lines
lines = [

    TransmissionLine("L2", bus2, bus3, bundle, geometry, length=25, s_base=s_base, frequency=frequency, connection_type="untransposed", zero_seq_model="enabled"),
    ]

# Add Transmission Lines to Circuit
for line in lines:
    circuit.add_transmission_line(line)


# Calculate Ybus and Display It
Ybus = circuit.calc_ybus()
print("\n--- Ybus (for Power Flow Analysis) ---")
print(Ybus)




# Comment/uncomment depending on which analysis you want to run.
from MainSolver import Solver

# # Example for Power Flow Analysis
# solver = Solver(circuit, analysis_mode='pf')
# solver.run()

# # Run Line-to-Ground (SLG) Fault at Bus 5
# fault_solver = Solver(circuit, analysis_mode='fault', faulted_bus="Bus 5", fault_type="slg", fault_impedance=0.0)
# fault_solver.run()


# # Example for 3 Phase (3ph) Fault at Bus 5
# fault_solver = Solver(circuit, analysis_mode='fault', faulted_bus="Bus 1", fault_type="3ph")
# fault_solver.run()

# Or for Line-to-Line (LL) Fault at Bus 3
# fault_solver = Solver(circuit, analysis_mode='fault', faulted_bus="Bus 3", fault_type="ll")
# fault_solver.run()
#
# # Or for Double-Line-to-Ground (DLG) Fault at Bus 6
# fault_solver = Solver(circuit, analysis_mode='fault', faulted_bus="Bus 5", fault_type="dlg")
# fault_solver.run()

# Run DC Power Flow
dc_solver = DCPowerFlowSolver(circuit)
dc_solver.solve()
dc_solver.display_results()
