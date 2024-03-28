from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import secrets

'''
-> References: The CTR-DRBG mechanism based on NIST SP800-90A Publication
-> Please consider all the Input parameters in bytes...
-> A single output fix block length is 128 bits or 16 bytes

-> This file generates only one sequence per execution the reseed is not required, while generating more than one sequences and the
-> reseed counter reach the max interval leval the drbg need to be reseeded using the reseed function with new entropy and data
-> Comments and the variable names are also referenced from the given NIST document
'''


# 0.0 =========== User Inputs ==========================================================================================
'''When the in_seed (initial seed) and per_str (personalise string) values are None, the algorithm provides itself the seed and 
the string internally using the device's entropy pool. But a user can provide desired inputs.'''
sel_CTR_cipher_name = 'AES256'                          # Select one cipher from this list ('aes128', 'aes192', 'aes256')
in_seed = None                                          # For the initial seed length can be [48, 40, 32] bytes
per_str = None                                          # personalise string length should be equal to seed length
output_bytes = 500                                       # OUTPUT bytes: 32 * 8 = 256 bits < 4000 bits or 500 byts

# ============== Use the Derivation Function with a Block Cipher Algorithm =============================================
in_put_string = b'Test String to check the Block Cipher function.'          # use any string to create a cipher text
bits_to_return = 128                                    # the return bits should be less than 512 bytes


# 1.0 =========== Convert The Data Types to print or Store the final output ============================================
def b2i(data):                                              # convert bytes to a list of integers
    binary_string = ''                                      # Convert each byte to a binary string and join them
    for byte in data:
        binary_string += bin(byte)[2:].zfill(8)             # convert each byte to binary of 8 characters and append
    # integer_list = [int(bit) for bit in binary_string]      # Convert the binary string to a list of integers
    return binary_string


# 2.0 =========== Convert The Data Types for convenience ===============================================================
def strings_xor(a, b):                              # XOR two byte strings
    x_str = bytes(x ^ y for x, y in zip(a, b))
    return x_str


def bytes_padding(a, n):                            # Pad or extend a byte string with zeros
    padded_bytes = a + b'\x00' * (n - len(a))       # example: extend the Byte String: b'\x01\x02\x03\x00\x00\x00\x00\x00'
    return padded_bytes


def bytes2long_int(a):                              # Convert a byte string to a long integer
    long_int = int.from_bytes(a, 'big')             # example: b'\x01\x02\x03\x04' = 16909060
    return long_int


