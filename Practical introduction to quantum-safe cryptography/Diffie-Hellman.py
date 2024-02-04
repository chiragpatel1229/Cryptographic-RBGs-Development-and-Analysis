# Step 1: Choose a prime `p` and a primitive root `a`
p = 11
a = 7

print(f"prime: {p}")
print(f"primitive root: {a}")

k_A = 4  # A lice's private key
h_A = (a ** k_A) % p  # Alice's public key

print(f"Alice's private key is {k_A} and public key is {h_A}")

k_B = 8  # Bob's private key
h_B = (a ** k_B) % p  # Bob's public key

print(f"Bob's private key is {k_B} and public key is {h_B}")

secret_key_alice  = h_B**k_A % p
secret_key_bob = h_A**k_B % p
assert secret_key_alice == secret_key_bob
print(f'The shared secret key is: {secret_key_bob}')






