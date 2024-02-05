# polynomial module

# contains logic for polynomial management
# (creation, replacement, deletion, display)

from math import sqrt, floor
from enum import Flag, auto

# field characteristic
FCH = 7
# polynomial dictionary
poly_dict = {}
# inverse lookup

# WIP!!
class DisplayFlag(Flag):
    # true => print terms in descending order, false => ascending order
    DESCENDING = auto()
    # not yet implemented: balanced -- coeffs in -(FCH-1)/2 .. (FCH-1)/2
    # instead of 0 .. FCH-1
    # BALANCED = auto()

# polynomials stored as lists of coefficients
# in ascending order, so p.coeffs[i] == x^i coefficient
class Poly():
    def __init__(self, cfs: list):
        self.coeffs = cfs
        # empty list => zero polynomial
        if len(self.coeffs) == 0:
            self.coeffs = [0]
        self.normalize()

    def __str__(self):
        # constant => print as-is
        if len(self.coeffs) == 1:
            return str(self.coeffs[0])
        # otherwise iterate thru terms
        # adding only those with nonzero coeffs to the string rep
        terms = []
        for i in range(len(self.coeffs)):
            coefficient = self.coeffs[i]
            if coefficient != 0:
                # constant term printed as is
                if i == 0:
                    terms.append(str(self.coeffs[0]))
                else:
                    # power x^i, printed as just x for i=1
                    power = f"x^{i}"
                    if i == 1:
                        power = "x"
                    if coefficient == 1:
                        terms.append(power)
                    else:
                        terms.append(str(coefficient) + power)
                    
        return " + ".join(terms)

    def normalize(self):
        """
        normalizes all coefficients to range 0..FCH-1
        and trims leading zeroes
        """
        self.coeffs = list(map(lambda n: n % FCH, self.coeffs))
        # trim zeroes
        zeroidx = len(self.coeffs)-1
        while zeroidx > 0 and self.coeffs[zeroidx] == 0:
            zeroidx -= 1
        del self.coeffs[zeroidx+1:]

    def __add__(self, other):
        """
        adds two polynomials
        """
        total = Poly([0])
        total.coeffs = [0] * max(len(self.coeffs),len(other.coeffs))
        n = len(total.coeffs)
        for i in range(n):
            if i < len(self.coeffs):
                total.coeffs[i] += self.coeffs[i]
            if i < len(other.coeffs):
                total.coeffs[i] += other.coeffs[i]
        total.normalize()
        return total

    def __sub__(self, other):
        """
        subtracts two polynomials (self - other)
        """
        total = Poly([0])
        total.coeffs = [0] * max(len(self.coeffs),len(other.coeffs))
        n = len(total.coeffs)
        for i in range(n):
            if i < len(self.coeffs):
                total.coeffs[i] += self.coeffs[i]
            if i < len(other.coeffs):
                total.coeffs[i] -= other.coeffs[i]
        total.normalize()
        return total

    def __mul__(self, other):
        """
        multiplies two polynomials
        """
        total = Poly([0])
        # polynomial degrees; assumes normalized
        m = len(self.coeffs) - 1
        n = len(other.coeffs) - 1
        total.coeffs = [0]*(m+n+1)
        # naive convolution
        for k in range(m+n+1):
            for i in range(k+1):
                j = k - i
                if i <= m and j <= n:
                    total.coeffs[k] += (self.coeffs[i]*other.coeffs[j]) % FCH
        total.normalize()
        return total

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
            raise ValueError(f"Coefficient on x^{i} "+
                             f"read as \"{coefficients[i]}\", "+
                             "cannot parse!")

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
        raise KeyError(name)

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
        raise KeyError(name)
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
        raise KeyError(name)

    del_poly(name)
    make_poly(name, coefficients)


def addmake_poly(name1: str, name2: str, result: str):
    """
    pulls two polynomials from poly_dict, adds them, and stores the result
    name1 and name2 must exist, while result must NOT exist

    name1: str -- name of the first polynomial to be summed
    name2: str -- name of the second polynomial to be summed
    result: str -- name under which to store the result
    """
    # read polynomials from dict
    try:
        addend1 = poly_dict[name1]
        addend2 = poly_dict[name2]
    except KeyError as e:
        raise e
    # ensure name `result` does not exist
    if result in poly_dict.keys():
        raise ValueError(f"Cannot store addition result -- name {result}"+
                         "already in use.")
    # now we have our polys and can add them
    total = addend1 + addend2
    # not calling make_poly b/c the polynomial object is already there
    poly_dict[result] = total

def submake_poly(name1: str, name2: str, result: str):
    """
    pulls two polynomials from poly_dict, subtracts them, and stores the result
    name1 and name2 must exist, while result must NOT exist

    name1: str -- name of the first polynomial to be summed
    name2: str -- name of the second polynomial to be summed
    result: str -- name under which to store the result
    """
    # read polynomials from dict
    try:
        addend1 = poly_dict[name1]
        addend2 = poly_dict[name2]
    except KeyError as e:
        raise e
    # ensure name `result` does not exist
    if result in poly_dict.keys():
        raise ValueError(f"Cannot store subtraction result -- name {result}"+
                         "already in use.")
    # now we have our polys and can subtract them
    total = addend1 - addend2
    # not calling make_poly b/c the polynomial object is already there
    poly_dict[result] = total

def mulmake_poly(name1: str, name2: str, result: str):
    """
    pulls two polynomials from poly_dict, multiplies them, and stores the result
    name1 and name2 must exist, while result must NOT exist

    name1: str -- name of the first polynomial to be summed
    name2: str -- name of the second polynomial to be summed
    result: str -- name under which to store the result
    """
    # read polynomials from dict
    try:
        addend1 = poly_dict[name1]
        addend2 = poly_dict[name2]
    except KeyError as e:
        raise e
    # ensure name `result` does not exist
    if result in poly_dict.keys():
        raise ValueError(f"Cannot store addition result -- name {result}"+
                         "already in use.")
    # now we have our polys and can add them
    total = addend1 * addend2
    # not calling make_poly b/c the polynomial object is already there
    poly_dict[result] = total

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
        raise ValueError(f"Invalid characteristic value {new_char} -- "+
                         "Not a natural number.")
    elif not is_prime(new_char):
        raise ValueError(f"Invalid characteristic value {new_char} -- "+
                         "Not prime.")
    else:
        # new characteristic is prime and differs from old
        FCH = new_char
        # flushing the polynomials
        poly_dict.clear()
