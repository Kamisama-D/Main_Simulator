import numpy as np
import pandas as pd
from Classes.transformer import Transformer
from Classes.transmission_line import TransmissionLine


class Circuit:
    """Represents a power system circuit, storing all components and managing configuration."""

    def __init__(self, name):
        """Initializes the circuit with a name and empty dictionaries for components."""
        self.name = name
        self.buses = {}  # Stores Bus objects
        self.transformers = {}  # Stores Transformer objects
        self.transmission_lines = {}  # Stores TransmissionLine objects

        self.ybus = None

    def add_bus(self, bus):
        """Adds a bus object to the circuit. Raises an error if the bus already exists."""
        if bus.name in self.buses:
            raise ValueError(f"Bus '{bus.name}' already exists in the circuit.")
        self.buses[bus.name] = bus

    def add_transformer(self, transformer):
        """Adds a transformer object to the circuit. Raises an error if the transformer already exists."""
        if transformer.name in self.transformers:
            raise ValueError(f"Transformer '{transformer.name}' already exists in the circuit.")
        self.transformers[transformer.name] = transformer

    def add_transmission_line(self, transmission_line):
        """Adds a transmission line object to the circuit. Raises an error if the line already exists."""
        if transmission_line.name in self.transmission_lines:
            raise ValueError(f"Transmission Line '{transmission_line.name}' already exists in the circuit.")
        self.transmission_lines[transmission_line.name] = transmission_line

    def calc_ybus(self):
        """Computes the system-wide Ybus admittance matrix in per-unit."""
        num_buses = len(self.buses)
        bus_names = list(self.buses.keys())
        # Initialize the Ybus matrix as an N x N zero matrix
        self.ybus = pd.DataFrame(np.zeros((num_buses, num_buses), dtype=complex), index=bus_names, columns=bus_names)

        # Accumulate contributions from all transformers
        for transformer in self.transformers.values():
            yprim_pu = transformer.yprim_pu  # Ensure using per-unit values
            bus1, bus2 = transformer.bus1.name, transformer.bus2.name
            self.ybus.loc[bus1, bus1] += yprim_pu.loc[bus1, bus1]
            self.ybus.loc[bus2, bus2] += yprim_pu.loc[bus2, bus2]
            self.ybus.loc[bus1, bus2] += yprim_pu.loc[bus1, bus2]  # Off-diagonal term
            self.ybus.loc[bus2, bus1] += yprim_pu.loc[bus2, bus1]  # Mutual admittance (negative)

        # Accumulate contributions from all transmission lines
        for line in self.transmission_lines.values():
            yprim_pu = line.yprim_pu  # Ensure using per-unit values
            bus1, bus2 = line.bus1.name, line.bus2.name
            self.ybus.loc[bus1, bus1] += yprim_pu.loc[bus1, bus1]
            self.ybus.loc[bus2, bus2] += yprim_pu.loc[bus2, bus2]
            self.ybus.loc[bus1, bus2] += yprim_pu.loc[bus1, bus2]  # Off-diagonal term
            self.ybus.loc[bus2, bus1] += yprim_pu.loc[bus2, bus1]  # Mutual admittance (negative)

        # Ensure numerical stability by checking that all buses have self-admittance entries
        for bus in bus_names:
            if self.ybus.loc[bus, bus] == 0:
                raise ValueError(f"Numerical instability detected: Bus {bus} has no self-admittance.")

        return self.ybus

    def show_network(self):
        """Displays the network configuration."""
        print(f"\nCircuit Name: {self.name}")
        print("\n--- Buses ---")
        for bus in self.buses.values():
            print(f"{bus.name} - {bus.base_kv} kV")
        print("\n--- Transformers ---")
        for transformer in self.transformers.values():
            print(f"{transformer.name}: {transformer.bus1.name} ↔ {transformer.bus2.name}")
        print("\n--- Transmission Lines ---")
        for line in self.transmission_lines.values():
            print(f"{line.name}: {line.bus1.name} ↔ {line.bus2.name}")

    def show_ybus(self):
        """Displays the Ybus matrix if it has been calculated."""
        if self.ybus is None:
            print("Ybus has not been calculated. Run calc_ybus() first.")
        else:
            print("\n--- Ybus Admittance Matrix ---")
            #print(self.ybus.map(lambda x: f"{x.real:.6f} {'+' if x.imag >= 0 else '-'} j{x.imag:.6f}"))
            print(self.ybus)
