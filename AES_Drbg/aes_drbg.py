import pyaes


# References: The AES-DRBG mechanism based on NIST SP800-90A Publication
# Please consider all the Input parameters in bytes...

# Page: 48 - 10.2.1 : for AES, the output block lengths are 128 bits. The same block cipher algorithm and key length shall be used
# for all block cipher operations of this DRBG. The block cipher algorithm and key length shall meet or exceed the
# security requirements of the consuming application.


# 2.0 =========== Convert The Data Types for convenience ===============================================================

def strings_xor(a, b):                                  # XOR two byte strings a and b
    x_str = bytes(x ^ y for x, y in zip(a, b))
    return x_str


def bytes_padding(a, n):                                # Pad or extend a byte string with n byte zeros
    padded_bytes = a + b'\x00' * (n - len(a))           # example: extend the Byte String: b'\x01\x02\x03\x00\x00\x00\x00\x00'
    return padded_bytes


def bytes2long_int(a):                                  # Convert a byte string to a long integer
    long_int = int.from_bytes(a, 'big')                 # example: b'\x01\x02\x03\x04' = 16909060
    return long_int


def long_int2bytes(a):                                  # Convert a long integer to a byte string
    l2bytes = a.to_bytes((a.bit_length() + 7) // 8, 'big')     # example: 16909060 = b'\x01\x02\x03\x04'
    return l2bytes


# 0.0 ==================================================================================================================

class AES_DRBG(object):

    # 0.0 ==============================================================================================================

    def __init__(self, security_strength):

        # 0.0 ===== Initialize the important variables in this algorithm ===============================================
        self.reseed_counter = 0

        self.aes = None
        self.key = None
        self.ctr = None

        # 0.0 ==========================================================================================================
        self.out_length = 16                            # Set the output block length to 16 bytes (128 bits)

        # Set the reseed interval max limit to 2^48, that will be same for all key lengths,
        self.reseed_interval = 2 ** 48                  # Refer the Table: 3 on Page - 49

        # 0.0 ==========================================================================================================
        # Seed Length = output length + Key length (Key length = security strength)
        if security_strength == 256:
            self.seed_length = 48                       # key length + output length = 32 + 16 = 48 bytes
            self.key_length = 32                        #

        elif security_strength == 192:
            self.seed_length = 40                       # key length + output length = 24 + 16 = 40 bytes
            self.key_length = 24

        elif security_strength == 128:
            self.seed_length = 32                       # key length + output length = 16 + 16 = 32 bytes
            self.key_length = 16

        else:
            raise ValueError("Keylen is not possible to support for the AES-DRBG Algorithm.")

    # 0.0 ==============================================================================================================

    def instantiate(self, entropy_in, personalization_string=b''):

        # Check if the entropy input is the same length as the seed length
        if len(entropy_in) != self.seed_length:
            raise ValueError("Length of entropy input must be equal to seedlen")

        # Check if the personalization string is provided
        if len(personalization_string) != 0:

            # Get the length of the personalization string in bytes
            temp = len(personalization_string)

            # If the personalization string is shorter than the seed length, pad it with zeros
            if temp < self.seed_length:

                personalization_string = bytes_padding(personalization_string, self.seed_length)

            # If the personalization string is longer than the seed length, raise an error
            else:

                raise ValueError("Length of personalization string must be equal or less than seedlen")

        # If the personalization string is not provided or empty, set it to a string of zeros
        else:
            cjp = b"Chirag Patel"
            personalization_string = bytes_padding(cjp, self.seed_length)

        # Get the seed material by XORing the entropy input and the personalization string
        seed_material = strings_xor(entropy_in, personalization_string)

        # Split the seed material into two parts: the first part is the key, and the second part is the initial value of the counter
        self.key = seed_material[0:self.key_length]

        s_m = bytes2long_int(seed_material[-self.out_length:])
        self.ctr = pyaes.Counter(initial_value=s_m)

        # Create the AES object using the key and the counter, and set the mode of operation to CTR
        self.aes = pyaes.AESModeOfOperationCTR(self.key, counter=self.ctr)

        # Set the reseed counter to one
        self.reseed_counter = 1

    # 0.0 ==============================================================================================================

    def _update(self, provided_data):

        # Initialize a temporary byte string to store the key stream
        temp = b""

        # Loop until the temporary byte string is long enough to match the seed length
        while len(temp) < self.seed_length:
            # Encrypt a string of zeros with the current key and counter, and get an output block of 128 bits
            output_block = self.aes.encrypt(bytes_padding(b"\x00", self.out_length))
            # Concatenate the output block to the temporary byte string
            temp = temp + output_block

        # Truncate the temporary byte string to the seed length
        temp = temp[0:self.seed_length]

        # Check if the provided data is empty
        if provided_data:
            # If the provided data is not empty, XOR it with the key stream
            temp = strings_xor(temp, provided_data)

        # Split the result into two parts: the first part is the new key, and the second part is the new value of the counter
        self.key = temp[0:self.key_length]

        s_m_2 = bytes2long_int(temp[-self.out_length:])
        self.ctr = pyaes.Counter(initial_value=s_m_2)

        # Update the AES object with the new key and the new counter
        self.aes = pyaes.AESModeOfOperationCTR(self.key, counter=self.ctr)

    # 0.0 ==============================================================================================================

    def reseed(self, entropy_in, add_in=b''):

        # Check if the reseed counter has exceeded the reseed interval, and raise a warning if it has
        if self.reseed_counter > self.reseed_interval:
            raise Warning("the DRBG should be reseeded !!!")

        # Check if the entropy input is the same length as the seed length
        if len(entropy_in) != self.seed_length:
            raise ValueError("Length of entropy input must be equal to seedlen")

        # Check if the additional input is provided
        if len(add_in) != 0:

            # Check if the additional input is the same length as the seed length
            if len(add_in) != self.seed_length:
                raise ValueError("Length of additional input must be equal to seedlen")

        # If the additional input is not provided or empty, set it to a string of zeros
        else:

            add_in = bytes_padding(b"\x00", self.seed_length)

        # Get the seed material by XORing the entropy input and the additional input
        seed_material = strings_xor(entropy_in, add_in)

        # Call the _update method with the seed material as an argument, and update the key and the counter
        self._update(seed_material)

        # Set the reseed counter to one
        self.reseed_counter = 1

    # 0.0 ==============================================================================================================

    def generate(self, req_bytes, add_in=b''):

        # Check if the reseed counter has exceeded the reseed interval, and raise a warning if it has
        if self.reseed_counter > self.reseed_interval:
            raise Warning("the DRBG should be reseeded !!!")

        # Check if the additional input is provided
        if len(add_in) != 0:

            # Check if the additional input is the same length as the seed length
            if len(add_in) != self.seed_length:
                raise ValueError("Length of additional input must be equal to seedlen")

            # Call the _update method with the additional input as an argument, and update the key and the counter
            self._update(add_in)

        # Initialize a temporary byte string to store the random binary sequence
        temp = b''

        # Loop until the temporary byte string is long enough to satisfy the requested number of bytes
        while len(temp) < req_bytes:
            # Encrypt a string of zeros with the current key and counter, and get an output block of 128 bits
            output_block = self.aes.encrypt(bytes_padding(b"\x00", self.out_length))
            # Concatenate the output block to the temporary byte string
            temp = temp + output_block
            # Increment the counter by one, and wrap around to zero when it reaches its maximum value
            self.ctr.increment()

        # Return the requested number of bytes from the temporary byte string
        returned_bytes = temp[0:req_bytes]

        # Call the _update method with the additional input as an argument, and update the key and the counter again
        self._update(add_in)

        # Increment the reseed counter by one
        self.reseed_counter = self.reseed_counter + 1

        # Return the random binary sequence
        return returned_bytes
