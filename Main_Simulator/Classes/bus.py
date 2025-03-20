class Bus:
    count = 0
    slack_assigned = False  # Ensures only one slack bus is assigned

    def __init__(self, name: str, base_kv: float, vpu: float = None, delta: float = None):
        """
        Initializes a Bus object and classifies its type automatically.
        """
        self.name = name
        self.base_kv = base_kv
        self.index = Bus.count
        Bus.count += 1

        self.vpu = vpu if vpu is not None else 1.0  # Default voltage magnitude
        self.delta = delta if delta is not None else 0.0  # Default voltage angle

        self.generators = []  # List of connected generators
        self.loads = []  # List of connected loads

        # Assign initial bus type dynamically
        self.bus_type = None
        self.update_bus_type()

    # def update_bus_type(self):
    #     """
    #     Determines the bus type dynamically based on connected components.
    #     - Slack Bus: Manually assigned, only one allowed.
    #     - PV Bus: If a generator is connected.
    #     - PQ Bus: If only loads are connected.
    #     """
    #     if not Bus.slack_assigned and self.vpu == 1.0 and self.delta == 0.0:
    #         self.bus_type = "Slack Bus"
    #         Bus.slack_assigned = True
    #     elif self.generators:
    #         self.bus_type = "PV Bus"
    #     else:
    #         self.bus_type = "PQ Bus"

    def update_bus_type(self):
        """
        Determines the bus type dynamically based on connected components.
        - Slack Bus: Manually assigned, only one allowed.
        - PV Bus: If a generator is connected.
        - PQ Bus: If only loads are connected.
        """
        if not Bus.slack_assigned and self.vpu == 1.0 and self.delta == 0.0:
            self.bus_type = "Slack Bus"
            Bus.slack_assigned = True
        elif len(self.generators) > 0:  # ✅ Ensure generators are correctly assigned
            self.bus_type = "PV Bus"
        else:
            self.bus_type = "PQ Bus"

        # ✅ Debug to confirm correct classification
        print(f"[DEBUG] Bus {self.name} classified as {self.bus_type}, Generators: {len(self.generators)}")

    def add_generator(self, generator):
        """Adds a generator to the bus and updates the bus type."""
        self.generators.append(generator)
        self.update_bus_type()

    def add_load(self, load):
        """Adds a load to the bus and updates the bus type."""
        self.loads.append(load)
        self.update_bus_type()

    def total_real_power(self):
        """Calculates total real power at the bus from all connected loads."""
        return sum(load.real_power for load in self.loads)

    def total_reactive_power(self):
        """Calculates total reactive power at the bus from all connected loads."""
        return sum(load.reactive_power for load in self.loads)

    def __repr__(self):
        """Returns a formatted string representation of the Bus object."""
        return (f"Bus(name='{self.name}', base_kv={self.base_kv}, index={self.index}, "
                f"vpu={self.vpu}, delta={self.delta}, bus_type='{self.bus_type}', "
                f"total_real_power={self.total_real_power()} MW, total_reactive_power={self.total_reactive_power()} Mvar)")







