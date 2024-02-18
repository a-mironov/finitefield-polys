# polynomial module

# contains the polynomial class
# as well as a few functions to do with polynomials

from enum import Flag, auto

import auxiliaries as aux

# field characteristic
FCH = 7
# polynomial dictionary
poly_dict = {}

# WIP!!
class DisplayFlag(Flag):
    # true => print terms in descending order, false => ascending order
    DESCENDING = auto()
    # true => balanced -- coeffs in -(FCH-1)/2 .. (FCH-1)/2
    # false => unbalanced -- coeffs in 0 .. FCH-1
    # ignored in char 2
    BALANCED = auto()
    def __str__(self):
        result = ""
        # degree
        if DisplayFlag.DESCENDING in self:
            result += "Descending-degree order"
        else:
            result += "Ascending-degree order"
        result += "\n"
        if FCH != 2:
            if DisplayFlag.BALANCED in self:
                result += ("Balanced coefficients "+
                          f"(-{(FCH-1)//2} to {(FCH-1)//2})")
            else:
                result += f"Unbalanced coefficients (0 to {FCH-1})"
        elif DisplayFlag.BALANCED in self:
            result += "Balanced coefficients (0 to 1 -- option ignored)"
        else:
            result += "Unbalanced coefficients (0 to 1 -- option ignored)"
        return result

display_cfg = DisplayFlag.DESCENDING | DisplayFlag.BALANCED
opttags = {"deg": DisplayFlag.DESCENDING, "bal": DisplayFlag.BALANCED}

# for echoing option states to the user
# singleopts_names[option][0] == option name
# singleopts_names[option][1] == meaning if false
# singleopts_names[option][2] == meaning if true
singleopts_names = {"deg": ("Term order", "Ascending", "Descending"),
                    "bal": ("Coefficient display", "Unbalanced", "Balanced")}

