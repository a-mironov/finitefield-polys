# data management module

# contains logic for polynomial and fieldel storage
# as well as interfacing with arithmetic

# polynomials used to be handled by parith

import functools

import auxiliaries as aux
import polynomial as pol
import nonprimefield as npf

# dict for storing both polynomials and fieldels
obj_dict = {}

# helpers

# these are migrated from main
def set_characteristic(new_char: int):
    """
    Resets the characteristic of the base field.
    Unless the old value matches the new, flushes all stored
    polynomials and field elements.

    new_char: int -- the new value of the characteristic
    """
    # if new characteristic is the same as the old, do nothing
    if new_char == pol.FCH:
        return
    elif new_char <= 1:
        raise ValueError(f"Invalid characteristic value {new_char} -- "+
                         "Not a natural number.")
    elif not aux.is_prime(new_char):
        raise ValueError(f"Invalid characteristic value {new_char} -- "+
                         "Not prime.")
    else:
        # new characteristic is prime and differs from old
        pol.FCH = new_char
        # flushing stored objects
        obj_dict.clear()
        # resetting non-prime field
        npf.FieldEl.quotpoly = None
        npf.FieldEl.powers = []

def set_field(new_qpoly_name: str):
    """
    Resets the defining polynomial of the non-prime field.
    Flushes all current fieldels stored.
    """
    if new_qpoly_name not in obj_dict.keys():
        print(f"Polynomial {new_qpoly_name} not found!")
        return
    if type(obj_dict[new_qpoly_name]) == npf.FieldEl:
        print(f"{new_qpoly_name} must be a polynomial!")
        return
    try:
        npf.FieldEl.setfield(obj_dict[new_qpoly_name])
    except ValueError as e:
        print(e)
    else:
        mass_delete("el")
        print("Quotient polynomial set to "
              f"{str(obj_dict[new_qpoly_name].monify())} "
              "successfully.")

def group_convert(names: list):
    """
    Queries obj_dict for all stored objects.
    KeyErrors handled upstream.
    """
    return [obj_dict[name] for name in names]

def get_names_by_type(mode: str):
    if mode not in ["poly", "el"]:
        raise ValueError(f"Invalid mode '{mode}'!")
    match mode:
        case "poly":
            type_ = pol.Poly
        case "el":
            type_ = npf.FieldEl

    names = []
    for k in obj_dict.keys():
        if type(obj_dict[k]) == type_:
            names.append(k)

    return sorted(names)

def get_type(name: str):
    """
    Returns the string 'Polynomial' or 'Field element'
    according to the type of the object.
    """
    if name not in obj_dict.keys():
        raise KeyError(name)
    if type(obj_dict[name]) == pol.Poly:
        return "Polynomial"
    if type(obj_dict[name]) == npf.FieldEl:
        return "Field element"
    return "Unknown type"

# non-calculative data management

def make(name: str, coefficients: list, mode: str = "poly"):
    """
    Makes a new polynomial and adds it to the dict.

    name: str - the name of the polynomial
    coefficients: list - the coefficients of the polynomial
    """
    # possible exceptions: 2
    # 1. bad name: supplied name is already found in the dict

    if mode not in ["poly", "el"]:
        raise ValueError(f"Invalid creation mode '{mode}'!")
    if name in obj_dict.keys():
        raise ValueError(f"Name {name} already in use! "
                         "Use `update` to overwrite polynomials "
                         "and field elements.")
    
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
    if mode == "poly":
        obj_dict[name] = pol.Poly(cfs_clean)
    elif mode == "el":
        obj_dict[name] = npf.FieldEl(cfs_clean)
    else:
        raise ValueError("Something went disastrously wrong.")

def delete(name: str):
    """
    deletes an object from the dict

    name: str - the name of the object 
    """
    # possible exceptions: 1
    # 1. bad name: polynomial by that name doesn't exist in obj_dict anyway
    if name not in obj_dict.keys():
        raise KeyError(name)

    # if we made it here, the name is good and deletable
    obj_dict.pop(name)

def display(name: str):
    """
    outputs a string representation of the given poly or el
    """
    obj = obj_dict[name]
    match type(obj):
        case pol.Poly:
            typetag = "[p] "
        case npf.FieldEl:
            typetag = "[e] "
        case _:
            typetag = "[?] "
    return typetag + name + " = " + str(obj)

def display_all(mode: str = "all"):
    """
    outputs a string representation for the entire dict
    or only polys or els
    """
    if mode not in ["all", "el", "poly"]:
        raise ValueError(f"Invalid display-all mode '{mode}'!")

    if mode == "all":
        dispkeys = sorted(obj_dict.keys())
    else:
        dispkeys = get_names_by_type(mode)
            
    displayed_objs = [display(name) for name in dispkeys]

    return "\n".join(displayed_objs)

def update(name: str, coeffs: list):
    """
    updates a polynomial with new coefficients
    the value of the old polynomial is discarded

    name: str - the name of the polynomial
    coefficients: list - the new coefficients of the polynomial
    """
    if name not in obj_dict.keys():
        raise KeyError(name)

    if type(obj_dict[name]) == pol.Poly:
        mode = "poly"
    else:
        mode = "el"

    delete(name)
    make(name, coeffs, mode)

