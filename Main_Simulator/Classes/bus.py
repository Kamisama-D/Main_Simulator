class Bus:
    count = 0
    slack_assigned = False  # Ensures only one slack bus is assigned

    def __init__(self, name: str, base_kv: float, P: float = None, Q: float = None, vpu: float = None, delta: float = None):
        """
        Initializes a Bus object and classifies its type automatically.
        """
        self.name = name
        self.base_kv = base_kv
        self.index = Bus.count
        Bus.count += 1

        self.P = P
        self.Q = Q
        self.vpu = vpu
        self.delta = delta

        self.Q_min = None
        self.Q_max = None

        # Automatically classify bus type
        self.classify_bus_type()

    def classify_bus_type(self):
        """
        Determines the bus type based on provided attributes:
        - Slack Bus: Defined by user with vpu=1.0, delta=0.0.
        - PV Bus: Has P and vpu defined.
        - PQ Bus: Has P and Q defined.
        """
        if self.vpu == 1.0 and self.delta == 0.0 and not Bus.slack_assigned:
            self.bus_type = "Slack Bus"
            Bus.slack_assigned = True
            print(f"[INFO] Bus '{self.name}' classified as Slack Bus.")

        elif self.P is not None and self.vpu is not None:
            self.bus_type = "PV Bus"
            self.Q = None  # Q will be calculated
            self.Q_min = -0.4 * self.P  # Assuming ±40% limit
            self.Q_max = 0.4 * self.P
            self.delta = 0.0  # Initial guess for voltage angle
            print(f"[INFO] Bus '{self.name}' classified as PV Bus.")

        elif self.P is not None and self.Q is not None:
            self.bus_type = "PQ Bus"
            self.vpu = 1.0  # Initial guess for voltage magnitude
            self.delta = 0.0  # Initial guess for voltage angle
            print(f"[INFO] Bus '{self.name}' classified as PQ Bus.")

        else:
            raise ValueError(f"Bus '{self.name}' has insufficient inputs to classify its type.")

    def check_reactive_limits(self):
        """
        Enforces Q limits for PV Bus and switches to PQ if exceeded.
        """
        if self.bus_type == "PV Bus" and self.Q is not None:
            if self.Q > self.Q_max:
                print(f"[WARNING] Bus '{self.name}' exceeded Q_max ({self.Q_max}). Switching to PQ Bus.")
                self.Q = self.Q_max
                self.bus_type = "PQ Bus"

            elif self.Q < self.Q_min:
                print(f"[WARNING] Bus '{self.name}' went below Q_min ({self.Q_min}). Switching to PQ Bus.")
                self.Q = self.Q_min
                self.bus_type = "PQ Bus"

    def __repr__(self):
        """Returns a formatted string representation of the Bus object."""
        P_value = self.P if self.P is not None else "Not Calculated"
        Q_value = self.Q if self.Q is not None else "Not Calculated"
        Q_min_value = self.Q_min if self.Q_min is not None else "Not Applicable"
        Q_max_value = self.Q_max if self.Q_max is not None else "Not Applicable"

        return (f"Bus(name='{self.name}', base_kv={self.base_kv}, index={self.index}, "
                f"vpu={self.vpu}, delta={self.delta}, bus_type='{self.bus_type}', "
                f"P={P_value}, Q={Q_value}, Q_min={Q_min_value}, Q_max={Q_max_value})")



