import hashlib
import hmac
import os
import secrets

"""
The security strength is the entropy that is required to initiate and reseed the DRBG. For HASH and HMAC the output
length is equal to the security strength per request, if more bits then the loop has to iterate further until the 
reseed counter limit is reached then the DRBG has to be reseeded again.
"""

# References: The HMAC-DRBG mechanism based on NIST SP800-90A Publication
# Please consider all the Input parameters in bytes...

# This file generates only one sequence per execution the reseed is not required, while generating more than one sequences and the
# reseed counter reach the max interval leval the drbg need to be reseeded using the reseed function with new entropy and data
# Comments and the variable names are also referenced from the given NIST document


# 0.0 =========== User Inputs ==========================================================================================

security_strength = 112                              # The strength should be = (112, 128, 192, 256)

output_bytes = 4000 // 8                             # input will be in bytes, it should be less than 7500

# 1.0 =========== Convert The Data Types to Store ======================================================================


def b2i(data):                                              # convert bytes to a list of integers
    binary_string = ''                                      # Convert each byte to a binary string and join them
    for byte in data:
        binary_string += bin(byte)[2:].zfill(8)             # convert each byte to binary of 8 characters and append
    # integer_list = [int(bit) for bit in binary_string]      # Convert the binary string to a list of integers
    return binary_string


# 2.0 =========== The HMAC DRBG class ==================================================================================

class HMAC_DRBG:

    # 2.1 ==============================================================================================================

    def __init__(self, requested_security_strength: int = 256):

        # Internal state variables  ====================================================================================
        self.K = None
        self.V = None
        self.reseed_counter = None

        # Check requested security strength ============================================================================
        if requested_security_strength > 256:
            raise RuntimeError("requested_security_strength cannot exceed 256 bits.")

        # consider the security strength based on requested value check Table 1 on Page - 14 ===========================
        if requested_security_strength <= 112:
            self.security_strength = 112
        elif requested_security_strength <= 128:
            self.security_strength = 128
        elif requested_security_strength <= 192:
            self.security_strength = 192
        else:
            self.security_strength = 256

        # Internal state variables  ====================================================================================

        entropy = os.urandom(self.security_strength // 8 * 2)           # (security strength * 1.5) < init_entropy < (125 bytes)
        personalization_string = secrets.token_bytes(30)                # (security_strength bits) < nonce < (256 bits / 32 bytes)

        # Modified from Section 10.1.1, which specified 440 bits here ==================================================
        if len(personalization_string) * 8 > 256:
            raise RuntimeError("personalization_string cannot exceed 256 bits.")

        # Check the length of the entropy input ========================================================================
        if (len(entropy) * 8 * 2) < (3 * self.security_strength):       # The length should be at least equal to the security strength
            raise RuntimeError(f"entropy must be at least {self.security_strength * 3} bits.")

        if len(entropy) * 8 > 1000:                                     # The length should not exceed 1000 bits
            raise RuntimeError("entropy cannot exceed 1000 bits.")

        self.instantiate(entropy, personalization_string)  # Initialize the internal state

    # 2.2 ==============================================================================================================

    @staticmethod                 # to Generate a 'message authentication code' (MAC) for the input and secret key
    def hmac(key: bytes, data: bytes) -> bytes:
        return hmac.new(key, data, hashlib.sha256).digest()

    # 2.3 ==============================================================================================================

    def update(self, provided_data: bytes = None):     # Update the key and internal values using HMAC-SHA256
        self.K = self.hmac(self.K, self.V + b"\x00" + (b"" if provided_data is None else provided_data))
        self.V = self.hmac(self.K, self.V)

        if provided_data is not None:                  # Additional update steps if provided_data is not None
            self.K = self.hmac(self.K, self.V + b"\x01" + provided_data)
            self.V = self.hmac(self.K, self.V)

    # 2.3 ==============================================================================================================

    def instantiate(self, entropy: bytes, personalization_string: bytes):
        seed_material = entropy + personalization_string    # prepare the seed material for the update function

        # Initialize key and internal values ===========================================================================
        self.K = b"\x00" * 32
        self.V = b"\x01" * 32

        # Initial update of the internal state =========================================================================
        self.update(seed_material)
        self.reseed_counter = 1

    # 2.4 ==============================================================================================================

    def reseed(self):       # Reseed the generator with additional entropy

        entropy = os.urandom(self.security_strength // 8 + 3)      # (security strength * 1.5) < init_entropy < (125 bytes)

        # Check entropy length as per the requirements =================================================================
        if (len(entropy) * 8) < self.security_strength:
            raise RuntimeError(f"entropy must be at least {self.security_strength} bits.")

        if len(entropy) * 8 > 1000:
            raise RuntimeError("entropy cannot exceed 1000 bits.")

        # Update the internal state with additional entropy ============================================================
        self.update(entropy)
        self.reseed_counter = 1

    # 2.5 ==============================================================================================================

    def generate(self, num_bytes: int, requested_security_strength: int = 256):

        # Check limits of on the number of requested bits ==============================================================
        if (num_bytes * 8) > pow(2, 12):
            raise RuntimeError("It is not possible to generate more than 7500 bits in a single call.")

        # Check requested security strength  ===========================================================================
        if requested_security_strength > self.security_strength:
            raise RuntimeError(f"requested_security_strength exceeds this instance's security_strength ({self.security_strength})")

        if self.reseed_counter >= 10000:        # Check reseed counter
            return None

        temp = b""

        while len(temp) < num_bytes:
            self.V = self.hmac(self.K, self.V)  # update internal value with every iteration and generate random bytes
            temp += self.V

        self.update()
        self.reseed_counter += 1                # Final update and increment reseed counter

        return temp[:num_bytes]                 # Return only requested bytes


# 3.0 =========== Call the class and its functions, required input data is =============================================
# =============== being generated inside the function so the user does not need to add it manually =====================
drbg = HMAC_DRBG(requested_security_strength=security_strength)
drbg.reseed()
# random_seq = drbg.generate(num_bytes=output_bytes, requested_security_strength=security_strength)
# print(b2i(random_seq), "\n", "Total number of Bits:", len(b2i(random_seq)))

# Open a file to write
with open("hmac_drbg.txt", "w") as file:
    for _ in range(100):
        random_seq = drbg.generate(num_bytes=output_bytes, requested_security_strength=security_strength)
        file.write(b2i(random_seq) + '\n')

print("Random bits have been stored in random_bits.txt")

