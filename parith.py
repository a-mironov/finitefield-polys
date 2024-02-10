# parith (polynomial arithmetic) module

# contains functions to interface arithmetic with polynomial storage

import polynomial as pol

def addmake_poly(name1: str, name2: str, result: str):
    """
    Reads polynomials `poly1` and `poly2` from poly_dict,
    adds them, and stores the result under name `result`.

    name1: str -- name of the first polynomial to be summed
    name2: str -- name of the second polynomial to be summed
    result: str -- name under which to store the result
    """
    # read polynomials from dict
    try:
        addend1 = pol.poly_dict[name1]
        addend2 = pol.poly_dict[name2]
    except KeyError as e:
        raise e
    # ensure name `result` does not exist
    if result in pol.poly_dict.keys():
        raise ValueError(f"Cannot store addition result -- name '{result}' "+
                         "already in use.")
    # now we have our polys and can add them
    total = addend1 + addend2
    # not calling make_poly b/c the polynomial object is already there
    pol.poly_dict[result] = total

def listaddmake_poly(addends: list, result: str):
    """
    Reads all polynomials by names in list `addends` from poly_dict,
    adds them up, and stores the result in `result`.
    """
    # ensure name `result` does not exist
    if result in pol.poly_dict.keys():
        raise ValueError(f"Cannot store summation result -- name '{result}' "+
                         "already in use.")
    total = pol.constant(0)
    # read polynomials from dict
    for name in addends:
        try:
            poly = pol.poly_dict[name]
            total = total + poly
        except KeyError as e:
            raise e
    pol.poly_dict[result] = total

def submake_poly(name1: str, name2: str, result: str):
    """
    Reads polynomials `poly1` and `poly2` from poly_dict,
    subtracts them, and stores the result under name `result`.

    name1: str -- name of the first polynomial to be summed
    name2: str -- name of the second polynomial to be summed
    result: str -- name under which to store the result
    """
    # read polynomials from dict
    try:
        addend1 = pol.poly_dict[name1]
        addend2 = pol.poly_dict[name2]
    except KeyError as e:
        raise e
    # ensure name `result` does not exist
    if result in pol.poly_dict.keys():
        raise ValueError(f"Cannot store subtraction result -- name '{result}' "+
                         "already in use.")
    # now we have our polys and can subtract them
    total = addend1 - addend2
    # not calling make_poly b/c the polynomial object is already there
    pol.poly_dict[result] = total

def mulmake_poly(name1: str, name2: str, result: str):
    """
    Reads polynomials `poly1` and `poly2` from poly_dict,
    multiplies them, and stores the result under name `result`.

    name1: str -- name of the first polynomial to be summed
    name2: str -- name of the second polynomial to be summed
    result: str -- name under which to store the result
    """
    # read polynomials from dict
    try:
        addend1 = pol.poly_dict[name1]
        addend2 = pol.poly_dict[name2]
    except KeyError as e:
        raise e
    # ensure name `result` does not exist
    if result in pol.poly_dict.keys():
        raise ValueError(f"Cannot store multiplication result -- name '{result}' "+
                         "already in use.")
    # now we have our polys and can multiply them
    total = addend1 * addend2
    # not calling make_poly b/c the polynomial object is already there
    pol.poly_dict[result] = total

def listmulmake_poly(factors: list, result: str):
    """
    Reads all polynomials by names in list `addends` from poly_dict,
    multiplies them together, and stores the result in `result`.
    """
    # ensure name `result` does not exist
    if result in pol.poly_dict.keys():
        raise ValueError(f"Cannot store product result -- name '{result}' "+
                         "already in use.")
    total = pol.constant(1)
    # read polynomials from dict
    for name in factors:
        try:
            poly = pol.poly_dict[name]
            total = total * poly
        except KeyError as e:
            raise e
    pol.poly_dict[result] = total
     
def powmake_poly(basename: str, exponent: int, result: str):
    """
    Reads polynomial `basename` from poly_dict,
    raises it to exponent `exponent`, and stores the result
    under name `result`.

    basename: str -- name of the polynomial to be exponentiated
    exponent: int -- the exponent
    result: str -- name under which to store the result
    """
    try:
        base = pol.poly_dict[basename]
    except KeyError as e:
        raise e
    if result in pol.poly_dict.keys():
        raise ValueError(f"Cannot store exponentiation result -- name '{result}' "+
                         "already in use.")
    try:
        power = base ** exponent
    except ValueError as e:
        raise e
    else:
        pol.poly_dict[result] = power

def eucdivmake_poly(divname: str, divisorname: str, quotname: str, remname: str):
    """
    Performs Euclidean division on polynomials
    `divname` and `divisorname`, and stores
    the results under names `quotname` and `remname`.

    divname: str -- name of the dividend
    divisorname: str -- name of the divisor
    quotname: str -- name to store the quotient
    remname: str -- name to store the remainder
    """
    # read polynomials
    try:
        dividend = pol.poly_dict[divname]
        divisor = pol.poly_dict[divisorname]
    except KeyError as e:
        raise e
    # ensure quotname and remname don't exist
    for key in [quotname, remname]:
        if key in pol.poly_dict.keys():
            raise ValueError("Cannot store division result -- "+
                             f"name '{result}' already in use.")
    # now we can do the division
    try:
        quotient, remainder = pol.eucdiv(dividend, divisor)
    except ZeroDivisionError:
        raise ZeroDivisionError
    pol.poly_dict[quotname] = quotient
    pol.poly_dict[remname] = remainder

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
        dividend = pol.poly_dict[divname]
        modulus = pol.poly_dict[modname]
    except KeyError as e:
        raise e
    # ensure result doesn't exist
    if result in pol.poly_dict.keys():
        raise ValueError("Cannot store modular reduction result -- "+
                         f"name '{result}' already in use.")
    try:
        remainder = dividend % modulus
    except ZeroDivisionError as e:
        raise e
    except ArithmeticError as e:
        raise e

    pol.poly_dict[result] = remainder

def eea_make_poly(name1: str, name2: str, gcdname: str,
                  coe1name: str, coe2name: str):
    """
    Finds the GCD and Bezout coefficients of polynomials
    by names `name1` and `name2`, and stores the result
    under names `gcdname`, `coe1name` and `coe2name`.
    """
    # read polynomials
    try:
        poly1 = pol.poly_dict[name1]
        poly2 = pol.poly_dict[name2]
    except KeyError as e:
        raise e
    # ensure destination names don't exist
    for key in [gcdname, coe1name, coe2name]:
        if key in pol.poly_dict.keys():
            raise ValueError("Cannot store extended Euclidean "+
                             "algorithm result -- "+
                             f"name '{result}' already in use.")

    gcd, coe1, coe2 = pol.ext_euclid_algo(poly1, poly2)
    pol.make_poly(gcdname, gcd.coeffs)
    pol.make_poly(coe1name, coe1.coeffs)
    pol.make_poly(coe2name, coe2.coeffs)

def diffmake_poly(name: str, order: int, result: str):
    """
    Takes the derivative of polynomial `name`
    of order `order`, and stores the result
    under name `result`.
    """
    # read polynomial
    try:
        poly = pol.poly_dict[name]
    except KeyError as e:
        raise e
    # ensure destination name doesn't exist
    if result in pol.poly_dict.keys():
        raise ValueError("Cannot store differentiation result -- "+
                         f"name {result} already in use.")
    if order == 0:
        pol.copy_poly(name, result)
    poly_diffd = poly.deriv(order)
    pol.poly_dict[result] = poly_diffd
