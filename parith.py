# parith (polynomial arithmetic) module

# contains functions to interface arithmetic with polynomial storage
# as well as euclidean division

import polynomial

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
        addend1 = polynomial.poly_dict[name1]
        addend2 = polynomial.poly_dict[name2]
    except KeyError as e:
        raise e
    # ensure name `result` does not exist
    if result in polynomial.poly_dict.keys():
        raise ValueError(f"Cannot store addition result -- name '{result}' "+
                         "already in use.")
    # now we have our polys and can add them
    total = addend1 + addend2
    # not calling make_poly b/c the polynomial object is already there
    polynomial.poly_dict[result] = total

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
        addend1 = polynomial.poly_dict[name1]
        addend2 = polynomial.poly_dict[name2]
    except KeyError as e:
        raise e
    # ensure name `result` does not exist
    if result in polynomial.poly_dict.keys():
        raise ValueError(f"Cannot store subtraction result -- name '{result}' "+
                         "already in use.")
    # now we have our polys and can subtract them
    total = addend1 - addend2
    # not calling make_poly b/c the polynomial object is already there
    polynomial.poly_dict[result] = total

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
        addend1 = polynomial.poly_dict[name1]
        addend2 = polynomial.poly_dict[name2]
    except KeyError as e:
        raise e
    # ensure name `result` does not exist
    if result in polynomial.poly_dict.keys():
        raise ValueError(f"Cannot store multiplication result -- name '{result}' "+
                         "already in use.")
    # now we have our polys and can multiply them
    total = addend1 * addend2
    # not calling make_poly b/c the polynomial object is already there
    polynomial.poly_dict[result] = total
    
    
def powmake_poly(basename: str, exponent: int, result: str):
    """
    raises a polynomial to an exponent and stores the result

    basename: str -- name of the polynomial to be exponentiated
    exponent: int -- the exponent
    result: str -- name under which to store the result
    """
    try:
        base = polynomial.poly_dict[basename]
    except KeyError as e:
        raise e
    if result in polynomial.poly_dict.keys():
        raise ValueError(f"Cannot store exponentiation result -- name '{result}' "+
                         "already in use.")
    try:
        power = base ** exponent
    except ValueError as e:
        raise e
    else:
        polynomial.poly_dict[result] = power

def eucdiv(dividend, divisor):
    """
    performs Euclidean division, outputting a tuple of quotient and remainder

    dividend: Poly
    divisor: Poly
    """
    quotient = polynomial.Poly([0])
    remainder = polynomial.Poly(dividend.coeffs)
    if divisor.degree == -1:
        raise ZeroDivisionError
    if divisor.degree == 0:
        remainder = remainder.scale(pow(divisor[0], -1, polynomial.FCH))
        return (remainder, polynomial.Poly([0]))
    leading_coeff = divisor.coeffs[-1]
    while remainder.degree() >= divisor.degree():
        # calculate the monomial a*x^n to cancel out the leading term of the dividend
        # a is quotcoeff, n is remainder.degree() - divisor.degree()
        quotcoeff = remainder.coeffs[-1] * pow(leading_coeff, -1, polynomial.FCH)
        # making the monomial; coeffs are n zeros followed by quotcoeff
        monom = polynomial.Poly([0]*(remainder.degree()-divisor.degree()) + [quotcoeff])
        quotient = quotient + monom
        remainder = remainder - divisor * monom
    return (quotient, remainder)

def eucdivmake_poly(divname: str, divisorname: str, quotname: str, remname: str):
    """
    performs Euclidean division and stores the results

    divname: str -- name of the dividend
    divisorname: str -- name of the divisor
    quotname: str -- name to store the quotient
    remname: str -- name to store the remainder
    """
    # read polynomials
    try:
        dividend = polynomial.poly_dict[divname]
        divisor = polynomial.poly_dict[divisorname]
    except KeyError as e:
        raise e
    # ensure quotname and remname don't exist
    for key in [quotname, remname]:
        if key in polynomial.poly_dict.keys():
            raise ValueError("Cannot store division result -- "+
                             f"name '{result}' already in use.")
    # now we can do the division
    try:
        quotient, remainder = eucdiv(dividend, divisor)
    except ZeroDivisionError:
        raise ZeroDivisionError
    polynomial.poly_dict[quotname] = quotient
    polynomial.poly_dict[remname] = remainder

def modmake_poly(divname: str, modname: str, result: str):
    """
    Reduces polynomial `divname` modulo polynomial `modname`
    and stores the result in `result`.

    divname: str -- name of the divisor
    modname: str -- name of the modulus
    result: str -- name of the result
    """
    # read polynomials
    try:
        dividend = polynomial.poly_dict[divname]
        modulus = polynomial.poly_dict[modname]
    except KeyError as e:
        raise e
    # ensure result doesn't exist
    if result in polynomial.poly_dict.keys():
        raise ValueError("Cannot store modular reduction result -- "+
                         f"name '{result}' already in use.")
    try:
        remainder = dividend % modulus
    except ZeroDivisionError as e:
        raise e
    except ArithmeticError as e:
        raise e

    polynomial.poly_dict[result] = remainder
