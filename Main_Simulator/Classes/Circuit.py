class Circuit:
    """Represents a power system circuit, storing all components and managing configuration."""

    def __init__(self, name):
        """Initializes the circuit with a name and empty dictionaries for components."""
        self.name = name
        self.buses = {}  # Stores Bus objects
        self.transformers = {}  # Stores Transformer objects
        self.transmission_lines = {}  # Stores TransmissionLine objects

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

    def show_network(self):
        """Displays the network configuration."""
        print(f"\nCircuit Name: {self.name}")
        print("Buses:", list(self.buses.keys()))
        print("Transformers:", list(self.transformers.keys()))
        print("Transmission Lines:", list(self.transmission_lines.keys()))
