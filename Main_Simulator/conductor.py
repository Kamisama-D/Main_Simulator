class Conductor:
    def __init__(self, name:str, diam:float, GMR:float, resistance:float, ampacity:float):
        self.name = name
        self.diam = diam
        self.GMR = GMR # Geometric Mean Radius
        self.resistance = resistance
        self.ampacity = ampacity

# Validation
if __name__ == "__main__":
    conductor1 = Conductor("Partridge", 0.642, 0.0217,
                           0.385, 460)
    print(conductor1.name, conductor1.diam,
         conductor1.GMR, conductor1.resistance, conductor1.ampacity)