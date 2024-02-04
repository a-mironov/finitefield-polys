# polynomial module

# contains logic for finite field calculations
# and polynomial management (input, output, creation, replacement and deletion)

from math import sqrt, floor

# field characteristic
FCH = 7
# polynomial dictionary
poly_dict = {}

# polynomials stored as lists of coefficients
# in ascending order, so p.coeffs[i] == x^i coefficient
class Poly():
    def __init__(self, cfs: list):
        self.coeffs = cfs
        self.normalize()

    def __str__(self):
        # will make something more sophisticated here...
        return str(self.coeffs)

    def normalize(self):
        # normalize coefficients to range 0..FCH-1
        self.coeffs = list(map(lambda n: n % FCH, self.coeffs))
        # trim zeroes
        zeroidx = len(self.coeffs)-1
        while zeroidx > 0 and self.coeffs[zeroidx] == 0:
            zeroidx -= 1
        del self.coeffs[zeroidx+1:]

def is_prime(n: int):
    """
    Checks if its input is prime. Auxiliary.

    n: int -- The number whose primality is to be checked.
    """
    if n == 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = floor(sqrt(n)) + 1
    # check for divisibility by odd numbers between 3 and sqrt(n)
    for d in range(3, limit, 2):
        if n % d == 0:
            return False
    return True

def make_poly(name: str, coefficients: list):
    """
    makes a new polynomial and adds it to the dict

    name: str - the name of the polynomial
    coefficients: list - the coefficients of the polynomial
    """
    # possible exceptions: 2
    # 1. bad name: supplied name is already found in the dict
    
    if name in poly_dict.keys():
        raise ValueError(f"Name {name} already in use! Use `update` to overwrite polynomials.")
    
    #2. bad coeffs: at least one entry in cfs can't parse as an int
    cfs_clean = [0] * len(coefficients)
    for i in range(len(coefficients)):
        try:
            cfs_clean[i] = int(coefficients[i])
        except ValueError:
            raise ValueError(f"""Coefficient on x^{i}
                            read as "{coefficients[i]}", cannot parse!""")

    #if we made it here, the name is good and the coefficients list is clean
    poly_dict[name] = Poly(cfs_clean)

def del_poly(name: str):
    """
    deletes a polynomial from the dict

    name: str - the name of the polynomial 
    """
    # possible exceptions: 1
    # 1. bad name: polynomial by that name doesn't exist in poly_dict anyway
    if name not in poly_dict.keys():
        raise KeyError(f"No polynomial with name {name} to delete.")

    # if we made it here, the name is good and deletable
    poly_dict.pop(name)

def display_poly(name: str):
    """
    outputs a string representation of the given polynomial

    name: str - the name of the polynomial
    """
    try:
        poly = poly_dict[name]
    except KeyError:
        raise KeyError(f"No polynomial by name {name} to print.")
    return name + " = " + str(poly)

def display_all():
    """
    outputs a string representation for the entire polynomial dict
    """
    display_string = ""
    for name in poly_dict.keys():
        display_string += display_poly(name) + "\n"

    return display_string

def update_poly(name: str, coefficients: list):
    """
    updates a polynomial with new coefficients
    the value of the old polynomial is discarded

    name: str - the name of the polynomial
    coefficients: list - the new coefficients of the polynomial
    """
    if name not in poly_dict.keys():
        raise KeyError(f"""No polynomial with name {name} to update!
Use `create` to create new polynomials.""")

    del_poly(name)
    make_poly(name, coefficients)

def set_characteristic(new_char: int):
    """
    Resets the characteristic of the base field.
    Unless the old value matches the new, flushes all stored polynomials.

    new_char: int -- the new value of the characteristic
    """
    global FCH
    # if new characteristic is the same as the old, do nothing
    if new_char == FCH:
        return
    elif new_char <= 1:
        raise ValueError(f"Invalid characteristic value {new_char} -- Not a natural number.")
    elif not is_prime(new_char):
        raise ValueError(f"Invalid characteristic value {new_char} -- Not prime.")
    else:
        # new characteristic is prime and differs from old
        FCH = new_char
        # flushing the polynomials
        for name in poly_dict.keys():
            del_poly(name)
