def brute(g, y, n):
    """
    Brute Force to solve Discrete Log Problem
    :param g: g of g^x = y (mod n). g > 0.
    :param y: y of g^x = y (mod n). Non-negative integer.
    :param n: n of g^x = y (mod n). n > 1.
    :returns: x of g^x = y (mod n). If not found returns -1.
    """
    # Examine each g^i iteratively to determine if any are matches.
    # Start with i = 0
    g_raise_to_i = 1
    for i in range(0, n-1):
        # If matched we have found x
        if g_raise_to_i == y:
            return i
        g_raise_to_i = (g_raise_to_i * g) % n
    return -1