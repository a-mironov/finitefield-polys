# auxiliaries module

# contains various minor functions
# used in various places throughout the program
# created to eliminate dependency hell

# used only for primality checks
from math import sqrt, floor

def ordinal_suffix(n: int):
    """
    Returns the English ordinal suffix (-st, -nd, -rd, or -th)
    of the specified number n. Auxiliary.
    """
    if n < 0:
        return ordinal_suffix(-n)
    # 10th through 19th
    if n % 100 in range(10, 20):
        return "th"
    # ends in 1 => (fir)st, 2 => (seco)nd, 3 => (thi)rd,
    # anything else => (four, fif, six, seven, eigh, nin)th
    # all multiples of 10 get -th as well
    match (n % 10):
        case 1:
            return "st"
        case 2:
            return "nd"
        case 3:
            return "rd"
        case _:
            return "th"

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

def prime_factors(n: int):
    """
    Returns a list of all prime factors of n.
    Multiplicities unneeded, thus not returned.
    Auxiliary.
    """
    if n <= 0:
        raise ValueError("Attempted to factorize "+
                         f"nonpositive integer {n}!")
    if n == 1:
        return []
    if is_prime(n):
        return [n]
    factors = []
    p = 2
    while p * p <= n:
        # if n is divisible by p, add it to the list
        # and divide out by it as much as possible
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
        # move on to the next prime
        p += 1
        while not is_prime(p):
            p += 1
    if n > 1:
        factors.append(n)
    return factors

def proper_factors(n: int):
    """
    Returns a sorted list of all factors of a number.
    """
    # edge cases
    if n == 0:
        raise ValueError("Cannot factorize 0.")
    if n < 0:
        return proper_factors(-n)
    if n == 1 or is_prime(n):
        return []

    # do this in O(sqrt(n)) time by only iterating up to that.
    # all big factors are n // (small factor).
    small_factors = []
    big_factors = []
    root = floor(sqrt(n))

    # iterate up to and INCLUDING root
    for i in range(2, root+1):
        if n % i == 0:
            small_factors.append(i)
            big_factors.append(n // i)
            
    # if n is a perfect square (== root * root),
    # then root will appear in both big and small factor lists.
    # it is the largest small factor and the smallest big factor.
    if root * root == n:
        del small_factors[-1]

    big_factors.reverse()
    factors = small_factors + big_factors
    return factors
    

def parse_lincomb(arguments: list):
    """
    parses argument list for `lincomb` command
    assumes the last argument (`result`) is NOT present, i.e. only inputs
    attempts to parse arguments as alternating weights and polynomials
    """
    if len(arguments) % 2 == 1:
        raise ValueError(f"Invalid argument count -- expected an even number, read {len(arguments)}.")
    
    weights = []
    polynames = []
    for i in range(len(arguments)):
        # even positions expect weights
        if i % 2 == 0:
            try:
                weights.append(int(arguments[i]))
            except ValueError:
                raise ValueError(f"Could not parse {arguments[i]} as integer!")
        else:
            name = arguments[i]
            if name not in polynomial.poly_dict.keys():
                raise KeyError(name)
            polynames.append(name)
    return (weights, polynames)
