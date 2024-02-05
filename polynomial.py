# polynomial module

# contains logic for polynomial management
# (creation, replacement, deletion, display, copy, rename)
# as well as the polynomial class
# incl. operator definitions

from math import sqrt, floor
from enum import Flag, auto

# field characteristic
FCH = 7
# polynomial dictionary
poly_dict = {}

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
    def __init__(self, cfs: list=[0]):
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

    def degree(self):
        # zero polynomial is defined with degree -1
        if len(self.coeffs) == 0 and self.coeffs[0] == 0:
            return -1
        return len(self.coeffs) - 1

    def scale(self, scalar: int):
        """
        multiplies all coeffs in a polynomial by a scalar
        """
        result = Poly([0])
        result.coeffs = list(map(lambda n: scalar * n, self.coeffs))
        result.normalize()
        return result

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
        m = self.degree()
        n = other.degree()
        total.coeffs = [0]*(m+n+1)
        # naive convolution
        for i in range(m+1):
            for j in range(n+1):
                total.coeffs[i+j] += (self.coeffs[i]*other.coeffs[j]) % FCH

        total.normalize()
        return total

    def __pow__(self, exponent: int):
        """
        raises the polynomial to a power. must be integer and >= 0.
        implemented by repeated squaring.
        """
        if exponent < 0:
            raise ValueError(f"Cannot raise a polynomial to power {exponent}.")
        elif exponent == 0:
            return Poly([1]) # p^0 = 1
        elif exponent == 1:
            return self
        else:
            temp = self ** (exponent // 2)
            if exponent % 2 == 0:
                return temp * temp
            else:
                return temp * temp * self

    def peval(self, x: int):
        """
        Evaluates the polynomial at a point, using the Horner method.
        """
        # special case: polynomial is constant or needs to be eval'd at 0
        if self.degree() <= 0 or x == 0:
            return self.coeffs[0]
        
        result = 0
        power = 1 # holds x^n mod FCH
        for i in range(self.degree()+1):
            result = (result + power * self.coeffs[i]) % FCH
            power = (power * x) % FCH

        return result

    def __mod__(self, other):
        """
        Computes self % other as follows:
        1. Create list of polynomials equivalent to x^i mod other,
           for i from 0 up to self.degree().
        2. Take the linear combination of those, with the
           coefficients of self as weights.
        """
        if other.degree() == -1:
            raise ZeroDivisionError
        if other.degree() == 0:
            raise ArithmeticError("Cannot reduce modulo a constant polynomial!")
        if other.degree() == 1:
            point = -other.coeffs[0] * pow(other.coeffs[1], -1, FCH)
            return Poly([self.peval(point)])
        # make `other` monic by dividing out by its leading coefficient
        other_monic = other.scale(pow(other.coeffs[-1], -1, FCH))
        powers_mod_other = [Poly([0])] * len(self.coeffs)
        powers_mod_other[0] = Poly([1])
        for i in range(1,len(self.coeffs)):
            # multiply by x
            poly = powers_mod_other[i-1] * Poly([0,1])
            # reduce mod other
            # under normal circumstances, this >= should only ever be ==...
            if poly.degree() >= other.degree():
                coeff = poly.coeffs[-1]
                poly = poly - other.scale(coeff)
            powers_mod_other[i] = poly
        return lincomb(self.coeffs, powers_mod_other)
                

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

def copy_poly(source: str, dest: str):
    """
    copies a polynomial

    source: str -- name of the source polynomial
    dest: str -- name of the destination
    """
    try:
        poly = poly_dict[source]
    except KeyError as e:
        raise KeyError(source)

    if dest in poly_dict.keys():
        update_poly(dest, poly.coeffs)
    else:
        make_poly(dest, poly.coeffs)

def rename_poly(oldname: str, newname: str):
    """
    renames a polynomial
    """
    try:
        poly = poly_dict[oldname]
    except KeyError:
        raise KeyError(oldname)

    if newname in poly_dict.keys():
        raise ValueError(f"Polynomial by name {newname} already exists.")

    poly_dict[newname] = poly
    poly_dict.pop(oldname)
    

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

def lincomb(weights: list, polys: list):
    """
    linear combination: computes the sum
    weights[0] * polys[0] + weights[1] * polys[1] + ...

    weights - list: list of weights
    polys - list: list of polynomials
    """
    if len(weights) != len(polys):
        raise ValueError("Bad linear combination -- weight and polynomial count don't match.")
    # if we are here, len(weights) == len(polys)
    # initialize sum to 0
    total = Poly([0])
    for i in range(len(weights)):
        total = total + polys[i].scale(weights[i])
    return total
