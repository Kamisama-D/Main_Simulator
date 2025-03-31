from Classes.bus import Bus


class Generator:
    def __init__(self, name: str, bus, real_power: float, per_unit: float):
        self.name = name
        self.bus = bus  # This should be a Bus object
        self.real_power = real_power  # Real power generation in MW
        self.per_unit = per_unit  # Voltage setpoint in p.u.
        self.Q = None  # Reactive power, to be calculated during power flow

        # Set PV or Slack Bus behavior
        if self.bus.bus_type not in ["Slack Bus", "PV Bus"]:
            self.bus.bus_type = "PV Bus"
            self.bus.per_unit = self.per_unit

            if not hasattr(self.bus, 'generators'):
                self.bus.generators = []
            self.bus.generators.append(self)


        else:
            print(f"[INFO] Generator '{self.name}' is connected to Slack Bus '{self.bus.name}'. P will be calculated during power flow.")



    def __repr__(self):
        return (f"Generator(name='{self.name}', bus='{self.bus.name}', "
                f"voltage_setpoint={self.per_unit} p.u., real_power={self.real_power} MW, "
                f"Q={self.Q})")
