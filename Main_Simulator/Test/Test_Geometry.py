from Classes.geometry import Geometry

def test_geometry_class():
    """Function to test the Geometry class with a sample three-phase system."""

    # Create geometry instance (Example: Spacing in feet)
    geometry1 = Geometry("Standard_3Phase", xa=0, ya=0, xb=5, yb=8, xc=10, yc=0)

    # Print geometry details
    print("\nGeometry Details:")
    print(geometry1)
    print(f"Calculated Deq: {geometry1.Deq:.4f} ft")  # Explicitly print Deq

    # Manually compute expected Deq
    Dab = ((geometry1.xb - geometry1.xa) ** 2 + (geometry1.yb - geometry1.ya) ** 2) ** 0.5
    Dbc = ((geometry1.xc - geometry1.xb) ** 2 + (geometry1.yc - geometry1.yb) ** 2) ** 0.5
    Dca = ((geometry1.xa - geometry1.xc) ** 2 + (geometry1.ya - geometry1.yc) ** 2) ** 0.5
    expected_Deq = (Dab * Dbc * Dca) ** (1/3)

    # Verify Deq calculation
    assert abs(geometry1.Deq - expected_Deq) < 1e-6, "Deq calculation incorrect"

    print("\nAll Geometry class tests passed!")

if __name__ == "__main__":
    test_geometry_class()
