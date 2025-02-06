from Classes.conductor import Conductor
from Classes.bundle import Bundle

def test_bundle_class():
    """Function to test the Bundle class with different conductor configurations."""

    # Create a conductor instance
    conductor1 = Conductor("Partridge", diam=0.642, GMR=0.0217, resistance=0.385, ampacity=460)

    # Create bundle instances for 1, 2, 3, and 4 conductors
    bundle1 = Bundle("Single", num_conductors=1, spacing=1.0, conductor=conductor1)
    bundle2 = Bundle("Double", num_conductors=2, spacing=10.0, conductor=conductor1)
    bundle3 = Bundle("Triple", num_conductors=3, spacing=15.0, conductor=conductor1)
    bundle4 = Bundle("Quad", num_conductors=4, spacing=20.0, conductor=conductor1)

    # Print bundle details
    print("\nBundle Details:")
    print(bundle1)
    print(bundle2)
    print(bundle3)
    print(bundle4)

    # Assertions to check correctness
    assert bundle1.DSL == conductor1.GMR, "DSL calculation incorrect for single conductor"
    assert bundle2.DSL == (conductor1.GMR * bundle2.spacing) ** 0.5, "DSL incorrect for double bundle"
    assert bundle3.DSL == (conductor1.GMR * bundle3.spacing ** 2) ** (1/3), "DSL incorrect for triple bundle"
    assert bundle4.DSL == 1.091 * (conductor1.GMR * bundle4.spacing ** 3) ** (1/4), "DSL incorrect for quad bundle"

    assert bundle1.DSC == conductor1.radius, "DSC calculation incorrect for single conductor"
    assert bundle2.DSC == (conductor1.radius * bundle2.spacing) ** 0.5, "DSC incorrect for double bundle"
    assert bundle3.DSC == (conductor1.radius * bundle3.spacing ** 2) ** (1/3), "DSC incorrect for triple bundle"
    assert bundle4.DSC == 1.091 * (conductor1.radius * bundle4.spacing ** 3) ** (1/4), "DSC incorrect for quad bundle"

    print("\nAll Bundle class tests passed!")

if __name__ == "__main__":
    test_bundle_class()
