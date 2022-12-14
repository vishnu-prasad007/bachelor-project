import random
from math import gcd
from mathlib import mod_inverse, solve_linear_congurence, is_prime


def __compute_next(x: int, g: int, y: int, a: int, b: int, p: int, order: int):
    """
    Computes x_(i+1), a_(i+1), b_(i+1) from x_i, a_i, b_i

    :param x: x_i in the random walk. Positive integer.
    :param g: Generator g of g^x = y (mod p). Positive integer.
    :param y: y of g^x = y (mod p). Positive integer.
    :param a: a_i in the random walk. Non-negative integer.
    :param b: b_i in the random walk. Non-negative integer.
    :param p: p of g^x = y (mod p). Prime number.
    :param order: order of g in (mod p). ie. Smallest i such that g^i = 1 (mod p). Positive integer.
    :returns: x_(i+1), a_(i+1), b_(i+1)
    """

    # By considering mod 3, it is determined if x belongs to S0, S1, or S2.
    # Compute the next x, a and b
    if x % 3 == 0:
        x = (x * x) % p
        a = (2 * a) % order
        b = (2 * b) % order
    elif x % 3 == 1:
        x = (x * y) % p
        b = (b + 1) % order
    else:
        x = (x * g) % p
        a = (a + 1) % order
    return x, a, b


def pollard_rho(g: int, y: int, p: int, order: int = 0, tries: int = 10, verify: bool = False) -> int:
    """
    Computes x such that g^x = y mod p using the Pollard Rho algorithm

    :param g: Generator g of g^x = y (mod p). Positive integer.
    :param y: y of g^x = y (mod p). Positive integer.
    :param p: p of g^x = y (mod p). Prime number.
    :param order: order of g in (mod p). ie. Smallest i such that g^i = 1 (mod p). Positive integer.
    :param tries: number of tries to run algorithm with varying starting points (a and b). Positive integer.
    :param verify: Checks if p is prime when True
    :returns: A non-negative integer x such that g^x = y (mod p) or -1 if the algorithm failed to find any such x 
    """

    if verify:
        assert is_prime(p), "Pollard-rho works for prime p"
    else:
        print("")
    
    # If no order is given, use order p-1.
    # g^(p-1) = 1 (mod p) for any prime p
    # However, the answer returned might not be the smallest one if the initial order was (p-1)
    if order == 0 or order is None:
        print()
        order = p-1

    # Handle special case
    if y == 1:
        return 0

    def __pollard_rho(g: int, y: int, p: int, order: int, a0: int, b0: int):

        # Start with x0 = g^a0 * y^b0
        x0 = (pow(g, a0, p) * pow(y, b0, p)) % p
        xi, ai, bi = x0, a0, b0
        x2i, a2i, b2i = x0, a0, b0

        # Perform p steps at random
        for i in range(1, p):
            # For 2i pointers, we need to take 2 steps
            xi, ai, bi = __compute_next(xi, g, y, ai, bi, p, order)
            x2i, a2i, b2i = __compute_next(x2i, g, y, a2i, b2i, p, order)
            x2i, a2i, b2i = __compute_next(x2i, g, y, a2i, b2i, p, order)

            # Collision
            if (xi == x2i):
                beta = (b2i - bi) % order
                alpha = (ai - a2i) % order

                # Algorithm failed
                if beta == 0:
                    return -1

                # We need to solve beta * x = alpha (mod order)
                xs = solve_linear_congurence(beta, alpha, order)
                for x in xs:
                    if pow(g, x, p) == y:
                        return x

        # Algorithm failed
        return -1

    # In the first attempt start with a0 = 0 and b0 = 0
    a0, b0 = 0, 0
    x = __pollard_rho(g, y, p, order, a0, b0)
    # return If the algorithm was able to find x (in which case x >=0)
    if x >= 0:
        return x

    # If the algorithm finds the solution, return
    for _ in range(tries):
        a0, b0 = random.randint(1, order), random.randint(1, order)
        x = __pollard_rho(g, y, p, order, a0, b0)
        if x >= 0:
            return x
    
    # Failed to solve, x would be negative
    return x