from Classes.Circuit import Circuit
from Classes.bus import Bus
from Classes.transformer import Transformer
from Classes.transmission_line import TransmissionLine
from Classes.bundle import Bundle
from Classes.geometry import Geometry
from Classes.conductor import Conductor

# Create the Seven Bus Power System (Without Generators)
circuit = Circuit("Seven Bus Power System")

# Define Buses
bus1 = Bus("Bus 1", 20)
bus2 = Bus("Bus 2", 230)
bus3 = Bus("Bus 3", 230)
bus4 = Bus("Bus 4", 230)
bus5 = Bus("Bus 5", 230)
bus6 = Bus("Bus 6", 230)
bus7 = Bus("Bus 7", 18)

# Add Buses to Circuit
circuit.add_bus(bus1)
circuit.add_bus(bus2)
circuit.add_bus(bus3)
circuit.add_bus(bus4)
circuit.add_bus(bus5)
circuit.add_bus(bus6)
circuit.add_bus(bus7)

# Define Transformers
transformer1 = Transformer("T1", bus1, bus2, power_rating=125, impedance_percent=8.5, x_over_r_ratio=10)
transformer2 = Transformer("T2", bus7, bus6, power_rating=200, impedance_percent=10.5, x_over_r_ratio=12)

# Add Transformers to Circuit
circuit.add_transformer(transformer1)
circuit.add_transformer(transformer2)

# Define Conductor & Bundle
conductor = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)
bundle = Bundle("Double", num_conductors=2, spacing=1.5, conductor=conductor)

# Define Geometry
geometry = Geometry("Standard_3Phase", xa=0, ya=0, xb=19.5, yb=0, xc=39, yc=0)

# Define Transmission Lines
L1 = TransmissionLine("L1", bus2, bus4, bundle, geometry, length=10)
L2 = TransmissionLine("L2", bus2, bus3, bundle, geometry, length=25)
L3 = TransmissionLine("L3", bus3, bus5, bundle, geometry, length=20)
L4 = TransmissionLine("L4", bus4, bus6, bundle, geometry, length=20)
L5 = TransmissionLine("L5", bus5, bus6, bundle, geometry, length=10)
L6 = TransmissionLine("L6", bus4, bus5, bundle, geometry, length=35)

# Add Transmission Lines to Circuit
circuit.add_transmission_line(L1)
circuit.add_transmission_line(L2)
circuit.add_transmission_line(L3)
circuit.add_transmission_line(L4)
circuit.add_transmission_line(L5)
circuit.add_transmission_line(L6)

# Display Circuit Network
def display_circuit():
    print(f"\nCircuit Name: {circuit.name}")
    print(f"Total Buses: {len(circuit.buses)}")
    for name, bus in circuit.buses.items():
        print(f"Bus: {name}, Base Voltage: {bus.base_kv} kV")
    for name, transformer in circuit.transformers.items():
        print(f"\nTransformer {name}:\n  - Power Rating: {transformer.power_rating:.4f} MVA\n  - Impedance: {transformer.impedance_percent:.4f}%\n  - X/R Ratio: {transformer.x_over_r_ratio:.4f}\n  - Zt: {transformer.zt:.4f} Ω\n  - Yt: {transformer.yt:.4f} S\n  - Connected between {transformer.bus1.name} and {transformer.bus2.name}")
    for name, line in circuit.transmission_lines.items():
        print(f"\nTransmission Line {name}:\n  - Length: {line.length:.4f} miles\n  - Base Impedance: {line.z_base:.4f} Ω\n  - Base Admittance: {line.y_base:.4f} S\n  - Series Resistance: {line.r_series:.4f} Ω/mi\n  - Series Reactance: {line.x_series:.4f} Ω/mi\n  - Shunt Admittance: {line.b_shunt:.4f} S/mi\n  - Y-Series: {line.y_series:.4f} S\n  - Connected between {line.bus1.name} and {line.bus2.name}")

display_circuit()

