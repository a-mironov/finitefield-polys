# nonprimefield module

# contains logic for GF(p^n) arithmetic
# field operations and exponentiation
# latter is done thru a lookup table

import polynomial as pol
import pprops

class FieldEl():
    # polynomial that defines the field
    quotpoly = None
    # power lookup for multiplication and addition
    powers = None
    
    def setfield(poly):
        """
        Sets the polynomial `poly` such that F_p[x]/(poly) = GF(p^n).
        p = pol.FCH, the field characteristic.
        Prepares the exponential lookup table (actually a list).
        Flushes all stored field elements.

        Input `poly` must be a primitive polynomial.
        """
        if not pprops.is_primitive(poly):
            raise ValueError("Cannot initialize finite field "
                             f"GF({pol.FCH}^{poly.degree()}) "
                             f"on polynomial {str(poly)} -- "
                             "Not primitive.")
        
        # constant multiplier makes no difference
        # but it's nice to have quotpoly be monic
        FieldEl.quotpoly = poly.monify()

        p = pol.FCH
        n = poly.degree()

        fieldsize = p ** n - 2

        power_lookup = [pol.constant(1)]
        for i in range(1,p**n - 1):
            next_power = ( (power_lookup[-1] * pol.monomial(1,1))
                           % FieldEl.quotpoly)
            power_lookup.append(next_power.__copy__())
            if i % 10000 == 0:
                print(f"Computed powers up to {i} of {fieldsize}...")

        FieldEl.powers = power_lookup

    setfield = staticmethod(setfield)

    def __init__(self, inp):
        """
        Initializes field element based on input,
        which can be either a Poly or a coefficient list.
        """
        if isinstance(inp, pol.Poly):
            self.poly = inp % FieldEl.quotpoly
        elif isinstance(inp, list):
            self.poly = pol.Poly(inp) % FieldEl.quotpoly
        elif isinstance(inp, int):
            self.poly = pol.constant(inp)
            
        if self.poly.is_zero():
            self.dlog = None
        else:
            self.dlog = FieldEl.powers.index(self.poly)

    def __str__(self):
        # prints the same as polynomials
        # but with 'a' as the variable
        return self.poly.str_custom(varname="a")

    def __eq__(self, other):
        return self.poly == other.poly

    def __add__(self, other):
        """
        Addition as polynomials.
        Reduction modulo quotpoly is handled by init method.
        """
        return FieldEl(self.poly + other.poly)

    def __sub__(self, other):
        """
        Subtraction is basically the same as addition.
        """
        return FieldEl(self.poly - other.poly)

    def __mul__(self, other):
        """
        multiplication using the lookup table.
        """
        # either factor is 0 => product is 0
        if self.poly.is_zero() or other.poly.is_zero():
            return FieldEl(0)

        if isinstance(other, int):
            return FieldEl(self.poly.scale(other))

        # otherwise, a * b = powers[a.dlog + b.dlog]
        idx = (self.dlog + other.dlog) % len(FieldEl.powers)
        return FieldEl(FieldEl.powers[idx])

    def __truediv__(self, other):
        """
        division using the lookup table.
        """
        # NOT eucdiv!!! this is a field!

        if other.poly.is_zero():
            raise ZeroDivisionError("Cannot divide by zero in "+
                                    "finite field modulo "+
                                    str(FieldEl.quotpoly))

        if self.poly.is_zero():
            return FieldEl(0)

        # otherwise, a / b = powers[a.dlog - b.dlog]
        idx = (self.dlog - other.dlog) % len(FieldEl.powers)
        return FieldEl(FieldEl.powers[idx])

    def __pow__(self, n: int):
        """
        Exponentiation using the lookup table.
        """

        if self.poly.is_zero():
            return FieldEl(0)

        idx = (self.dlog * n) % len(FieldEl.powers)
        return FieldEl(FieldEl.powers[idx])