def copy(source: str, dest: str):
    """
    copies a polynomial or fieldel

    source: str -- name of the source polynomial
    dest: str -- name of the destination
    """
    try:
        obj = obj_dict[source]
    except KeyError as e:
        raise KeyError(source)

    if type(obj) is pol.Poly:
        cfs = obj.coeffs
        mode = "poly"
    elif type(obj) is npf.FieldEl:
        cfs = obj.poly.coeffs
        mode = "el"
    
    if dest in obj_dict.keys():
        update(dest, cfs, mode)
    else:
        make(dest, cfs, mode)

def rename(oldname: str, newname: str):
    """
    renames a poly or el
    """
    try:
        obj = obj_dict[oldname]
    except KeyError:
        raise KeyError(oldname)

    if newname in obj_dict.keys():
        raise ValueError(f"{get_type(obj_dict[newname])} "
                         f"by name {newname} already exists.")

    obj_dict[newname] = obj
    obj_dict.pop(oldname)

def mass_delete(mode: str = "all"):
    """
    Deletes either all polys, or all els, or everything.
    """
    if mode not in ["all", "el", "poly"]:
        raise ValueError(f"Invalid deletion mode '{mode}'!")

    if mode == "all":
        obj_dict.clear()
    else:
        names_to_delete = get_names_by_type(mode)
        for name in names_to_delete:
            obj_dict.pop(name)

# operate on polynomials or fieldels

def opmake(names: list, result: str,
           op):
    """
    Operates on polynomials or fieldels from the dict,
    then stores the result in the same dict.
    """
    try:
        polys = group_convert(names)
    except KeyError as e:
        raise e
    obj_dict[result] = functools.reduce(op, polys)


# operation-specific functions for + - * **

def addmake(names, result):
    try:
        opmake(names, result, lambda x, y: x + y)
    except KeyError as e:
        raise e
    except AttributeError:
        raise AttributeError("Cannot add polynomials and "
                             "field elements!")

def submake(names, result):
    try:
        opmake(names, result, lambda x, y: x - y)
    except KeyError as e:
        raise e
    except AttributeError:
        raise AttributeError("Cannot subtract polynomials and "
                             "field elements!")  

def mulmake(names, result):
    try:
        opmake(names, result, lambda x, y: x * y)
    except KeyError as e:
        raise e
    except AttributeError:
        raise AttributeError("Cannot multiply polynomials and "
                             "field elements!")

def powmake(basename: str, exponent: int, result: str):
    """
    Reads polynomial `basename` from poly_dict,
    raises it to exponent `exponent`, and stores the result
    under name `result`.

    basename: str -- name of the polynomial to be exponentiated
    exponent: int -- the exponent
    result: str -- name under which to store the result
    """
    # exception handling relegated upstream
    base = obj_dict[basename]
    power = base ** exponent # can be either FieldEl or Poly

    obj_dict[result] = power

# fieldel-specific operations

def divmake_el(names, result):
    try:
        opmake(names, result, npf.FieldEl.__truediv__)
    except AttributeError:
        raise AttributeError("Cannot perform field division "
                             "with polynomials!")

# polynomial-specific operations
# incl. multi-output ones

def modmake_poly(divname: str, modname: str, result: str):
    """
    Reduces polynomial `divname` modulo polynomial `modname`
    and stores the result in `result`.

    divname: str -- name of the divisor
    modname: str -- name of the modulus
    result: str -- name of the result
    """
    polys = group_convert([divname, modname])
    for i in range(2):
        if type(polys[i]) != pol.Poly:
            raise TypeError("Cannot perform modulo on non-polynomials!")
    remainder = polys[0] % polys[1]
    obj_dict[result] = remainder

### LEGACY CODE RELOCATED FROM PARITH
# with some minor fixes

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
    # copy just in case
    dividend = obj_dict[divname].__copy__()
    divisor = obj_dict[divisorname].__copy__()

    # now we can do the division
    # ZeroDivisionError handled upstream
    quotient, remainder = pol.eucdiv(dividend, divisor)
    obj_dict[quotname] = quotient
    obj_dict[remname] = remainder

def eea_make_poly(name1: str, name2: str, gcdname: str,
                  coe1name: str, coe2name: str):
    """
    Finds the GCD and Bezout coefficients of polynomials
    by names `name1` and `name2`, and stores the result
    under names `gcdname`, `coe1name` and `coe2name`.
    """
    # read polynomials
    poly1 = obj_dict[name1]
    poly2 = obj_dict[name2]

    if type(poly1) != pol.Poly or type(poly2) != pol.Poly:
        raise TypeError("Cannot perform EEA on non-polynomials!")

    gcd, coe1, coe2 = pol.ext_euclid_algo(poly1, poly2)
    obj_dict[gcdname] = gcd
    obj_dict[coe1name] = coe1
    obj_dict[coe2name] = coe2

def diffmake_poly(name: str, order: int, result: str):
    """
    Takes the derivative of polynomial `name`
    of order `order`, and stores the result
    under name `result`.
    """
    # read polynomial
    poly = obj_dict[name]

    if type(poly) != pol.Poly:
        raise TypeError("Cannot take derivative of non-polynomials!")
    # ensure destination name doesn't exist

    if order == 0:
        obj_dict[result] = poly.__copy__()
    else:
        poly_diffd = poly.deriv(order)
        obj_dict[result] = poly_diffd
