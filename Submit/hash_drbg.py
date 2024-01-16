import hashlib
import os
import secrets

"""The security strength is the entropy that is required to initiate and reseed the DRBG. For HASH and HMAC the output
length is equal to the security strength per request, if more bits then the loop has to iterate further until the 
reseed counter limit is reached then the DRBG has to be reseeded again."""

# References: The HASH-DRBG mechanism based on NIST SP800-90A Publication
# Please consider all the Input parameters in bytes...

# This file generates only one sequence per execution so the reseed is not required, while generating more than one sequences and the
# reseed counter reach the max interval leval the drbg need to be reseeded using the reseed function with new entropy and data

# 0.0 =========== User Inputs ==========================================================================================

security_strength = 112                              # The strength should be = (112, 128, 192, 256)

output_bytes = 32                                    # input will be in bytes, it should be less than 7500


# 1.0 =========== Convert The Data Types to Store ======================================================================

def b2i(data):                                              # convert bytes to a list of integers
    binary_string = ''                                      # Convert each byte to a binary string and join them
    for byte in data:
        binary_string += bin(byte)[2:].zfill(8)             # convert each byte to binary of 8 characters and append
    # integer_list = [int(bit) for bit in binary_string]      # Convert the binary string to a list of integers
    return binary_string


# 2.0 =========== Hash DRBG class ======================================================================================

class Hash_DRBG:
    def __init__(self, selected_strength: int = 256):    # data = personalized byte string

        # Internal state variables  ====================================================================================
        self.V = None
        self.C = None
        self.reseed_counter = None

        # Check requested security strength ============================================================================
        if selected_strength > 256:
            raise RuntimeError("requested_security_strength cannot exceed 256 bits.")

        # consider the security strength based on requested value check Table 1 on Page - 14 ===========================
        if selected_strength <= 112:
            self.security_strength = 112
        elif selected_strength <= 128:
            self.security_strength = 128
        elif selected_strength <= 192:
            self.security_strength = 192
        else:
            self.security_strength = 256

        # Internal state variables  ====================================================================================

        entropy = os.urandom(self.security_strength // 8 + 3)   # (security strength * 1.5) < init_entropy < (125 bytes)
        data = secrets.token_bytes(30)                      # (security_strength bits) < nonce < (256 bits / 32 bytes)

        # Modified from Section 10.1.1, which specified 440 bits here ==================================================
        if len(data) * 8 > 256:
            raise RuntimeError("personalization_string cannot exceed 256 bits.")

        # Check the length of the entropy input ========================================================================
        if (len(entropy) * 8) < self.security_strength:     # The length should be at least equal to the security strength
            raise RuntimeError(f"entropy must be at least {self.security_strength} bits.")
        if len(entropy) * 8 > 1000:                         # The length should not exceed 1000 bits
            raise RuntimeError("entropy cannot exceed 1000 bits.")

        # Generate a random nonce of the required length ===============================================================
        nonce_length = self.security_strength // 2 // 8     # The length should be equal to half the security strength
        nonce_length = min(nonce_length, 256 // 8)          # The length should not exceed 256 bits
        nonce = os.urandom(nonce_length)

        # Check the length of the seed is the concatenation of the entropy input and the nonce =========================
        seed = entropy + nonce
        if (len(seed) * 8) < (self.security_strength * 3 // 2):     # The length should be at least 1.5 times the security strength
            raise RuntimeError(f"seed must be at least {1.5 * self.security_strength} bits.")

        self.instantiate(seed, data)  # Prepare the basic seed and the string for the function

# 2.1 ==================================================================================================================

    @staticmethod                                           # Simple wrapper for SHA-256 hash function
    def hash(data: bytes) -> bytes:                        # Updating and manipulating the internal state
        return hashlib.sha256(data).digest()                # return Hash Digest as a bytes object

# 2.2 ==================================================================================================================

    def update(self, provided_data: bytes = None):         # Update internal state of V and C based on provided data
        if provided_data is None:
            provided_data = b"\x00" * (self.security_strength // 8)
        temp = self.hash(self.V + b"\x01" + provided_data)
        self.V = self.hash(self.V + b"\x02" + provided_data + temp)  # updating the internal state of V
        self.C = self.hash(self.V + b"\x03" + provided_data + temp)  # updating the internal state of C

        '''b"\x01", b"\x02", and b"\x03" are used to indicate different cases, to separate the V and the provided_data.
        This ensures that the function produces different outputs for different inputs and cases. -> 10.3.1 and Appendix B'''

# 2.3 ==================================================================================================================

    def instantiate(self, seed: bytes, personalization_string: bytes):
        # B.1.7
        seed_material = seed + personalization_string
        # B.1.8 and 9
        self.V = self.hash(seed_material + b"\x00")
        # B.1.10
        self.C = self.hash(self.V + b"\x01")
        # B.1.11
        self.reseed_counter = 1

# 2.4 ==================================================================================================================

    def reseed(self, entropy: bytes, additional_input: bytes = b""):

        # B.1.2.3
        if (len(entropy) * 8) < self.security_strength:
            raise RuntimeError(f"entropy must be at least {self.security_strength} bits.")
        # B.1.2.4
        if len(entropy) * 8 > 1000:
            raise RuntimeError("entropy cannot exceed 1000 bits.")

        # B.1.2.6 to 10, Sum up the entropy and the additional input
        self.update(entropy + additional_input)
        # B.1.2.10
        self.reseed_counter = 1

# 2.5 ==================================================================================================================

    def generate(self, num_bytes: int):
        # B.1.3.1
        if (num_bytes * 8) > 7500:
            raise RuntimeError("It is not possible to generate more than 7500 bits in a single call.")

        # B.1.3.6
        if self.reseed_counter >= 10000:
            raise RuntimeError("Reseed required for further bit generation")

        temp = b""

        # B.1.3.11
        while len(temp) < num_bytes:
            self.V = self.hash(self.V)
            temp += self.V

        # B.1.3.13 and 14 and 16
        self.update()

        # B.1.3.15
        self.reseed_counter += 1

        return temp[:num_bytes]


# 3.0 =========== Call the class and its functions, required input data is =============================================
# =============== being generated inside the function so the user does not need to add it manually =====================

drbg = Hash_DRBG(security_strength)
random_seq = drbg.generate(output_bytes)
print(b2i(random_seq), "\n", "Total number of Bits:", len(b2i(random_seq)))
