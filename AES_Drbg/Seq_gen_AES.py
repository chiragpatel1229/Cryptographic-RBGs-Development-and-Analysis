import os
import secrets
import aes_drbg


# =================================================================================================================
my_generator = aes_drbg.AES_DRBG(256)  # Create an instance of the AES_DRBG class with a key length of 256 bits


# =================================================================================================================
entropy_in = os.urandom(48)                     # Obtain an entropy source that can provide at least 48 bytes of random bytes


per_string = b"\x00" * 43                       # Provide a personalization string that is unique to your application and 48 bytes long


my_generator.instantiate(entropy_in,
                         per_string)  # Call the instantiate method with the entropy input and the personalization string


random_bytes = my_generator.generate(32)        # Call the generate method with the number of bytes you want to generate


print(random_bytes.hex())                       # Print the random binary sequence in hexadecimal format


# =================================================================================================================

add_in = secrets.token_bytes(48)                # Provide an additional input that is 48 bytes long


random_bytes = my_generator.generate(32, add_in)    # Call the generate method again with the number of bytes and the additional input


print(random_bytes.hex())                       # Print the random binary sequence in hexadecimal format


# =================================================================================================================
entropy_in = os.urandom(48)                     # Obtain a new entropy source that can provide at least 48 bytes of random bytes


my_generator.reseed(entropy_in, add_in)         # Call the reseed method with the new entropy input and the additional input
