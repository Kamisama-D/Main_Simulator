import numpy as np
import pandas as pd
from Classes.transformer import Transformer
from Classes.transmission_line import TransmissionLine
from Classes.generator import Generator
from Classes.load import Load
from Classes.system_setting import SystemSettings


class Circuit:
    """Represents a power system circuit, storing all components and managing configuration."""

    def __init__(self, name, system_settings: SystemSettings):
        """Initializes the circuit with a name and empty dictionaries for components."""
        self.name = name
        self.settings = system_settings
        self.buses = {}  # Stores Bus objects
        self.bus_type = {}  # Initialize the bus type dictionary
        self.transformers = {}  # Stores Transformer objects
        self.transmission_lines = {}  # Stores TransmissionLine objects
        self.generators = {}  # Stores Generator objects
        self.loads = {}  # Stores Load objects

        self.ybus: pd.DataFrame = None  # Explicitly hinting it's a DataFrame

    def add_bus(self, bus):
        """Adds a bus object to the circuit. Raises an error if the bus already exists."""
        if bus.name in self.buses:
            raise ValueError(f"Bus '{bus.name}' already exists in the circuit.")
        self.buses[bus.name] = bus
        self.bus_type[bus.name] = bus.bus_type

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

    # def add_generator(self, generator):
    #     """Adds a generator object to the circuit and updates the corresponding bus."""
    #     if generator.name in self.generators:
    #         raise ValueError(f"Generator '{generator.name}' already exists in the circuit.")
    #     self.generators[generator.name] = generator
    #     generator.bus.add_generator(generator)  # Associate with the correct bus

    def add_generator(self, generator):
        """Adds a generator object to the circuit and updates the corresponding bus."""
        if generator.name in self.generators:
            raise ValueError(f"Generator '{generator.name}' already exists in the circuit.")

        # Add generator to circuit storage
        self.generators[generator.name] = generator

        # Ensure generator is assigned to the bus
        bus = self.buses[generator.bus.name]
        if generator not in bus.generators:  # ✅ Prevent duplicate assignments
            bus.generators.append(generator)

        # ✅ Update bus type after adding generator
        bus.update_bus_type()

        print(f"[DEBUG] Generator '{generator.name}' added to {bus.name}. Bus Type Updated: {bus.bus_type}")

    def add_load(self, load):
        """Adds a load object to the circuit and updates the corresponding bus."""
        if load.name in self.loads:
            raise ValueError(f"Load '{load.name}' already exists in the circuit.")
        self.loads[load.name] = load
        load.bus.add_load(load)  # Associate with the correct bus

    def calc_ybus(self):
        """Computes the system-wide Ybus admittance matrix in per-unit."""
        num_buses = len(self.buses)
        bus_names = list(self.buses.keys())
        # Initialize the Ybus matrix as an N x N zero matrix
        self.ybus = pd.DataFrame(np.zeros((num_buses, num_buses), dtype=complex), index=bus_names, columns=bus_names)

        # Accumulate contributions from all transformers
        for transformer in self.transformers.values():
            yprim_pu = transformer.yprim_pu  # Ensure using per-unit values
            if not isinstance(yprim_pu, pd.DataFrame):
                raise TypeError(f"{transformer.name} yprim_pu is not a DataFrame!")
            bus1, bus2 = transformer.bus1.name, transformer.bus2.name
            self.ybus.loc[bus1, bus1] += yprim_pu.loc[bus1, bus1]
            self.ybus.loc[bus2, bus2] += yprim_pu.loc[bus2, bus2]
            self.ybus.loc[bus1, bus2] += yprim_pu.loc[bus1, bus2]  # Off-diagonal term
            self.ybus.loc[bus2, bus1] += yprim_pu.loc[bus2, bus1]  # Mutual admittance (negative)

        # Accumulate contributions from all transmission lines
        for line in self.transmission_lines.values():
            yprim_pu = line.yprim_pu  # Ensure using per-unit values
            if not isinstance(yprim_pu, pd.DataFrame):
                raise TypeError(f"{line.name} yprim_pu is not a DataFrame!")
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

    def get_base_power(self):
        """Returns the base power of the system."""
        return self.settings.base_power

    def get_frequency(self):
        """Returns the system frequency."""
        return self.settings.frequency

    def bus_order(self):
        """Returns the ordered list of bus names."""
        return list(self.buses.keys())

    def bus_types(self):
        """Returns a dictionary mapping bus names to their types."""
        return {bus.name: bus.bus_type for bus in self.buses.values()}

    def real_power_vector(self):
        """Computes the real power vector (P) from all buses."""
        return {bus.name: sum(load.real_power for load in bus.loads) for bus in self.buses.values()}

    def reactive_power_vector(self):
        """Computes the reactive power vector (Q) from all buses."""
        return {bus.name: sum(load.reactive_power for load in bus.loads) for bus in self.buses.values()}

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
        print("\n--- Generators ---")
        for generator in self.generators.values():
            print(f"{generator.name}: Connected to {generator.bus.name}, MW Setpoint: {generator.mw_setpoint} MW")
        print("\n--- Loads ---")
        for load in self.loads.values():
            print(
                f"{load.name}: Connected to {load.bus.name}, Real Power: {load.real_power} MW, Reactive Power: {load.reactive_power} Mvar")


    def show_ybus(self):
        """Displays the Ybus matrix if it has been calculated."""
        if self.ybus is None:
            print("Ybus has not been calculated. Run calc_ybus() first.")
        else:
            print("\n--- Ybus Admittance Matrix ---")
            #print(self.ybus.map(lambda x: f"{x.real:.6f} {'+' if x.imag >= 0 else '-'} j{x.imag:.6f}"))
            print(self.ybus)


