import math

class Geometry:
    def __init__(self, name:str, xa:float, ya:float, xb:float, yb:float, xc:float, yc:float):
        self.name = name
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb
        self.xc = xc
        self.yc = yc
        self.Deq = float # equivalent distance
        self.calc_Deq()

    def calc_Deq(self):
        # Calculate distances between each pair of points
        d_ab = math.sqrt((self.xa - self.xb) ** 2 + (self.ya - self.yb) ** 2)
        d_ac = math.sqrt((self.xa - self.xc) ** 2 + (self.ya - self.yc) ** 2)
        d_bc = math.sqrt((self.xb - self.xc) ** 2 + (self.yb - self.yc) ** 2)

        # Calculate the geometric mean of the distances
        self.Deq = (d_ab * d_ac * d_bc) ** (1 / 3)
        return self.Deq

# Validation
if __name__ == "__main__":
    geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0,
                         37, 0)
    print(geometry1.name, geometry1.xa, geometry1.ya,
          geometry1.xb, geometry1.yb, geometry1.xc, geometry1.yc)
    print(geometry1.Deq)