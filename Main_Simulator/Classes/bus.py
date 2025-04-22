class Bus:
    count = 0
    slack_assigned = False  # Ensures only one slack bus is assigned

    def __init__(self, name: str, base_kv: float):

        self.name = name
        self.base_kv = base_kv
        self.index = Bus.count
        self.real_power = 0.0
        self.reactive_power = 0.0
        self.bus_type = "PQ Bus"  # Slack, PV, PQ — set later by generator/load addition
        self.loads = []
        Bus.count += 1

    def __repr__(self):
        return f"Bus(name={self.name}, base_kv={self.base_kv}, type={self.bus_type})"