# https://asecuritysite.com/encryption/blum

import sympy
import random
import sys

x = 3 * 10 ** 10
y = 4 * 10 ** 10
seed = random.randint(1, 10 ** 10)


def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b // gcd(a, b)  # Use // for integer division


def gcd(c, d):
    """Compute the greatest common divisor of a and b"""
    while d > 0:
        c, d = d, c % d
    return c


def next_usable_prime(r):
    t = sympy.nextprime(r)
    while t % 4 != 3:
        t = sympy.nextprime(t)
    return t


p = next_usable_prime(x)
q = next_usable_prime(y)
M = p * q

N = 1000

if len(sys.argv) > 1:
    try:
        N = int(sys.argv[1])
    except ValueError:
        print("Invalid input for N. Please provide a valid integer.")

print("\np:\t", p)
print("q:\t", q)
print("M:\t", M)
print("Seed:\t", seed)

x = seed

bit_output = ""
for _ in range(N):
    x = x * x % M
    y = x % 2
    bit_output += str(y)
print(bit_output)

print("\nNumber of zeros:\t", bit_output.count("0"))
print("Number of ones:\t\t", bit_output.count("1"))

xi = ''

print("\nPredicting 1st 13 with Euler's Theorem:")
for i in range(1, 30):
    val = pow(2, int(i), int(lcm(p - 1, p - 1)))
    xi += str(pow(int(seed), int(val), int(M)) % 2)
print(xi)
