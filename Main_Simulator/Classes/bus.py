class Bus:
    count = 0

    def __init__(self, name:str, base_kv:float):
        self.name = name
        self.base_kv = base_kv
        self.index = Bus.count
        Bus.count += 1

    def __repr__(self):
        """Returns a string representation of the Bus object."""
        return f"Bus(name='{self.name}', base_kv={self.base_kv}, index={self.index})"

