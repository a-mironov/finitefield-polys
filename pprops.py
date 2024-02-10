# pprops module

# contains logic for testing polynomial properties
# irreducibility and (eventually) primitivity

import polynomial as pol

def prime_factors(n: int):
    """
    Returns a list of all prime factors of n.
    Multiplicities unneeded, thus not returned.
    """
    if n <= 0:
        raise ValueError("Attempted to factorize "+
                         f"nonpositive integer {n}!")
    if n == 1:
        return []
    if pol.is_prime(n):
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
        while not pol.is_prime(p):
            p += 1
    if n > 1:
        factors.append(n)
    return factors
        

def xqpower(n: int, f):
    """
    Calculates x^(FCH^n) modulo polynomial f.
    Used for x^(FCH^n) - x; the -x is added beyond this function.
    (i.e. (x^(FCH^n) - x) mod f is
    `xqpower(n, f) - pol.monomial(deg=1)`
    """
    # we're not gonna call this on constants or linears
    # but that case needs to be handled anyway
    if f.degree() <= 0:
        raise ValueError("Cannot reduce modulo a constant polynomial!")
    if f.degree() == 1:
        # a^FCH == a for all a in the base field
        # so the value of x^(FCH^n) - x at x=a will always be 0
        return pol.monomial(coeff=0)
    # and another edge case: n = 0
    if n == 0:
        # x^(FCH^0) = x^1
        return pol.monomial(coeff=1, deg=1)

    result = pol.monomial(coeff=1, deg=1)
    for i in range(n):
        # worst-case space complexity is FCH * f.degree()
        result = (result ** pol.FCH) % f
    return result

def is_irreducible(poly):
    """
    Checks polynomial `poly`, copied as `f`, for irreducibility.
    Returns:
    - True if the polynomial is irreducible, False otherwise.
    - reason: the reason for (ir)reducibility.
    
    Uses Rabin's test of irreducibility:
    Letting n = deg(f),
    p_0, ..., p_k be the prime factors of n,
    n_i = n // p_i,
    `f` is irreducible if and only if both of the following conditions
    are true:
    1. gcd(f, x^(FCH^n_i) - x) = 1 for all i
    2. f divides x^(FCH^n) - x

    implementation detail:
    since storing x^(q^n_i) - x and x^(q^n) - x directly would be
    prohibitively expensive due to their high degree,
    they are calculated modulo `f` via the helper function
    xqpower(n, f).
    """
    reason = ""
    # get some edge cases out of the way first!
    
    # constant => NOT irreducible
    if poly.degree() <= 0:
        reason = "Constant"
        return (False, reason)
    
    # linear => irreducible ALWAYS
    if poly.degree() == 1:
        reason = "Linear"
        return (True, reason)
    
    # check if polynomial has a root.
    # if it does, it's NOT irreducible
    # (since its degree is >= 2 if we made it this far)
    for point in range(pol.FCH):
        if poly.peval(point) == 0:
            reason = f"Has root {point}"
            return (False, reason)
        
    # at this point, the polynomial's degree is >= 2
    # and it has been checked not to have any roots
    # if its degree is 2 or 3,
    # then it has no linear factors,
    # and is thus irreducible.
    if poly.degree() <= 3:
        if poly.degree() == 2:
            reason = "Quadratic "
        if poly.degree() == 3:
            reason = "Cubic "
        reason += "with no linear factors"
        return (True, reason)
    
    # last edge case: polynomial has repeated factors
    # tested as computing GCD with its own derivative
    # if GCD isn't constant, f and f' have a common
    # factor, and thus f is NOT irreducible.
    gcd, _, _ = pol.ext_euclid_algo(poly, poly.deriv())
    if gcd.degree() > 0:
        reason = f"Repeated factor: {str(gcd)}"
        return (False, reason)

    # and now time for Rabin's test!

    # the test requires its input to be monic
    # scaling doesn't affect irreducibility
    f = poly.monify()
    # get the degree as well
    n = f.degree()

    # p_i and n_i (see docstring)
    primes = prime_factors(n)
    prime_complements = []
    for p in primes:
        prime_complements.append(n // p)

    # testing coprimality with x^(FCH^n_i) - x
    # if f fails to be coprime to one of them,
    # then f is NOT irreducible.
    for ni in prime_complements:
        x_q_ni = xqpower(ni,f) - pol.monomial(deg=1)
        gcd, _, _ = pol.ext_euclid_algo(x_q_ni, f)
        if gcd.degree() > 0:
            reason = ("Rabin's test failed -- "+
                      f"not coprime to x^({pol.FCH}^{ni}) - x: "+
                      f"gcd({f}, {x_q_ni}) = {gcd}")
            return (False, reason)

    # now f is coprime with x^(FCH^n_i) - x
    # if it DIVIDES x^(FCH^n) - x,
    # then it's irreducible.
    # otherwise it is not.
    x_q_n = xqpower(n, f) - pol.monomial(deg=1)
    # x_q_n is actually (x^(FCH^n_i) - x) % f
    # so f divides x^(FCH^n_i) - x
    # is equivalent to x_q_n == 0
    if x_q_n.is_zero():
        reason = ("Rabin's test failed -- "+
                 f"Not a factor of x^({pol.FCH}^{n}) - x")
    reason = "Rabin's test passed"
    return (True, reason)