def long_int2bytes(a):                              # Convert a long integer to a byte string
    l2bytes = a.to_bytes((a.bit_length() + 7) // 8, 'big')     # example: 16909060 = b'\x01\x02\x03\x04'
    return l2bytes


# 3.0 =========== The CTR-Drbg class ===================================================================================


class CTRDRBG:                                      # class for CTR-DRBG mechanism

    # 3.1 Initialize CTR class with a name of required block cipher and entropy and data ===============================
    def __init__(self, name, entropy=None):              # Data = Personalization string

        # ===== Initialize the important variables in this algorithm ===================================================

        self.V = None
        self.key = None
        self.reseed_counter = None

        name = name.lower()                         # Convert the name to lowercase in case of different user input

        if name not in ['aes128', 'aes192', 'aes256']:      # Check if the name is a valid cipher name
            raise ValueError(f'This is an Unknown cipher: {name}')

        # ===== Set the cipher, key length, output length and flag for AES or TDEA as per NIST =========================
        if name.startswith('aes'):
            self.cipher     = AES
            self.key_length = int(name[3:])
            self.out_length = 128
            self.is_aes     = True

        # ===== Set the maximum request size and seed length ===========================================================
        self.max_request_size = pow(2, 12)          # Maximum bytes or 2^12 < 2^19 bits  for AES mentioned in table-3 but check on Page-84
        self.reseed_interval  = 100000              # Max reseed intervals is 2^48 bits for AES but check p-84
        self.seed_length = (self.out_length + self.key_length) // 8

        if entropy:                                 # Initialize the DRBG with entropy and data if provided
            self.instantiate()

    # 3.2 ==============================================================================================================

    def instantiate(self, entropy=None, data=None):

        if entropy is None:
            entropy = os.urandom(self.seed_length)       # Obtain an entropy source that can provide at least 48 bytes of random bytes
        if data is None:
            data = b'Indian cuisine is most favourite!' + b'\x25'  # Provide a personalization string that is unique to your application and 48 bytes long

        # ===== Verify the Entropy Input conditions ====================================================================
        if len(entropy) != self.seed_length:
            raise ValueError(f'Entropy should be exactly {self.seed_length} bytes long')

        # ===== Verify the personalization string conditions ===========================================================

        if data:                                    # If data is provided, xor it with the entropy after padding
            if len(data) > self.seed_length:
                raise ValueError(f'Only { self.seed_length} bytes of data supported.')

            bytes_padding(data, self.seed_length)
            seed_material = strings_xor(entropy, data)

        else:                                       # Otherwise, use the entropy as the seed material
            seed_material = entropy

        # ===== set the internal state of the variables ================================================================

        Key = b'\x00' * (self.key_length // 8)      # Initialize the key and the counter with zeros
        V = b'\x00' * (self.out_length // 8)

        self.key, self.V = self.update(seed_material, Key, V)   # Update the key and the counter with the seed material
        self.reseed_counter = 1

    # 3.3 ==============================================================================================================

    def generate(self, count, data=None):           # Generate random bytes with optional data

        # ===== Verify required conditions and update the key and the counter ==========================================

        if (count * 8) > self.max_request_size:
            raise RuntimeError(f"It is not possible to generate {count} bytes which is more than 500 bytes in a single call.")

        if self.reseed_counter >= self.reseed_interval:
            raise Warning("The CTR Class is require to reseeded now !!!")

        if data:                                    # if the data is provided by the user
            if len(data) > self.seed_length:        # Check the length of the data
                raise ValueError('Additional data is more than required !!!')

        else:                                       # if data is not provided then Use the internally provided data
            data = b'A user can add here anything. Based on NIST standards'  # it can be any length, we used padding in the next step

        self.key, self.V = self.update(data, self.key, self.V)

        # ===== Generate the output using a loop =======================================================================

        temp = b''                                  # Initialize an empty string to buffer
        K, V = self.key, self.V                     # Copy the key and the counter

        while len(temp) < count:                    # Loop until the string buffer is filled with the requested bits

            V = long_int2bytes((bytes2long_int(V) + 1) % 2 ** self.out_length)  # Increment the counter modulo 2^outlen

            if len(V) < self.out_length // 8:       # Pad the counter with zeros if needed
                V = (b'\x00' * (self.out_length // 8 - len(V))) + V

            temp += self.cipher.new(K, AES.MODE_ECB).encrypt(V)     # Encrypt the counter with the key and append it to the buffer

        # ===== Prepare the generate function for the next execution   ===================================================

        self.key, self.V = self.update(data or b'', K, V)  # Update the key and the counter with the data or zeros

        self.reseed_counter += 1

        return temp[:count]                         # Return the requested number of bytes from the buffer

    # 3.4 ==============================================================================================================

    def reseed(self, data=None):                    # Reseed the DRBG with entropy and optional data

        entropy = secrets.token_bytes(self.seed_length)  # reseed_entropy must be equal to the seed length, check line: 164

        # ===== Verify the data and Entropy Input conditions ===========================================================
        if data:                                    # Check the length of the data
            if len(data) > self.seed_length:
                raise ValueError('Additional data is more than required !!!')

        else:                                       # Use internal data if data is not provided
            data = b'A user can add here anything. Based on NIST standards'  # it can be any length, used padding in the next step
            data = bytes_padding(data, self.seed_length)

        if len(entropy) != self.seed_length:
            raise ValueError(f'Too much entropy. it should be {self.seed_length}')

        seed_material = strings_xor(entropy, bytes_padding(data, self.seed_length))     # If data is provided or not, xor it with the entropy after padding

        # ===== Update the internal state of the variables ==============================================================

        self.key, self.V = self.update(seed_material, self.key, self.V)
        self.reseed_counter = 1

    # 3.5 ==============================================================================================================

    def update(self, provided_data, Key, V):        # Update the key and the counter with provided data

        # ===== generate a temporary string to refresh the internal variables ==========================================

        temp = b''                                  # Initialize an empty string buffer

        cipher = self.cipher.new(Key, AES.MODE_ECB)     # Create a cipher object with the key

        while len(temp) < self.seed_length:         # Loop until the buffer is filled

            V = long_int2bytes((bytes2long_int(V) + 1) % 2 ** self.out_length)  # Increment the counter modulo 2^outlen

            if len(V) < self.out_length // 8:       # Pad the counter with zeros if needed
                V = (b'\x00' * (self.out_length // 8 - len(V))) + V

            temp += cipher.encrypt(V)               # Encrypt the counter with the key and append it to the buffer

        # ===== XOR the provided input and temporary string to improve the entropy =====================================

        temp = strings_xor(temp[:self.seed_length], bytes_padding(provided_data, self.seed_length))

        Key = temp[:self.key_length // 8]           # Split the updated buffer into the new key and counter
        V   = temp[-self.out_length // 8:]

        return Key, V                               # Return the new key and counter

    # 3.5 ==============================================================================================================
    # Block_Encrypt is used for convenience in the specification of the BCC function. This function is not specifically defined in this Recommendation
    # A basic encryption operation that uses the selected block cipher algorithm. page - 61
    @staticmethod
    def Block_Encrypt(Key, input_block):
        # the basic encryption operation is called the forward cipher operation (see [SP 800-67]); for AES,
        # the basic encryption operation is called the cipher operation (see [FIPS 197]).
        # The basic encryption operation is equivalent to an encryption operation on a single block of data using the ECB mode.

        cipher = AES.new(Key, AES.MODE_ECB)                                 # create a hash object to encrypt the data using the key
        output_block = cipher.encrypt(pad(input_block, AES.block_size))     # encrypt the input block provided by the block cipher function

        return output_block                         # return the hashed block for the provided data

    # 3.5 ==============================================================================================================
    # For the BCC function, let outlen be the length of the output block of the block cipher algorithm to be used.
    def BCC(self, Key, data):

        # data: The data to be operated upon. Note that the length of data must be a multiple of outlen.
        # This is guaranteed by Block_Cipher_df process steps 4 and 8.1 in Section 10.3.2.
        # The length of data must be a multiple of outlen.
        remindr = len(data) % self.out_length               # find the reminder
        if remindr != 0:                                    # check if the length of data is no multiple of out length
            padding_len = self.out_length - remindr         # find the required bytes
            data += b'\x00' * padding_len                   # add the required zero bytes

        chaining_value = bytes([0]*self.out_length)         # Set the first chaining value to outlen zeros.
        n = len(data) // self.out_length

        # 3.Starting with the leftmost bits of data, split data into n blocks of outlen bits each, forming block-1 to block-n.
        blocks = []
        for i in range(0, len(data), self.out_length):
            block = data[i:i + self.out_length]             # separate the blocks of out length
            blocks.append(block)

        for i in range(n):
            input_block = []
            for a, b in zip(chaining_value, blocks[i]):     # XOR each block with changing value byte string
                xor_result = a ^ b
                input_block.append(xor_result)
            input_block = bytes(input_block)

            chaining_value = self.Block_Encrypt(Key, input_block)   # get the new value for each iteration

        output_block = chaining_value
        return output_block

    # 3.5 ==============================================================================================================
    # 10.3.2 Derivation Function Using a Block Cipher Algorithm (Block_Cipher_df) page - 59
    def Block_Cipher_df(self, input_string, no_of_bits_to_return):

        # The maximum length (max_number_of_bits) is 512 bits for the currently approved block cipher algorithms. p-59
        max_number_of_bits = 512
        if no_of_bits_to_return > max_number_of_bits:           # point 1 - error flag p-59
            return 'ERROR_FLAG', None

        # L is the bitstring representation of the integer resulting from len (input_string)/8.
        L = len(input_string) // 8
        L = L.to_bytes(4, 'big')                                # L shall be represented as a 32-bit integer.

        # N is the bitstring representation of the integer resulting from number_of_bits_to_return/8.
        N = no_of_bits_to_return // 8
        N = N.to_bytes(4, 'big')                                # N shall be represented as a 32-bit integer.

        # Prepend the string length and the requested length of the output to the input_string.
        S = L + N + input_string + b'\x80'                      # string length s is prepares as recommended on p-60

        while len(S) % (self.out_length // 8) != 0:             # Pad S with zeros, if necessary.
            S += b'\x00'

        temp_1 = b''                                            # prepare the empty buffer for to store the bytes
        i = 0
        i = i.to_bytes(4, 'big')
        K = self.key

        while len(temp_1) < self.seed_length:                   # seed length = keylen + outlen
            IV = i + b'\x00' * ((self.out_length // 8) - 4)     # The 32-bit integer representation of i is padded with zeros to outlen bits.
            temp_1 += self.BCC(K, IV + S)
            i += 1

        # Compute the requested number of bits now p-60
        K = temp_1[:self.key_length // 8]                       # trim the data from the temp_1 byte string equal to key length
        X = temp_1[self.key_length // 8:self.seed_length]

        temp_2 = b''                                            # prepare the empty buffer for to store the bytes
        while len(temp_2) < no_of_bits_to_return:
            X = self.Block_Encrypt(K, X)
            temp_2 += X

        requested_bits = temp_2[:no_of_bits_to_return]
        return 'SUCCESS', requested_bits


# 4.0 =========== Call the class and its functions, required input data is =============================================
# =============== being generated inside the function so the user does not need to add it manually =====================

drbg = CTRDRBG(sel_CTR_cipher_name)                 # initialize or select the security strength
drbg.instantiate(in_seed, per_str)                  # initiate the algorithm with the fresh entropy and the personalizing string
random_bytes = drbg.generate(output_bytes)          # select the number of bytes to generate and the personalizing string
print(b2i(random_bytes), "\nTotal number of Bits:", len(b2i(random_bytes)))      # print the generated bytes converted in the list of integers

# Use Block_Cipher_df function
status, req_bits = drbg.Block_Cipher_df(in_put_string, bits_to_return)
print(f"Status: {status}, \nRequested Bits: {req_bits}")
print(len(req_bits))


# Open a file to write
# with open("CTR_DRBG.txt", "w") as file:
#     for _ in range(100):
#         random_bytes = drbg.generate(output_bytes)
#         file.write(b2i(random_bytes) + '\n')
#
# print("Files is ready!")