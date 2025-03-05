from Classes.bus import Bus


class Generator:
    def __init__(self, name: str, bus: Bus, voltage_setpoint: float, mw_setpoint: float):
        """
        Initialize the Generator object.
        - name: Name of the generator
        - bus: Associated Bus object
        - voltage_setpoint: Target voltage magnitude in per unit
        - mw_setpoint: Real power generation in MW
        """
        self.name = name
        self.bus = bus
        self.voltage_setpoint = voltage_setpoint  # Target voltage magnitude in per unit
        self.mw_setpoint = mw_setpoint  # Real power generation in MW
        self.Q = None  # Reactive power is calculated during power flow

        # Automatically set the bus to PV type unless it is the Slack Bus
        if self.bus.bus_type != "Slack Bus":
            self.bus.bus_type = "PV Bus"
            self.bus.vpu = self.voltage_setpoint  # Set the voltage setpoint

            # Register this generator with the bus
            if not hasattr(self.bus, 'generators'):
                self.bus.generators = []
            self.bus.generators.append(self)

            # Update the bus's total real power (P) by summing all connected generators
            self.update_bus_power()
        else:
            # For Slack Bus, P should not be set by the Generator Class
            print(
                f"[INFO] Generator '{self.name}' is connected to Slack Bus '{self.bus.name}'. P will be calculated during power flow.")

    def update_bus_power(self):
        """ Accumulate the total real power (P) from all generators connected to the bus. """
        total_P = sum(gen.mw_setpoint for gen in self.bus.generators)
        self.bus.P = total_P

    def calculate_Q(self, ybus, voltages):
        """
        Calculate reactive power (Q) for the generator's bus using power injection equations.
        This should be called during power flow solution.
        """
        if self.bus.bus_type == "PV Bus":
            # Placeholder for power injection equation to calculate Q
            # Q_k = V_k * sum(V_m * Y_km * sin(delta_k - delta_m - theta_km))
            self.Q = self.bus.vpu * sum(...)  # Complete this with power injection logic
            self.bus.Q = self.Q  # Update the bus's Q value

    def __repr__(self):
        return (f"Generator(name='{self.name}', bus='{self.bus.name}', "
                f"voltage_setpoint={self.voltage_setpoint} p.u., mw_setpoint={self.mw_setpoint} MW, "
                f"Q={self.Q})")
