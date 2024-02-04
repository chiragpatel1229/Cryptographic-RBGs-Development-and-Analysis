# https://learning.quantum.ibm.com/course/practical-introduction-to-quantum-safe-cryptography/quantum-safe-cryptography

import numpy as np
from matplotlib import pyplot as plt

n = 8
q = 127
N = int(1.1 * n * np.log(q))
sigma = 1.0
print(f"n={n}, q={q}, N={N}, sigma={sigma}")


# ======================================================================================================================

def chi(st_dev, modulus):
    return round((np.random.randn() * st_dev ** 2)) % modulus


# print some examples
sd = 2
m = 1000
for x in range(10):
    print("chi = ", chi(sd, m))

# ======================================================================================================================

# Alice needs to generate her key pair.
# Alice's private key
alice_private_key = np.random.randint(0, high=q, size=n)
print(f"Alice's private key: {alice_private_key}")

# ======================================================================================================================

# Alice now sets up her public key, by choosing random vectors, which are then combined with the generated errors.
# Alice's Public Key
alice_public_key = []

# N is the number of values we want in the key
for i in range(N):
    # Get n random values between 0 and <q
    a = np.random.randint(0, high=q, size=n)
    # get an error to introduce
    epsilon = chi(sigma, q)
    #  calculate dot product (ie like array multiplication)
    b = (np.dot(a, alice_private_key) + epsilon) % q
    # value to be added to the key -
    sample = (a, b)
    alice_public_key.append(sample)

# print(f"Alice's public key: {alice_public_key}")
print(f"Alice's public key is generated!")
# ======================================================================================================================

# Alice can now share her public key.
# Bob can now use this to send Alice an encrypted message.
# Bob's message is a single bit.

# Encryption
bob_message_bit = 1
print(f"Bob's message bit={bob_message_bit}")

# ======================================================================================================================

# To encrypt the message, Bob needs to select an arbitrary number of samples at random from Alice's public key to form the ciphertext.
# For this, he creates a mask, a random binary vector r of length N.

# a list of N values between 0 and <2 - ie 0 or 1
r = np.random.randint(0, 2, N)
print(r)

# ======================================================================================================================

# We now take this mask and apply it to the relevant entry in Alice's public key, calculating a sum of the values found.
sum_ai = np.zeros(n, dtype=int)
sum_bi = 0

for i in range(N):
    sum_ai = sum_ai + r[i] * alice_public_key[i][0]
    sum_bi = sum_bi + r[i] * alice_public_key[i][1]
sum_ai = [x % q for x in sum_ai]
# sum_bi = sum_bi
ciphertext = (sum_ai, (bob_message_bit * int(np.floor(q / 2)) + sum_bi) % q)
print(f"ciphertext is: {ciphertext}")
# ======================================================================================================================

# Finally, Bob broadcasts the ciphertext, which Alice can decrypt using her private key.
# Decryption
adots = np.dot(ciphertext[0], alice_private_key) % q
b_adots = (ciphertext[1] - adots) % q

decrypted_message_bit = round((2*b_adots)/q) % 2

print(f"original message bit={bob_message_bit}, decrypted message bit={decrypted_message_bit}")

assert bob_message_bit == decrypted_message_bit

# ======================================================================================================================

# Since this protocol works bit by bit for encrypting longer bit strings, we simply repeat the operations in a loop.
# The following shows a scenario where Bob wishes to transfer 16 encrypted bits.

bob_message_bits = np.random.randint(0, 2, 16)
print(f"Bob's message bits are : {bob_message_bits}")
decrypted_bits = []

for ib in range(len(bob_message_bits)):
    bob_message_bit = bob_message_bits[ib]

    r = np.random.randint(0, 2, N)

    sum_ai = np.zeros(n, dtype=int)
    sum_bi = 0
    for i in range(N):
        sum_ai = sum_ai + r[i] * alice_public_key[i][0]
        sum_bi = sum_bi + r[i] * alice_public_key[i][1]
    sum_ai = [x % q for x in sum_ai]

    ciphertext = (sum_ai, (bob_message_bit * int(np.floor(q / 2)) + sum_bi) % q)

    adots = np.dot(ciphertext[0], alice_private_key) % q
    b_adots = (ciphertext[1] - adots) % q

    decrypted_message_bit = round((2 * b_adots) / q) % 2
    assert decrypted_message_bit == bob_message_bit

    decrypted_bits.append(decrypted_message_bit)

print(f"Decrypted message bits = {np.array(decrypted_bits)}")

# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
