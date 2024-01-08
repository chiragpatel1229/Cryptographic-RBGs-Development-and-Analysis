import hashlib
import hmac
import os
import secrets

"""The security strength is the entropy that is required to initiate and reseed the DRBG. For HASH and HMAC the output
length is equal to the security strength per request, if more bits then the loop has to iterate further until the 
reseed counter limit is reached then the DRBG has to be reseeded again."""

# References: The HASH-DRBG mechanism based on NIST SP800-90A Publication
# Please consider all the Input parameters in bytes...

# 0.0 =========== User Inputs ==========================================================================================

security_strength = 256                              # The strength should be = (112, 128, 192, 256)
init_entropy = os.urandom(48)                        # (security strength * 1.5) < init_entropy < (125 bytes)
personalization_str = os.urandom(32)                 # (security_strength bits) < nonce < (256 bits / 32 bytes)

reseed_entropy = secrets.token_bytes(32)             # (security strength) < init_entropy < ( < 125 bytes)

output_bytes = 32                                    # input will be in bytes, it should be less than 7500

# 1.0 =========== Convert The Data Types to Store ======================================================================


def b2i(data):                                              # convert bytes to a list of integers
    binary_string = ''                                      # Convert each byte to a binary string and join them
    for byte in data:
        binary_string += bin(byte)[2:].zfill(8)             # convert each byte to binary of 8 characters and append
    integer_list = [int(bit) for bit in binary_string]      # Convert the binary string to a list of integers
    return integer_list


# 1.0 =========== The HMAC DRBG class ==================================================================================

class HMAC_DRBG:
    def __init__(self, entropy: bytes, requested_security_strength: int = 256, personalization_string: bytes = b""):

        # Internal state variables  ====================================================================================
        self.V = None
        self.reseed_counter = None

        # Check requested security strength ============================================================================
        if requested_security_strength > 256:
            raise RuntimeError("requested_security_strength cannot exceed 256 bits.")

        # Modified from Section 10.1.1, which specified 440 bits here ==================================================
        if len(personalization_string) * 8 > 256:
            raise RuntimeError("personalization_string cannot exceed 256 bits.")

        # consider the security strength based on requested value check Table 1 on Page - 14 ===========================
        if requested_security_strength <= 112:
            self.security_strength = 112
        elif requested_security_strength <= 128:
            self.security_strength = 128
        elif requested_security_strength <= 192:
            self.security_strength = 192
        else:
            self.security_strength = 256

        # Check the length of the entropy input ========================================================================
        if (len(entropy) * 8 * 2) < (3 * self.security_strength):       # The length should be at least equal to the security strength
            raise RuntimeError(f"entropy must be at least {1.5 * self.security_strength} bits.")

        if len(entropy) * 8 > 1000:                                     # The length should not exceed 1000 bits
            raise RuntimeError("entropy cannot exceed 1000 bits.")

        self._instantiate(entropy, personalization_string)              # Initialize the internal state

# ======================================================================================================================

    @staticmethod                 # to Generate a 'message authentication code' (MAC) for the input and secret key
    def _hmac(key: bytes, data: bytes) -> bytes:
        return hmac.new(key, data, hashlib.sha256).digest()

# ======================================================================================================================

    def _update(self, provided_data: bytes = None):     # Update the key and internal values using HMAC-SHA256
        self.K = self._hmac(self.K, self.V + b"\x00" + (b"" if provided_data is None else provided_data))
        self.V = self._hmac(self.K, self.V)

        if provided_data is not None:                   # Additional update steps if provided_data is not None
            self.K = self._hmac(self.K, self.V + b"\x01" + provided_data)
            self.V = self._hmac(self.K, self.V)

# ======================================================================================================================

    def _instantiate(self, entropy: bytes, personalization_string: bytes):
        seed_material = entropy + personalization_string    # prepare the seed material for the update function

        # Initialize key and internal values ===========================================================================
        self.K = b"\x00" * 32
        self.V = b"\x01" * 32

        # Initial update of the internal state =========================================================================
        self._update(seed_material)
        self.reseed_counter = 1

# ======================================================================================================================

    def reseed(self, entropy: bytes):       # Reseed the generator with additional entropy

        # Check entropy length as per the requirements =================================================================
        if (len(entropy) * 8) < self.security_strength:
            raise RuntimeError(f"entropy must be at least {self.security_strength} bits.")

        if len(entropy) * 8 > 1000:
            raise RuntimeError("entropy cannot exceed 1000 bits.")

        # Update the internal state with additional entropy ============================================================
        self._update(entropy)
        self.reseed_counter = 1

# ======================================================================================================================

    def generate(self, num_bytes: int, requested_security_strength: int = 256):

        # Check limits of on the number of requested bits ==============================================================
        if (num_bytes * 8) > 7500:
            raise RuntimeError("It is not possible to generate more than 7500 bits in a single call.")

        # Check requested security strength  ===========================================================================
        if requested_security_strength > self.security_strength:
            raise RuntimeError(f"requested_security_strength exceeds this instance's security_strength ({self.security_strength})")

        if self.reseed_counter >= 10000:        # Check reseed counter
            return None

        temp = b""

        while len(temp) < num_bytes:
            self.V = self._hmac(self.K, self.V)  # update internal value with every iteration and generate random bytes
            temp += self.V

        self._update()
        self.reseed_counter += 1                # Final update and increment reseed counter

        return temp[:num_bytes]                 # Return only requested bytes


drbg = HMAC_DRBG(entropy=init_entropy, requested_security_strength=security_strength, personalization_string=personalization_str)
drbg.reseed(reseed_entropy)
random_seq = drbg.generate(num_bytes=output_bytes, requested_security_strength=security_strength)
print(b2i(random_seq), "\n", "Total number of Bits:", len(b2i(random_seq)))
