class Bus:
    # Class-level attributes
    count = 0
    slack_assigned = False
    bus_types = ["Slack Bus", "PQ Bus", "PV Bus"]

    def __init__(self, name: str, base_kv: float, bus_type: str, P: float = None,
                 Q: float = None, vpu: float = 1.0, delta: float = 0.0):
        # Validate bus type against acceptable options.
        if bus_type not in Bus.bus_types:
            raise ValueError(f"Invalid bus type: {bus_type}. Must be one of {Bus.bus_types}")

        # Initialize common attributes
        self.name = name
        self.base_kv = base_kv
        self.index = Bus.count
        Bus.count += 1

        self.vpu = vpu  # Per unit voltage magnitude (default = 1.0 p.u.)
        self.delta = delta  # Voltage phase angle in degrees (default = 0.0 degrees)
        self.bus_type = bus_type  # Slack, PQ, or PV

        # Initialize Q and reactive power limits
        self.Q = None
        self.Q_min = None  # Initialize as None for all bus types
        self.Q_max = None  # Initialize as None for all bus types

        # Enforce bus-specific rules:
        if bus_type == "Slack Bus":
            if vpu != 1.0 or delta != 0.0:
                raise ValueError("Slack Bus must have vpu=1.0 and delta=0.0")
            if Bus.slack_assigned:
                raise ValueError("Only one Slack Bus is allowed in the system.")
            Bus.slack_assigned = True  # Mark that the slack bus is assigned.
            self.P = None  # Calculated during power flow
            self.Q = None  # Calculated during power flow

        elif bus_type == "PQ Bus":
            if P is None or Q is None:
                raise ValueError("PQ Bus must have real_power (P) and reactive_power (Q) values.")
            self.P = P  # Defined as input for PQ Bus
            self.Q = Q  # Defined as input for PQ Bus

        elif bus_type == "PV Bus":
            if P is None:
                raise ValueError("PV Bus must have a real_power (P) value.")
            self.P = P
            self.Q = None  # Q will be calculated during power flow
            # Reactive Power Limits for PV Bus using Percentage of Real Power (±40% of P)
            self.Q_max = 0.4 * self.P
            self.Q_min = -0.4 * self.P

    def check_reactive_limits(self):
        """
        Check and enforce reactive power limits for PV Bus.
        If Q exceeds limits, set Q to the limit and switch to PQ Bus.
        """
        if self.bus_type == "PV Bus":
            if self.Q is not None:
                if self.Q > self.Q_max:
                    print(f"[Notification] Bus '{self.name}' switched from PV to PQ: Q exceeded Q_max ({self.Q_max})")
                    self.Q = self.Q_max
                    self.bus_type = "PQ Bus"
                elif self.Q < self.Q_min:
                    print(f"[Notification] Bus '{self.name}' switched from PV to PQ: Q below Q_min ({self.Q_min})")
                    self.Q = self.Q_min
                    self.bus_type = "PQ Bus"

    def __repr__(self):
        """Returns a string representation of the Bus object."""
        # Display logic for P and Q
        P_value = self.P if self.P is not None else "Not Calculated"
        if self.bus_type == "PQ Bus":
            Q_value = self.Q  # Show Q as input for PQ Bus
        else:
            Q_value = self.Q if self.Q is not None else "Not Calculated"

        # Display logic for Q_min and Q_max
        Q_min_value = self.Q_min if self.Q_min is not None else "Not Applicable"
        Q_max_value = self.Q_max if self.Q_max is not None else "Not Applicable"

        return (f"Bus(name='{self.name}', base_kv={self.base_kv}, index={self.index}, "
                f"vpu={self.vpu}, delta={self.delta}, bus_type='{self.bus_type}', "
                f"P={P_value}, Q={Q_value}, Q_min={Q_min_value}, Q_max={Q_max_value})")


