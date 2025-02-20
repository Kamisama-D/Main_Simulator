from Classes.conductor import Conductor

def test_conductor_class():
    """Function to test the Conductor class, including radius calculation."""

    # Create conductor instance
    conductor1 = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)

    # Print conductor details (Now correctly showing all values)
    print("\nConductor Details:")
    print(conductor1)
    print(f"Calculated Radius: {conductor1.radius:.4f} ft")  # Explicitly printing the radius

    # Verify attributes
    assert conductor1.name == "Partridge", "Conductor name incorrect"
    assert conductor1.diam == 0.642, "Conductor diameter incorrect"
    assert conductor1.GMR == 0.0217, "GMR incorrect"
    assert conductor1.resistance == 0.385, "Resistance incorrect"
    assert conductor1.ampacity == 460, "Ampacity incorrect"
    assert abs(conductor1.radius - (0.642 / 24)) < 1e-6, "Radius calculation incorrect"

    print("\nAll Conductor class tests passed!")

if __name__ == "__main__":
    test_conductor_class()


