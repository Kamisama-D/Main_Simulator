class Bus:
    count = 0
    bus_types = {"Slack Bus", "PQ Bus", "PV Bus"}
    slack_assigned = False  # Class variable to ensure only one Slack Bus exists.

    def __init__(self, name:str, base_kv:float,  bus_type:str, P:float = None, Q:float = None, vpu:float = 1.0, delta:float = 0.0):
        # Validate bus type against acceptable options.
        if bus_type not in Bus.bus_types:
            raise ValueError(f"Invalid bus type: {bus_type}. Must be one of {Bus.bus_types}")

        # Enforce bus-specific rules:
        if bus_type == "Slack Bus":
            if vpu != 1.0 or delta != 0.0:
                raise ValueError("Slack Bus must have vpu=1.0 and delta=0.0")
            if Bus.slack_assigned:
                raise ValueError("Only one Slack Bus is allowed in the system.")
            Bus.slack_assigned = True  # Mark that the slack bus is assigned.
        elif bus_type == "PQ Bus":
            if P is None or Q is None:
                raise ValueError("PQ Bus must have both real_power and reactive_power values.")
        elif bus_type == "PV Bus":
            if P is None:
                raise ValueError("PV Bus must have a real_power value (voltage is specified by vpu).")

        self.name = name
        self.base_kv = base_kv
        self.index = Bus.count
        Bus.count += 1

        self.vpu = vpu # Per unit voltage magnitude (default = 1.0 p.u.)
        self.delta = delta # Voltage phase angle in degrees (default = 0.0 degrees)
        self.bus_type = bus_type # Slack, PQ, or PV
        self.P = P # real power in Mvar
        self.Q = Q # reactive power in MW

        # Ensure that bus type validation is enforced (acceptable types only)

    def __repr__(self):
        """Returns a string representation of the Bus object."""
        return (f"Bus(name='{self.name}', base_kv={self.base_kv}, index={self.index}, "
                f"vpu={self.vpu}, delta={self.delta}, bus_type='{self.bus_type}', "
                f"P={self.P}, Q={self.Q})")

