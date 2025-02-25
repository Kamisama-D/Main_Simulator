# Import the Bus class from the bus module
from Classes.bus import Bus

def test_bus_class():
    """Function to test the Bus class."""

    # Create instances of Bus
    bus1 = Bus("Bus 1", 20, 'Slack Bus')
    bus2 = Bus("Bus 2", 230, 'PQ Bus', P=50, Q=30)
    bus3 = Bus("Bus 3", 500, 'PV Bus', P=100)

    # Print details of each bus to verify attributes
    print(bus1)  # Expected: Bus(name='Bus 1', base_kv=20, index=0)
    print(bus2)  # Expected: Bus(name='Bus 2', base_kv=230, index=1)
    print(bus3)  # Expected: Bus(name='Bus 3', base_kv=500, index=2)

    # Verify unique indices
    assert bus1.index == 0, "Bus 1 index should be 0"
    assert bus2.index == 1, "Bus 2 index should be 1"
    assert bus3.index == 2, "Bus 3 index should be 2"

    # Verify the total bus count
    print(f"Total buses created: {Bus.count}")  # Expected: 3
    assert Bus.count == 3, "Bus count should be 3"

    print("All Bus class tests passed!")

if __name__ == "__main__":
    test_bus_class()
