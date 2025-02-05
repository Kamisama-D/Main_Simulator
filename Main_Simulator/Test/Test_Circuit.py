# Import necessary classes
from Classes.Circuit import Circuit
from Classes.bus import Bus
from Classes.transformer import Transformer
from Classes.transmission_line import TransmissionLine
from Classes.bundle import Bundle
from Classes.geometry import Geometry
from Classes.conductor import Conductor

def test_circuit_class():
    """Function to test the Circuit class."""

    # Step 1: Create a Circuit instance
    circuit = Circuit("Seven Bus Test System")
    print("\n✅ Circuit Created:", circuit.name)

    # Step 2: Create and Add Buses
    bus1 = Bus("Bus1", 230)
    bus2 = Bus("Bus2", 115)
    bus3 = Bus("Bus3", 500)

    circuit.add_bus(bus1)
    circuit.add_bus(bus2)
    circuit.add_bus(bus3)

    print("\n✅ Buses Added Successfully:")
    for bus in circuit.buses.values():
        print(f"- {bus.name}, {bus.base_kv} kV")

    # Step 3: Test Duplicate Bus Error Handling
    try:
        circuit.add_bus(bus1)  # Should raise ValueError
    except ValueError as e:
        print(f"\n✅ Duplicate Bus Error Caught: {e}")

    # Step 4: Create and Add a Transformer
    transformer = Transformer("T1", bus1, bus2, power_rating=100, impedance_percent=10, x_over_r_ratio=10)
    circuit.add_transformer(transformer)

    print("\n✅ Transformer Added Successfully:")
    print(f"- {transformer.name}, {transformer.power_rating} MVA")

    # Step 5: Test Duplicate Transformer Error Handling
    try:
        circuit.add_transformer(transformer)  # Should raise ValueError
    except ValueError as e:
        print(f"\n✅ Duplicate Transformer Error Caught: {e}")

    # Step 6: Create and Add a Transmission Line
    conductor = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)
    bundle = Bundle("Double", num_conductors=2, spacing=10.0, conductor=conductor)
    geometry = Geometry("Standard_3Phase", xa=0, ya=0, xb=5, yb=8, xc=10, yc=0)

    transmission_line = TransmissionLine("Line1", bus2, bus3, bundle, geometry, length=10)
    circuit.add_transmission_line(transmission_line)

    print("\n✅ Transmission Line Added Successfully:")
    print(f"- {transmission_line.name}, Length: {transmission_line.length} mi")

    # Step 7: Test Duplicate Transmission Line Error Handling
    try:
        circuit.add_transmission_line(transmission_line)  # Should raise ValueError
    except ValueError as e:
        print(f"\n✅ Duplicate Transmission Line Error Caught: {e}")

    # Step 8: Show Full Network Configuration
    print("\n--- Circuit Network Configuration ---")
    circuit.show_network()

    # Assertions to validate correctness
    assert circuit.name == "Seven Bus Test System", "Circuit name mismatch"
    assert len(circuit.buses) == 3, "Incorrect number of buses"
    assert len(circuit.transformers) == 1, "Incorrect number of transformers"
    assert len(circuit.transmission_lines) == 1, "Incorrect number of transmission lines"

    print("\n✅ All Circuit Class Tests Passed!")

if __name__ == "__main__":
    test_circuit_class()