# polynomials stored as lists of coefficients
# in ascending order, so p.coeffs[i] == x^i coefficient
class Poly():
    def __init__(self, cfs: list=[0]):
        self.coeffs = cfs
        # empty list => zero polynomial
        if len(self.coeffs) == 0:
            self.coeffs = [0]
        self.normalize()

    def str_custom(self, varname: str = "x"):
        # constant => print as-is
        if len(self.coeffs) == 1:
            coefficient = self.coeffs[0]
            if (FCH != 2 and
                DisplayFlag.BALANCED in display_cfg and 
                coefficient > (FCH-1)//2):
                coefficient -= FCH
            return str(coefficient)
        # otherwise iterate thru terms
        # adding only those with nonzero coeffs to the string rep
        terms = []
        for i in range(len(self.coeffs)):
            coefficient = self.coeffs[i]
            # characteristic 2 ignores balanced coeff option.
            # only nonzero coeff is 1 anyway!
            if (FCH != 2 and
                DisplayFlag.BALANCED in display_cfg and 
                coefficient > (FCH-1)//2):
                coefficient -= FCH
            if coefficient != 0:
                # constant term printed as is
                if i == 0:
                    terms.append(str(coefficient))
                else:
                    # power x^i, printed as just x for i=1
                    power = f"{varname}^{i}"
                    if i == 1:
                        power = varname
                    if coefficient == 1:
                        terms.append(power)
                    elif coefficient == -1:
                        terms.append("-" + power)
                    else:
                        terms.append(str(coefficient) + power)
        if DisplayFlag.DESCENDING in display_cfg:
            terms.reverse()
        result = " + ".join(terms).replace("+ -","- ")
        return result

    def __str__(self):
        return self.str_custom(varname = "x")

    def normalize(self):
        """
        Normalizes all coefficients to range 0..FCH-1,
        and trims leading zeroes.
        In case of the zero polynomial, keeps the sole zero coefficient.
        """
        self.coeffs = list(map(lambda n: n % FCH, self.coeffs))
        # trim zeroes
        zeroidx = len(self.coeffs)-1
        while zeroidx > 0 and self.coeffs[zeroidx] == 0:
            zeroidx -= 1
        del self.coeffs[zeroidx+1:]

    def __copy__(self):
        newcoeffs = self.coeffs.copy()
        return Poly(newcoeffs)

    def degree(self):
        # zero polynomial is defined with degree -1
        if len(self.coeffs) == 1 and self.coeffs[0] == 0:
            return -1
        return len(self.coeffs) - 1

    def is_zero(self):
        """
        Determines whether the polynomial is zero. Hacky.
        """
        self.normalize()
        if len(self.coeffs) == 1 and self.coeffs[0] == 0:
            return True
        return False

    def scale(self, scalar: int):
        """
        Multiplies all coeffs in a polynomial by a scalar.
        """
        result = Poly([0])
        result.coeffs = list(map(lambda n: scalar * n, self.coeffs))
        result.normalize()
        return result

    def monify(self):
        """
        Returns self divided by the leading coefficient of self.
        The result is monic, hence the name.
        On input of the zero polynomial, does nothing.
        """
        if self.is_zero():
            return self
        return self.scale(pow(self.coeffs[-1], -1, FCH))

    def __eq__(self, other):
        """
        Determines if two polynomials are equal.
        Normalizes both before proceeding, for good measure.
        """
        self.normalize()
        other.normalize()
        # degrees unequal => polys unequal
        if self.degree() != other.degree():
            return False
        # degrees equal => check equality of coeffs
        for i in range(self.degree() + 1):
            if self.coeffs[i] != other.coeffs[i]:
                return False
        # if we made it through the loop,
        # the degrees are equal and all coeffs match
        return True

    def __add__(self, other):
        """
        Adds two polynomials.
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
        Subtracts two polynomials (self - other).
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
        Multiplies two polynomials.
        """
        total = Poly([0])
        # special case for 0 polynomial
        if self.degree() == -1 or other.degree() == -1:
            return total
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
        Raises the polynomial to a power (self ** exponent).
        `exponent` must be an integer and >= 0.
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

    def __mod__(self, other):
        """
        Computes `self % other` as follows:
        1. Create list of polynomials congruent to x^i mod other,
           for i from 0 up to self.degree().
           Each of these is reduced so its degree is less than other.degree().
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

    # for easier readability
    def __floordiv__(self, other):
        quo, _ = eucdiv(self, other)
        return quo

    # used for FactorList sorting
    def __lt__(self, other):
        """
        Compares two polynomials lexicographically.
        
        If degrees are unequal, the lower degree is smaller.
        Otherwise, scan down the coefficients list starting
        from the highest-degreee coefficient until we find
        a pair of different coefficients, then compare those.
        If we scan all coefficients and all are equal, the polynomials
        are equal.
        """
        # assumes normalized
        
        # unequal degree => compare degrees
        if self.degree() != other.degree():
            return self.degree() < other.degree()
        
        # now degrees are equal
        
        # edge cases out of the way

        # if one of them is the zero polynomial,
        # then so is the other, and 0 < 0 is False
        if self.is_zero():
            return False
        
        # if they're constants, compare their values
        if self.degree() == 1:
            return self.coeffs[0] < other.coeffs[0]
        
        # now check their coefficients in descending order
        for i in reversed(range(len(self.coeffs))):
            if self.coeffs[i] != other.coeffs[i]:
                return self.coeffs[i] < other.coeffs[i]

        # finally, we've scanned the coefficients on both
        # and found no mismatches
        # they are equal
        return False

    def __le__(self, other):
        """
        Non-strict comparison.
        """
        return self == other or self < other
    
    def peval(self, x: int):
        """
        Evaluates the polynomial at a point.
        Implemented naively: compute x^i mod FCH iteratively,
        and add to the running total.
        """
        # special case: polynomial is constant or needs to be eval'd at 0
        if self.degree() <= 0 or x == 0:
            return self.coeffs[0]
        
        result = 0
        power = 1 # holds x^i mod FCH
        for i in range(self.degree()+1):
            result = (result + power * self.coeffs[i]) % FCH
            power = (power * x) % FCH

        return result

    def deriv(self, order: int = 1):
        """
        Takes the derivative of a polynomial to the specified order.
        """
        order = int(order)
        if order < 0:
            raise ValueError(f"Cannot take derivative of order {order} -- "+
                             "order is negative.")
        if order == 1:
            resultcfs = [0] * len(self.coeffs)
            for i in range(len(self.coeffs)):
                # self.coeffs[i] * x^i --> i * self.coeffs[i] * x^(i-1)
                # derivative power rule
                resultcfs[i] = (i * self.coeffs[i]) % FCH
            result = Poly(resultcfs[1:])
            result.normalize()
            return result
        # order 2 or higher -- recursive
        return self.deriv(order-1).deriv()
                

def monomial(coeff: int=1, deg: int=0):
    """
    Creates a monomial equal to coeff * x^deg. Auxiliary.
    """
    return Poly([0]*deg + [coeff])

def constant(value: int):
    """
    Creates a constant polynomial. Auxiliary.
    Equivalent to monomial(value, 0).
    """
    return Poly([value])

def x_power_modulo(deg: int, f):
    """
    Creates a polynomial congruent to x^deg modulo f.
    """
    # repeated squaring
    
    # 1 mod anything is 1
    if deg == 0:
        return constant(1)
    if deg == 1:
        return monomial(deg=1) % f
    k = deg // 2
    temp = x_power_modulo(k, f)
    result = (temp * temp) % f
    if deg % 2 == 1:
        result = (result * monomial(deg=1)) % f
    return result

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

def eucdiv(dividend, divisor):
    """
    performs Euclidean division, outputting a tuple of quotient and remainder

    dividend: Poly
    divisor: Poly
    """
    quotient = constant(0)
    remainder = Poly(dividend.coeffs)
    if divisor.is_zero():
        raise ZeroDivisionError
    if divisor.degree() == 0:
        remainder = remainder.scale(pow(divisor.coeffs[0], -1, FCH))
        return (remainder, constant(0))
    leading_coeff = divisor.coeffs[-1]
    while remainder.degree() >= divisor.degree():
        # calculate the monomial a*x^n to cancel out the leading term of the dividend
        # a is quotcoeff, n is remainder.degree() - divisor.degree()
        quotcoeff = remainder.coeffs[-1] * pow(leading_coeff, -1, FCH)
        # making the monomial; coeffs are n zeros followed by quotcoeff
        monom = monomial(coeff = quotcoeff,
                         deg = remainder.degree()-divisor.degree())
        quotient = quotient + monom
        remainder = remainder - divisor * monom
    return (quotient, remainder)

def ext_euclid_algo(poly1, poly2):
    """
    Extended Euclidean algorithm.
    Computes the greatest common divisor `gcd` of `poly1` and `poly2`,
    as well as the coefficients `coeff1` and `coeff2`
    (themselves polynomials) that make the following equality true:

    gcd == coeff1 * poly1 + coeff2 * poly2
    returns gcd, coeff1, coeff2 in that order
    """
    # edge cases: one of the polynomials is constant or 0
    # zero
    if poly1.degree() == -1:
        # gcd(0, poly2) = poly2
        return (poly2.__copy__(), constant(0), constant(1))
    if poly2.degree() == -1:
        # gcd(poly1, 0) = poly1
        return (poly1.__copy__(), constant(1), constant(0))
    # constant
    if poly1.degree() == 0:
        # gcd(c, poly2) = 1 = c^-1 * c + 0 * poly2
        return (Poly([1]),
                constant(pow(poly1.coeffs[0], -1, FCH)),
                constant(0))
    if poly2.degree() == 0:
        # gcd(poly1, c) = 1 = 0 * poly1 + c^-1 * poly2
        return (Poly([1]),
                constant(0),
                constant(pow(poly2.coeffs[0], -1, FCH)))

    # so now that the polynomials are at least linear
    # we can actually start cooking
    # the number of EEA iterations is at most this much,
    # since the degree goes down by 1 every time:
    iters = min(poly1.degree(), poly2.degree()) + 1

    # initialize these lists to have the required length
    # because messing with appends failed spectacularly
    rems = [poly1.__copy__(), poly2.__copy__()] + [constant(0)] * iters
    quots = [constant(0)] * (iters+2)
    coe1 = [constant(1), constant(0)] + [constant(0)] * iters
    coe2 = [constant(0), constant(1)] + [constant(0)] * iters
    
    # recurrence relations can actually be written directly in code now
    for i in range(1, len(rems)-1):
        # if current remainder is 0, we are done
        if rems[i].is_zero():
            break
        quots[i], rems[i+1] = eucdiv(rems[i-1], rems[i])
        coe1[i+1] = coe1[i-1] - quots[i] * coe1[i]
        coe2[i+1] = coe2[i-1] - quots[i] * coe2[i]

    # so now we have our rems, we need to find the last nonzero one
    k = len(rems)-1
    while rems[k].is_zero():
        k -= 1

    # QoL: make the GCD monic
    # given that neither poly1 nor poly2 is 0,
    # the GCD won't be either
    gcd, coe1, coe2 = rems[k], coe1[k], coe2[k]
    leadcoe_inv = pow(gcd.coeffs[-1],-1,FCH)

    gcd = gcd.scale(leadcoe_inv)
    coe1 = coe1.scale(leadcoe_inv)
    coe2 = coe2.scale(leadcoe_inv)
    
    return (gcd, coe1, coe2)
