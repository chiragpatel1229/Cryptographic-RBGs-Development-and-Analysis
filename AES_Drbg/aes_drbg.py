import pyaes


# References: The AES-DRBG mechanism based on NIST SP800-90A Publication
# Please consider all the Input parameters in bytes...

# Page: 48 - 10.2.1 : for AES, the output block lengths are 128 bits. The same block cipher algorithm and key length shall be used
# for all block cipher operations of this DRBG. The block cipher algorithm and key length shall meet or exceed the
# security requirements of the consuming application.


# 1.0 ===== Convert The Data Types for convenience =====================================================================

def strings_xor(a, b):                                  # XOR two byte strings a and b
    x_str = bytes(x ^ y for x, y in zip(a, b))
    return x_str


def bytes_padding(a, n):                                # Pad or extend a byte string with n byte zeros
    padded_bytes = a + b'\x00' * (n - len(a))           # example: extend the Byte String: b'\x01\x02\x03\x00\x00\x00\x00\x00'
    return padded_bytes


def bytes2long_int(a):                                  # Convert a byte string to a long integer
    long_int = int.from_bytes(a, 'big')                 # example: b'\x01\x02\x03\x04' = 16909060
    return long_int


# 2.0 ===== AES drbg algorithm based on the NIST recommendation ========================================================

