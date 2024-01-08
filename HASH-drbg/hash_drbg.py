import hashlib
import os

""" OKAY
Implements a Hash_DRBG from NIST SP 800-90A based on SHA-256.
Supports security strengths up to 256 bits.
Parameters are based on recommendations provided by Section 10.1.1 of NIST SP 800-90A.
Pseudocode is based on Appendix B of NIST SP 800-90A.
"""


class Hash_DRBG:
    def __init__(self, entropy: bytes, requested_security_strength: int = 256, personalization_string: bytes = b""):

        # Internal state variables  ====================================================================================
        self.V = None
        self.C = None
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

        self._instantiate(seed, personalization_string)     # Prepare the basic seed and the string for the function

# ======================================================================================================================

    @staticmethod                                           # Simple wrapper for SHA-256 hash function
    def _hash(data: bytes) -> bytes:                        # Updating and manipulating the internal state
        return hashlib.sha256(data).digest()                # return Hash Digest as a bytes object

# ======================================================================================================================

    def _update(self, provided_data: bytes = None):         # Update internal state of V and C based on provided data
        if provided_data is None:
            provided_data = b"\x00" * (self.security_strength // 8)
        temp = self._hash(self.V + b"\x01" + provided_data)
        self.V = self._hash(self.V + b"\x02" + provided_data + temp)     # updating the internal state of V
        self.C = self._hash(self.V + b"\x03" + provided_data + temp)     # updating the internal state of C

        '''b"\x01", b"\x02", and b"\x03" are used to indicate different cases, to separate the V and the provided_data.
        This ensures that the function produces different outputs for different inputs and cases. -> 10.3.1 and Appendix B'''

# ======================================================================================================================

    def _instantiate(self, seed: bytes, personalization_string: bytes):
        # B.1.7
        seed_material = seed + personalization_string
        # B.1.8 and 9
        self.V = self._hash(seed_material + b"\x00")
        # B.1.10
        self.C = self._hash(self.V + b"\x01")
        # B.1.11
        self.reseed_counter = 1

# ======================================================================================================================

    def reseed(self, entropy: bytes, additional_input: bytes = b""):

        # B.1.2.3
        if (len(entropy) * 8) < self.security_strength:
            raise RuntimeError(f"entropy must be at least {self.security_strength} bits.")
        # B.1.2.4
        if len(entropy) * 8 > 1000:
            raise RuntimeError("entropy cannot exceed 1000 bits.")

        # B.1.2.6 to 10, Sum up the entropy and the additional input
        self._update(entropy + additional_input)
        # B.1.2.10
        self.reseed_counter = 1

# ======================================================================================================================

    def generate(self, num_bytes: int):
        # B.1.3.1
        if (num_bytes * 8) > 7500:
            raise RuntimeError("generate cannot generate more than 7500 bits in a single call.")

        # B.1.3.6
        if self.reseed_counter >= 10000:
            return None

        temp = b""

        # B.1.3.11
        while len(temp) < num_bytes:
            self.V = self._hash(self.V)
            temp += self.V

        # B.1.3.13 and 14 and 16
        self._update()

        # B.1.3.15
        self.reseed_counter += 1

        return temp[:num_bytes]
