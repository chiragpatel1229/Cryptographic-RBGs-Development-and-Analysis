from random import randint

# parameter generation: select the primes q, p and generator g:
# EXPERIMENT with the values, they must meet certain rules
# this example code does not verify p,q are prime

q = 11
p = 23
g = 4

assert ((p - 1) % q == 0)
assert (g >= 2)
assert (g <= (p - 2))
assert ((pow(g, (p - 1) / q) % p) != 1)

print(f"Public information is good: q={p}, p={q}, g={g}")

# ======================================================================================================================

# Alice chooses an integer randomly from {2..q-1}
# EXPERIMENT with the values

alice_private_key = randint(2, q - 1)

assert (alice_private_key >= 2)
assert (alice_private_key <= (q - 1))

print(f"Alice's private key is {alice_private_key}")

# ======================================================================================================================

alice_public_key = pow(g, alice_private_key, p)
# Alternatively can use (g ** alice_private_key) % p

print(f"Alice's public key is {alice_public_key}")

# ======================================================================================================================

hash_dict = {}


def mock_hash_func(inp):
    print(inp)
    if inp not in hash_dict:
        hash_dict[inp] = randint(1, q)
    return hash_dict[inp]


alice_message = "Inspection tomorrow!"
alice_hash = mock_hash_func(alice_message)  # In reality, you'd use a hash function
print(f"Alice's message hash is: {alice_hash}")


# ======================================================================================================================

# brute-force implementation to find modular inverse
def modular_inverse(k1, q1):
    for i in range(0, q1):
        if (k1 * i) % q1 == 1:
            return i
    print(f'error! no inverse found! for {k1},{q1}')
    return 0


# Let's compare this algorithm with the standard python 'pow' function

n1 = modular_inverse(3, 7)
n2 = modular_inverse(4, 11)
n3 = modular_inverse(7, 5)
m1 = pow(3, -1, 7)
m2 = pow(4, -1, 11)
m3 = pow(7, -1, 5)

assert (n1 == m1)
assert (n2 == m2)
# assert(n3==m3)

print(f"modular_inverse(3,7) = {m1}")
print(f"modular_inverse(4,11) = {m2}")
print(f"modular_inverse(7,5) = {m3}")

# Some numbers don't have modular inverses - our function throws an error
n4 = modular_inverse(2, 6)

# The python library will throw an exception, which must be caught
try:
    m4 = pow(2, -1, 6)
except ValueError:
    print("Exception from pow() - no modular inverse found!")

# ======================================================================================================================

signed = False
r = 0
s = 0
while not signed:
    k = randint(1, q - 1)  # Should be different for every message
    print("Using random k =", k)
    r = pow(g, k, p) % q
    if r == 0:
        print(f"{k} is not a good random value to use to calculate r. Trying another k")
        continue
    # must restart algorithm if we get a 0 value for s (see above)
    s = (pow(k, -1, q) * (alice_hash + alice_private_key * r)) % q
    if s == 0:
        print(f"{k} is not a good random value to use to calculate s. Trying another k")
        continue
    signed = True

signature = (r, s)
print(f"Alice's signature is : {(r, s)}")

# ======================================================================================================================

# Bob re-generates message hash using Alice's broadcast message
bob_hash = mock_hash_func(alice_message)

# Bob computes auxiliary quantities w (using modular inverse), u1, u2 and v
w = (pow(s, -1, q)) % q
u1 = (bob_hash * w) % q
u2 = (r * w) % q
v = ((g ** u1 * alice_public_key ** u2) % p) % q

if v == r:
    print("Signature is valid!")
else:
    print("Signature is invalid!")
