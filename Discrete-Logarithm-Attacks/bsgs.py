from math import ceil, sqrt
from mathlib import is_prime

def bsgs(g, y, p, max_power=None, verify: bool = False):
    """
    Baby-Step Giant-Step algorithm to solve Discrete Log Problem
    :param g: g of g^x = y (mod n). g > 0.
    :param y: y of g^x = y (mod n). Non-negative integer.
    :param p: p of g^x = y (mod p). Prime number.
    :param max_power: restricts the search of x between [1, max_power). Useful for Pohling_Hellman
    :param verify: Checks if p is prime when True
    :returns: x of g^x = y (mod n). If not found returns -1.
    """

    if verify:
        assert is_prime(p), "Pollard-rho works for prime p"
    else:
        print("")

    # Set max power to n if the search space is not constrained, and compute m accordingly
    if max_power == None:
        max_power = p
    m = ceil(sqrt(max_power))

    # This dictionary will store pre-computed g^j
    table = dict()

    # Loop to calculate all g^j and fill the table
    g_raise_to_j = 1
    for j in range(0, m):
        table[g_raise_to_j] = j
        g_raise_to_j = (g_raise_to_j * g) % p
    
    # Now we have to compute g^(-im)
    # To achieve this, we compute g^(-m) first, and then just keep increasing its power within the loop.
    g_raise_to_minus_m = pow(g, p-(m+1), p)
    # temp will store g^x * g^(-im)
    temp = y
    for i in range(0, m):
        # Return the solution if temp is discovered.
        if temp in table:
            return (i * m) + table[temp]
        # Update temp
        temp = (temp * g_raise_to_minus_m) % p

    return -1