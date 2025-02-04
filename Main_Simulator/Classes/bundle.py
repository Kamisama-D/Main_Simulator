class Bundle:
    def __init__(self, name:str, num_conductors:int, spacing:float, conductor:str):
        self.name = name
        self.num_conductors = num_conductors
        self.spacing = spacing
        self.conductor = conductor
        self.DSC = float
        self.DSL = float
    #     calc_DSC()
    #     calc_DSL()
    #
    # def calc_DSC(self):
    #     # not sure what is DSC
    #
    # def calc_DSL(self):
    #     # not sure what is DSL

# Validation
if __name__ == '__main__':
    bundle1 = Bundle("Bundle 1", 2, 1.5, "Partridge")
    print(bundle1.name, bundle1.num_conductors,
          bundle1.spacing, bundle1.conductor)
    # print(bundle1.DSC, bundle1.DSL)
