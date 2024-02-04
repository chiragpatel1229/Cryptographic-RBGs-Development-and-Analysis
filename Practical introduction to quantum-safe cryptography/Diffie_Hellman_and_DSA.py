# import necessary library modules
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh, dsa
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization

# Generate DH parameters
parameters = dh.generate_parameters(generator=2, key_size=2048)

# Generate Alice's DH private key and public key
alice_dh_private_key = parameters.generate_private_key()
alice_dh_public_key = alice_dh_private_key.public_key()

# Generate Bob's DH private key and public key
bob_dh_private_key = parameters.generate_private_key()
bob_dh_public_key = bob_dh_private_key.public_key()

print("Public and private keys generated for Bob and Alice")

# ======================================================================================================================

# Generate DSA keys for Alice and Bob
alice_dsa_private_key = dsa.generate_private_key(key_size=2048)
alice_dsa_public_key = alice_dsa_private_key.public_key()
bob_dsa_private_key = dsa.generate_private_key(key_size=2048)
bob_dsa_public_key = bob_dsa_private_key.public_key()

print("Additional key pair generated for signing")

# ======================================================================================================================

# Alice signs
alice_public_bytes = alice_dh_public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                      format=serialization.PublicFormat.SubjectPublicKeyInfo)
alice_signature = alice_dsa_private_key.sign(alice_public_bytes, hashes.SHA256())

print("Alice signed public key")

# ======================================================================================================================

# Similarly, Bob signs his DH public key using his DSA private key.
bob_public_bytes = bob_dh_public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                  format=serialization.PublicFormat.SubjectPublicKeyInfo)
bob_signature = bob_dsa_private_key.sign(bob_public_bytes, hashes.SHA256())

print("Bob signed public key")

# ======================================================================================================================

# Alice and Bob verify each other's DH public keys using DSA public keys
# An InvalidSignature exception will occur if they are not valid
alice_dsa_public_key.verify(alice_signature, alice_public_bytes, hashes.SHA256())
bob_dsa_public_key.verify(bob_signature, bob_public_bytes, hashes.SHA256())

print("Signatures are valid")

# ======================================================================================================================

# Perform key exchange
alice_shared_key = alice_dh_private_key.exchange(bob_dh_public_key)
bob_shared_key = bob_dh_private_key.exchange(alice_dh_public_key)

print("Shared secrets generated")

# ======================================================================================================================


# Derive a shared symmetric key using key-stretching
def derive_key(shared_key):
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=None,
    ).derive(shared_key)


alice_symmetric_key = derive_key(alice_shared_key)
bob_symmetric_key = derive_key(bob_shared_key)

assert alice_symmetric_key == bob_symmetric_key
print("Keys checked to be the same")
