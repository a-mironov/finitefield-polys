# polynomial module

# contains logic for finite field calculations
# and polynomial management (input, output, creation, replacement and deletion)

# field characteristic
global FCH = 7

class Poly():
    def __init__(self, cfs):
        self.coeffs = cfs
        self.normalize()

    # normalize coefficients to range 0..FCH-1
    def normalize(self):
        self.coeffs = map(lambda n: n % FCH, self.coeffs)
        
