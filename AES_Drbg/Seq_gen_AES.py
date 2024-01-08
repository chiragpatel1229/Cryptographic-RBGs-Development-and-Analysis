import os
import aes_drbg

# Create an instance of the AES_DRBG class with a key length of 256 bits
my_generator = aes_drbg.AES_DRBG(256)

# Obtain an entropy source that can provide at least 48 bytes of random bytes
entropy_in = os.urandom(48)

# Provide a personalization string that is unique to your application and 48 bytes long
per_string = b"\x00" * 43

# Call the instantiate method with the entropy input and the personalization string
my_generator.instantiate(entropy_in, per_string)

# Call the generate method with the number of bytes you want to generate
random_bytes = my_generator.generate(32)

# Print the random binary sequence in hexadecimal format
print(random_bytes.hex())

# Provide an additional input that is 48 bytes long
add_in = b"MoreEntropy" + b"\x00" * 38

# Call the generate method again with the number of bytes and the additional input
random_bytes = my_generator.generate(32, add_in)

# Print the random binary sequence in hexadecimal format
print(random_bytes.hex())

# Obtain a new entropy source that can provide at least 48 bytes of random bytes
entropy_in = os.urandom(48)

# Call the reseed method with the new entropy input and the additional input
my_generator.reseed(entropy_in, add_in)
