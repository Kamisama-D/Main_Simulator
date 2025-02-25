from Classes.Circuit import Circuit
from Classes.bus import Bus
from Classes.transformer import Transformer
from Classes.transmission_line import TransmissionLine
from Classes.bundle import Bundle
from Classes.geometry import Geometry
from Classes.conductor import Conductor
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

#User defined power base and frequency
s_base=100 #MVA
f_base = 60  # Hz

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
transformer1 = Transformer("T1", bus1, bus2, power_rating=125, impedance_percent=8.5, x_over_r_ratio=10, s_base=s_base)
transformer2 = Transformer("T2", bus7, bus6, power_rating=200, impedance_percent=10.5, x_over_r_ratio=12, s_base=s_base)

# Add Transformers to Circuit
circuit.add_transformer(transformer1)
circuit.add_transformer(transformer2)

# Define Conductor & Bundle
conductor = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)
bundle = Bundle("Double", num_conductors=2, spacing=1.5, conductor=conductor)

# Define Geometry
geometry = Geometry("Standard_3Phase", xa=0, ya=0, xb=19.5, yb=0, xc=39, yc=0)

# Define Transmission Lines
L1 = TransmissionLine("L1", bus2, bus4, bundle, geometry, length=10, s_base=s_base, frequency=f_base)
L2 = TransmissionLine("L2", bus2, bus3, bundle, geometry, length=25, s_base=s_base, frequency=f_base)
L3 = TransmissionLine("L3", bus3, bus5, bundle, geometry, length=20, s_base=s_base, frequency=f_base)
L4 = TransmissionLine("L4", bus4, bus6, bundle, geometry, length=20, s_base=s_base, frequency=f_base)
L5 = TransmissionLine("L5", bus5, bus6, bundle, geometry, length=10, s_base=s_base, frequency=f_base)
L6 = TransmissionLine("L6", bus4, bus5, bundle, geometry, length=35, s_base=s_base, frequency=f_base)

# Add Transmission Lines to Circuit
circuit.add_transmission_line(L1)
circuit.add_transmission_line(L2)
circuit.add_transmission_line(L3)
circuit.add_transmission_line(L4)
circuit.add_transmission_line(L5)
circuit.add_transmission_line(L6)

# Display Circuit Network
def display_circuit():
    print(f"\n--- Circuit Name: {circuit.name} ---")
    print(f"Total Buses: {len(circuit.buses)}")

    # Display Buses
    for name, bus in circuit.buses.items():
        print(f"Bus: {name}, Base Voltage: {bus.base_kv} kV")

    # Display Transformers
    for name, transformer in circuit.transformers.items():
        print(f"\n--- Transformer {name} ---")
        print(f"  - Power Rating: {transformer.power_rating:.4f} MVA")
        print(f"  - X/R Ratio: {transformer.x_over_r_ratio:.4f}")
        print(f"  - System Base Power: {transformer.s_base:.4f} MVA")
        print(f"  - Base Impedance (Transformer): {transformer.z_base_xfmr:.4f} Ω")
        print(f"  - Base Impedance (System): {transformer.z_base_sys:.4f} Ω")

        print(f"\n  --- Impedance & Admittance Values ---")
        print(f"  - Z_pu_xfmr: {transformer.z_pu_xfmr:.4f} pu")
        print(f"  - Z_t (Impedance in Ohms): {transformer.zt:.4f} Ω")
        print(f"  - Z_pu_sys: {transformer.z_pu_sys:.4f} pu")
        print(f"  - Y_t (Admittance in Siemens): {transformer.yt:.4f} S")
        print(f"  - Y_pu_sys: {transformer.y_pu_sys:.4f} pu")

        print(f"\n  --- Resistance & Reactance Values ---")
        print(f"  - R_t (Resistance in Ohms): {transformer.zt.real:.4f} Ω")
        print(f"  - X_t (Reactance in Ohms): {transformer.zt.imag:.4f} Ω")
        print(f"  - R_pu_sys: {transformer.z_pu_sys.real:.4f} pu")
        print(f"  - X_pu_sys: {transformer.z_pu_sys.imag:.4f} pu")

        print(f"\n  --- Y-Primitive Matrix (Yprim) [Siemens] ---")
        # print(f"  [{transformer.yprim.iloc[0, 0]:.4f}, {transformer.yprim.iloc[0, 1]:.4f}]")
        # print(f"  [{transformer.yprim.iloc[1, 0]:.4f}, {transformer.yprim.iloc[1, 1]:.4f}]")
        print(transformer.yprim)

        print(f"\n  --- Y-Primitive Matrix (Yprim_pu) [Per Unit] ---")
        # print(f"  [{transformer.yprim_pu.iloc[0, 0]:.4f}, {transformer.yprim_pu.iloc[0, 1]:.4f}]")
        # print(f"  [{transformer.yprim_pu.iloc[1, 0]:.4f}, {transformer.yprim_pu.iloc[1, 1]:.4f}]")
        print(transformer.yprim_pu)

    # Display Transmission Lines
    for name, line in circuit.transmission_lines.items():
        print(f"\n--- Transmission Line {name} ---")
        print(f"  - Connected between: {line.bus1.name} - {line.bus2.name}")
        print(f"  - Length: {line.length:.4f} miles")
        print(f"  - Frequency: {line.frequency:.2f} Hz")

        print(f"\n  --- Base Values ---")
        print(f"  - s_base: {line.s_base:.4f} MVA")
        print(f"  - v_base: {line.v_base:.4f} kV")
        print(f"  - z_base_sys: {line.z_base_sys:.4f} Ω")

        print(f"\n  --- Impedance & Admittance Values ---")
        print(f"  - z_series: {abs(line.z_series):.4f} Ω")
        print(f"  - z_pu_sys: {abs(line.z_pu_sys):.4f} pu")
        print(f"  - y_series: {abs(line.y_series):.4f} S")
        print(f"  - y_pu_sys: {abs(line.y_pu_sys):.4f} pu")

        print(f"\n  --- Resistance & Reactance Values ---")
        print(f"  - r_series: {line.r_series:.4f} Ω")
        print(f"  - r_series_pu: {abs(line.z_pu_sys.real):.4f} pu")
        print(f"  - x_series: {line.x_series:.4f} Ω")
        print(f"  - x_series_pu: {abs(line.z_pu_sys.imag):.4f} pu")

        print(f"\n  --- Shunt Admittance ---")
        print(f"  - b_shunt: {line.b_shunt:.4f} S")
        print(f"  - b_shunt_pu: {line.b_shunt / line.y_base_sys:.4f} pu")

        print(f"\n  --- Y-Primitive Matrix (Yprim) [Siemens] ---")
        # print(f"  [{line.yprim.iloc[0, 0]:.4f}, {line.yprim.iloc[0, 1]:.4f}]")
        # print(f"  [{line.yprim.iloc[1, 0]:.4f}, {line.yprim.iloc[1, 1]:.4f}]")
        print(line.yprim)

        print(f"\n  --- Y-Primitive Matrix (Yprim_pu) [Per Unit] ---")
        # print(f"  [{line.yprim_pu.iloc[0, 0]:.4f}, {line.yprim_pu.iloc[0, 1]:.4f}]")
        # print(f"  [{line.yprim_pu.iloc[1, 0]:.4f}, {line.yprim_pu.iloc[1, 1]:.4f}]")
        print(line.yprim_pu)

    # Display Circuit Ybus
    circuit.calc_ybus()
    circuit.show_ybus()

# Run Display Function
display_circuit()


