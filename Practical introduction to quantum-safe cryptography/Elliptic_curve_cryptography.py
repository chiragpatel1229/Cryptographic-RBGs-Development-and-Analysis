from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# ----------------Key exchange with ECC

# Each party generates a private key
private_key1 = ec.generate_private_key(ec.SECP384R1())
private_key2 = ec.generate_private_key(ec.SECP384R1())

# They exchange public keys
public_key1 = private_key1.public_key()
public_key2 = private_key2.public_key()

# Each party uses their own private key and the other party's public key
# to derive the shared secret
shared_key1 = private_key1.exchange(ec.ECDH(), public_key2)
shared_key2 = private_key2.exchange(ec.ECDH(), public_key1)

# The shared secrets are the same
assert shared_key1 == shared_key2
print("Keys checked to be the same")

# ======================================================================================================================

# -----------------Digital signatures with ECC

# Generate a private key for use in the signature
private_key = ec.generate_private_key(ec.SECP384R1())

message = b"A message to be signed"

# Sign the message
signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))

# Anyone can verify the signature with the public key
public_key = private_key.public_key()
try:
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    print("The signature is valid.")
except ValueError:
    print("The signature is invalid.")
# In the above code, if one modifies the message after it has been signed, the verification will fail,
# providing a guarantee of authenticity and integrity for the message

# ======================================================================================================================

