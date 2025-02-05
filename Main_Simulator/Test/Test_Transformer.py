from Classes.bus import Bus
from Classes.transformer import Transformer

def test_transformer_class():
    """Function to test the Transformer class."""

    # Create Bus instances
    bus1 = Bus("Bus 1", 20)
    bus2 = Bus("Bus 2", 230)

    # Create Transformer instance
    transformer = Transformer("T1", bus1, bus2, power_rating=125, impedance_percent=8.5, x_over_r_ratio=10)

    # Print transformer details
    print(transformer)

    # Print Y-primitive matrix
    print("\nY-primitive matrix (Yprim):")
    for row in transformer.yprim:
        print(row)  # Print each row of the 2x2 Yprim matrix

    # Verify impedance calculation
    assert transformer.zt.real > 0, "Transformer real impedance (R) should be greater than 0"
    assert transformer.zt.imag > 0, "Transformer imaginary impedance (X) should be greater than 0"

    # Verify Y-primitive matrix
    assert transformer.yprim[0][0] == transformer.yt, "Yprim diagonal element is incorrect"
    assert transformer.yprim[0][1] == -transformer.yt, "Yprim off-diagonal element is incorrect"

    print("\nAll Transformer class tests passed!")


if __name__ == "__main__":
    test_transformer_class()


