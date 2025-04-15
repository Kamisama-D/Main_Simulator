from Classes.bus import Bus

class Generator:
    def __init__(self, name: str, bus: Bus, real_power: float, per_unit: float,
                 x1=None, x2=None, x0=None,
                 system_settings=None):
        self.name = name
        self.bus = bus  # This should be a Bus object
        self.real_power = real_power  # Real power generation in MW
        self.per_unit = per_unit  # Voltage setpoint in p.u.
        self.Q = None  # Reactive power, to be calculated during power flow

        # Initialize reactances (will be overwritten if conditions met)
        self.x1 = None
        self.x2 = None
        self.x0 = None

        # Set PV or Slack Bus behavior
        if self.bus.bus_type not in ["Slack Bus", "PV Bus"]:
            self.bus.bus_type = "PV Bus"
            self.bus.per_unit = self.per_unit

            if not hasattr(self.bus, 'generators'):
                self.bus.generators = []
            self.bus.generators.append(self)
        else:
            print(f"[INFO] Generator '{self.name}' is connected to Slack Bus '{self.bus.name}'. P will be calculated during power flow.")

        # Conversion of x1, x2, x0 from generator base to system base
        if system_settings and x1 is not None and x2 is not None and x0 is not None:
            v_gen = self.bus.base_kv
            v_sys = system_settings.base_voltage
            s_sys = system_settings.base_power

            # Avoid division by zero by setting s_gen = s_sys for Slack Bus
            if self.bus.bus_type == "Slack Bus" or real_power == 0:
                s_gen = s_sys
            else:
                s_gen = real_power

            base_ratio = (s_sys / s_gen) * (v_gen ** 2 / v_sys ** 2)

            self.x1 = x1 * base_ratio
            self.x2 = x2 * base_ratio
            self.x0 = x0 * base_ratio

    def calc_admittances(self):
        """
        Calculates and stores the positive-, negative-, and zero-sequence admittances (Y1, Y2, Y0)
        from system-base reactances x1, x2, and x0.

        Stores:
            self.Y1, self.Y2, self.Y0: Complex admittances (or None if x is not defined)
        """
        self.Y1 = -1j / self.x1 if self.x1 else None
        self.Y2 = -1j / self.x2 if self.x2 else None
        self.Y0 = -1j / self.x0 if self.x0 else None

        return {
            'Y1': self.Y1,
            'Y2': self.Y2,
            'Y0': self.Y0
        }

    def __repr__(self):
        return (f"Generator(name='{self.name}', bus='{self.bus.name}', "
                f"voltage_setpoint={self.per_unit} p.u., real_power={self.real_power} MW, "
                f"x1={self.x1}, x2={self.x2}, x0={self.x0})")