class AES_DRBG(object):

    # 2.1 ===== Initialise and / or set all the important variable values ==============================================

    def __init__(self, security_strength):

        # 2.1.1 ===== Initialize the important variables in this algorithm =============================================
        self.reseed_counter = 0
        self.security_strength = security_strength

        self.aes = None
        self.key = None
        self.ctr = None

        # 2.1.2 ===== define the output length and the reseed interval value ===========================================
        self.out_length = 16                            # Set the output block length to 16 bytes (128 bits)

        #                                               Set the reseed interval max limit to 2^48, that will be same for all key lengths,
        self.reseed_interval = 2 ** 48                  # Refer the Table: 3 on Page - 49

        # 2.1.3 ===== define the seed and key length based on the security strength ====================================

        #                                               Seed Length = output length + Key length (Key length = security strength)
        if security_strength == 256:
            self.seed_length = 48                       # key length + output length = 32 + 16 = 48 bytes
            self.key_length  = 32                       # key length = 256 // 8 == 32 bytes

        elif security_strength == 192:
            self.seed_length = 40                       # key length + output length = 24 + 16 = 40 bytes
            self.key_length  = 24                       # key length = 192 // 8 == 24 bytes

        elif security_strength == 128:
            self.seed_length = 32                       # key length + output length = 16 + 16 = 32 bytes
            self.key_length  = 16                       # key length = 128 // 8 == 16 bytes

        else:
            raise ValueError(f"{security_strength} Keylen is not possible "
                             f"to support this AES-DRBG Algorithm !!!")

    # 2.2 ===== instantiate the AES object, key and counter ============================================================

    def instantiate(self, entropy_in, personalization_string=b''):

        # 2.2.1 ===== Verify the Entropy Input conditions ==============================================================

        if len(entropy_in) != self.seed_length:         # The input entropy and the seed length must be the same
            raise ValueError(f"Length of entropy input must be equal to "
                             f"seedlen: {self.seed_length} !!!")

        # 2.2.2 ===== Verify the personalization string conditions =====================================================

        if len(personalization_string) != 0:            # if the personalization string is provided enter into the condition

            temp = len(personalization_string)

            if temp < self.seed_length:                 # If string is shorter than the seed length, pad it with zeros

                personalization_string = bytes_padding(personalization_string, self.seed_length)

            else:                                       # if temp > self.seed_length, raise an error

                raise ValueError("Personalization string Length <= seed length !!!")

        else:                                           # Otherwise create one using bytes_padding function
            cjp = b"Chirag Patel"                       # select a random byte string to initiate
            personalization_string = bytes_padding(cjp, self.seed_length)

        # 2.2.3 ===== XOR the provided inputs to improve the entropy ===================================================

        seed_material = strings_xor(entropy_in, personalization_string)     # Prepare the seed material using the inputs

        # 2.2.4 ===== Prepare the Key, Counter and the AES object using the seed material ==============================

        self.key = seed_material[0:self.key_length]     # Split the seed material for the Key

        s_m = bytes2long_int(seed_material[-self.out_length:])   # Split the seed material for the Counter
        self.ctr = pyaes.Counter(initial_value=s_m)     # initiate the counter class from the pyaes library

        self.aes = pyaes.AESModeOfOperationCTR(self.key, counter=self.ctr)  # Create the AES object, and use the CTR mode

        self.reseed_counter = 1                         # Set the reseed counter to one

    # 2.3 ===== A function to update or refresh the key, counter and the object ========================================

    def update(self, provided_data):

        #  2.3.1 ===== generate a temporary string to refresh the internal variables ===================================

        temp = b""                                      # Initialize a buffer to store the key

        while len(temp) < self.seed_length:             # Loop until the temporary byte string == seed length

            output_block = self.aes.encrypt(
                bytes_padding(b"\x00", self.out_length), )  # Encrypt a string of zeros with the current key and counter
            temp = temp + output_block                  # Append output block to the temporary byte string

        temp = temp[0:self.seed_length]                 # Trim the temp string == seed length

        #  2.3.2 ===== XOR the provided input and temporary string to improve the entropy ===============================

        if provided_data:                               # if the provided data is available

            temp = strings_xor(temp, provided_data)     # If data is provided, XOR it with the temp key stream

        # 2.3.3 ===== Prepare the Key, Counter and the AES object using the seed material ================================

        self.key = temp[0:self.key_length]              # Split the seed material for the Key

        s_m_2 = bytes2long_int(temp[-self.out_length:])  # Split the seed material for the counter
        self.ctr = pyaes.Counter(initial_value=s_m_2)   # initiate the counter class from the pyaes library

        self.aes = pyaes.AESModeOfOperationCTR(self.key, counter=self.ctr)  # Create the AES object, and use the CTR mode

    # 2.4 ===== improve the entropy of the seed material and the Key and the counter ===================================

    def reseed(self, entropy_in, add_in=b''):

        # 2.4.1 ===== Verify the reseed interval conditions ============================================================

        if self.reseed_counter > self.reseed_interval:  # Check the counter for the reseed interval
            raise Warning("The DRBG Class is require to reseeded now !!!")

        # 2.4.2 ===== Verify the Entropy Input conditions ==============================================================

        if len(entropy_in) != self.seed_length:         # Check the provided entropy length == seed length
            raise ValueError(f"Entropy input length == seed length {self.seed_length} !!!")

        # 2.4.3 ===== Verify the Additional Input conditions otherwise create additional string ======================

        if len(add_in) != 0:                            # if the provided data is available

            if len(add_in) != self.seed_length:         # Check if the additional input == seed length
                raise ValueError(f"Additional input length == seed length {self.seed_length} !!!")

        else:                                           # if add_in length == 0, create one using bytes_padding function

            cjp = b"Chirag Patel" * 2                   # select a random byte string to initiate
            add_in = bytes_padding(cjp, self.seed_length)

        # 2.4.4 ===== Update the internal state of the variables =======================================================

        seed_material = strings_xor(entropy_in, add_in)  # Prepare the seed material by XORing inputs

        self.update(seed_material)                      # Call the update method to refresh the key and the counter

        self.reseed_counter = 1                         # Set the reseed counter to one

    # 2.5 ==============================================================================================================

    def generate(self, req_bytes, add_in=b''):

        # 2.5.1 ===== Verify the Reseed interval conditions ============================================================

        if self.reseed_counter > self.reseed_interval:
            raise Warning("the DRBG should be reseeded !!!")

        # 2.5.2 ===== Verify the Additional Input conditions ===========================================================

        if len(add_in) != 0:                            # Check if the additional input is provided

            if len(add_in) != self.seed_length:         # the additional input must be equal to the seed length
                raise ValueError("Additional input length == seed length !!!")

        else:                                           # if add_in length == 0, create one using bytes_padding function

            cjp = b"Chirag Patel" * 2                   # select a random byte string to initiate
            add_in = bytes_padding(cjp, self.seed_length)
            # Call the update method with the additional input as an argument, and update the key and the counter

        self.update(add_in)                             # Call the update method to refresh the key and the counter

        # 2.5.3 ===== Generate the output using a loop =================================================================

        temp = b''                                      # create an empty buffer for the output bytes
        while len(temp) < req_bytes:                    # loop until the requested bytes are generated

            block_128 = bytes_padding(b"\x00", self.out_length)  # Generate string of zero == default output block length

            output_block = self.aes.encrypt(
                block_128, )  # Encrypt block_128 with the current key and counter, and get an output block of 128 bits

            temp = temp + output_block                  # collect the output blocks to the temporary byte string

            self.ctr.increment()                        # Increment the counter by one, and return zero when reach maximum

        # 2.5.4 ===== Prepare the output and the generate function for the next execution ==============================

        returned_bytes = temp[0:req_bytes]              # Return the requested number of bytes from the temporary byte string
        self.update(add_in)                             # Call the update method to refresh the key and the counter
        self.reseed_counter = self.reseed_counter + 1   # Increment the reseed counter by one

        return returned_bytes                           # Return the random binary sequence
