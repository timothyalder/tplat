import math


def common_factors(x, y):
    common_divisor = math.gcd(x, y)
    common_factors = []
    for i in range(1, common_divisor + 1):
        if common_divisor % i == 0:
            common_factors.append(i)
    return common_factors
