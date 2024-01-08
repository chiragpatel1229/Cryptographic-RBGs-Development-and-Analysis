from Crypto.Cipher import AES, DES3
import os
import secrets


# References: The CTR-DRBG mechanism based on NIST SP800-90A Publication
# Please consider all the Input parameters in bytes...

# 0.0 =========== User Inputs ==========================================================================================

sel_CTR_cipher_name = 'AES256'              # Select one cipher from this list ('aes128', 'aes192', 'aes256')
init_entropy = os.urandom(48)               # init_entropy must be equal to the seed length, check line: 99 & 96
init_data = b'Indian cuisine is most favourite!' + b'\x25'           # This is personalized string that can be anything but not more than seed length


output_bytes = 32                           # OUTPUT bytes: 32 * 8 = 256 bits < 7500
additional_data = b'A user can add here anything.'    # it should not be more than seed length but can be anything


reseed_entropy = secrets.token_bytes(48)    # reseed_entropy must be equal to the seed length, check line: 164
reseed_data = b'information' + b'electrical'            # It should not be more than seed length but can be anything


# 1.0 =========== Convert The Data Types to print or Store =============================================================

def b2i(data):                                              # convert bytes to a list of integers
    binary_string = ''                                      # Convert each byte to a binary string and join them
    for byte in data:
        binary_string += bin(byte)[2:].zfill(8)             # convert each byte to binary of 8 characters and append
    integer_list = [int(bit) for bit in binary_string]      # Convert the binary string to a list of integers
    return integer_list


# 2.0 =========== Convert The Data Types for convenience ===============================================================

def strings_xor(a, b):                           # XOR two byte strings
    x_str = bytes(x ^ y for x, y in zip(a, b))
    return x_str


def bytes_padding(a, n):                         # Pad or extend a byte string with zeros
    padded_bytes = a + b'\x00' * (n - len(a))    # example: extend the Byte String: b'\x01\x02\x03\x00\x00\x00\x00\x00'
    return padded_bytes


def bytes2long_int(a):                           # Convert a byte string to a long integer
    long_int = int.from_bytes(a, 'big')          # example: b'\x01\x02\x03\x04' = 16909060
    return long_int


def long_int2bytes(a):                           # Convert a long integer to a byte string
    l2bytes = a.to_bytes((a.bit_length() + 7) // 8, 'big')     # example: 16909060 = b'\x01\x02\x03\x04'
    return l2bytes


# 3.0 =========== The CTR-Drbg class ===================================================================================


class CTRDRBG:                                      # class for CTR-DRBG mechanism

    # 3.1 Initialize CTR class with a name of required block cipher and entropy and data ===============================
    def __init__(self, name, entropy=None, data=None):              # Data = Personalization string

        # Internal state variables  ====================================================================================

        self.V = None
        self.key = None
        self.reseed_counter = None

        name = name.lower()                         # Convert the name to lowercase in case of different user input

        if name not in ['aes128', 'aes192', 'aes256']:      # Check if the name is a valid cipher name
            raise ValueError('Unknown cipher: {}'.format(name))

        # Set the cipher, key length, output length and flag for AES or TDEA as per NIST ===============================
        if name.startswith('aes'):
            self.cipher = AES
            self.keylen = int(name[3:])
            self.outlen = 128
            self.is_aes = True
        else:
            self.cipher = DES3
            self.keylen = 168
            self.outlen = 64
            self.is_aes = False

        # Set the maximum request size and seed length =================================================================
        self.max_request_size = 4000                # Maximum bytes or 2^16 < 2^19 bits  for AES mentioned in table-3 but check on Page-84
        self.reseed_interval = 100000               # Max reseed intervals is 2^48 bits for AES but check p-84
        self.seedlen = (self.outlen + self.keylen) // 8

        if entropy:                                 # Initialize the DRBG with entropy and data if provided
            self.init(entropy, data)

    # 3.2 ==============================================================================================================

    def init(self, entropy, data=None):             # Initialize the DRBG with entropy and optional data

        # Check the length of the entropy ==============================================================================
        if len(entropy) != self.seedlen:
            raise ValueError('Entropy should be exactly {} bytes long'.format(
                             self.seedlen))

        if data:                                    # If data is provided, xor it with the entropy after padding
            if len(data) > self.seedlen:
                raise ValueError('Only {} bytes of data supported.'.format(
                                 self.seedlen))
            delta = len(entropy) - len(data)
            if delta > 0:
                data = (b'\x00' * delta) + data
            seed_material = strings_xor(entropy, data)

        else:                                       # Otherwise, use the entropy as the seed material
            seed_material = entropy

        Key = b'\x00' * (self.keylen // 8)          # Initialize the key and the counter with zeros
        V = b'\x00' * (self.outlen // 8)

        self.key, self.V = self.update(seed_material, Key,
                                       V)  # Update the key and the counter with the seed material
        self.reseed_counter = 1

    # 3.3 ==============================================================================================================

    def generate(self, count, data=None):          # Generate random bytes with optional data

        if (count * 8) > self.max_request_size:
            raise RuntimeError("It is not possible to generate more than 2^16 bits in a single call.")

        if self.reseed_counter >= self.reseed_interval:
            raise RuntimeError("Reseed required for further bit generation")

        if data and len(data) > self.seedlen:      # Check the length of the data
            raise ValueError('Too much data.')

        if data:                                   # If data is provided, pad it with zeros and update the key and the counter
            data += b'\x00' * (self.seedlen - len(data))
            self.key, self.V = self.update(data, self.key, self.V)

        temp = b''                                  # Initialize an empty string to buffer

        K, V = self.key, self.V                 # Copy the key and the counter

        while len(temp) < count:                    # Loop until the string buffer is filled with the requested bits

            V = long_int2bytes((bytes2long_int(V) + 1) % 2 ** self.outlen)  # Increment the counter modulo 2^outlen

            if len(V) < self.outlen // 8:           # Pad the counter with zeros if needed
                V = (b'\x00' * (self.outlen // 8 - len(V))) + V

            temp += self.cipher.new(self.prepare_key(K), AES.MODE_ECB).encrypt(V)     # Encrypt the counter with the key and append it to the buffer

        self.key, self.V = self.update(data or b'', K, V)  # Update the key and the counter with the data or zeros

        self.reseed_counter += 1

        return temp[:count]                         # Return the requested number of bytes from the buffer

    # 3.4 ==============================================================================================================

    def reseed(self, entropy, data=None):           # Reseed the DRBG with entropy and optional data

        if data and len(data) > self.seedlen:       # Check the length of the entropy and the data
            raise ValueError('Too much data.')
        if len(entropy) != self.seedlen:
            raise ValueError(f'Too much entropy. it should be {self.seedlen}')

        if data:                                    # If data is provided, xor it with the entropy after padding
            seed_material = strings_xor(entropy, bytes_padding(data, self.seedlen))

        else:                                       # Otherwise, use the entropy as the seed material
            seed_material = entropy

        self.key, self.V = self.update(seed_material, self.key, self.V)
        self.reseed_counter = 1

    # 3.5 ==============================================================================================================

    def update(self, provided_data, Key, V):        # Update the key and the counter with provided data

        temp = b''                                  # Initialize an empty string buffer

        cipher = self.cipher.new(self.prepare_key(Key), AES.MODE_ECB)     # Create a cipher object with the key

        while len(temp) < self.seedlen:             # Loop until the buffer is filled

            V = long_int2bytes((bytes2long_int(V) + 1) % 2 ** self.outlen)  # Increment the counter modulo 2^outlen

            if len(V) < self.outlen // 8:           # Pad the counter with zeros if needed
                V = (b'\x00' * (self.outlen // 8 - len(V))) + V

            temp += cipher.encrypt(V)               # Encrypt the counter with the key and append it to the buffer

        temp = strings_xor(temp[:self.seedlen], bytes_padding(provided_data, self.seedlen))

        Key = temp[:self.keylen // 8]               # Split the buffer into the new key and counter
        V = temp[-self.outlen // 8:]

        return Key, V                               # Return the new key and counter

    # 3.6 ==============================================================================================================

    def prepare_key(self, K):
        if self.is_aes:                             # If AES is selected then return K as it is.
            return K


# 4.0 =========== Call the class and its functions =====================================================================
drbg = CTRDRBG(sel_CTR_cipher_name)                             # initialize or select the security strength
drbg.init(init_entropy, init_data)                              # initiate the algorithm with the fresh entropy and the personalizing string
random_bytes = drbg.generate(output_bytes, additional_data)     # select the number of bytes to generate and the personalizing string
drbg.reseed(reseed_entropy, reseed_data)                        # refresh the initial states by providing the entropy and the personalizing string
print(b2i(random_bytes), "\n", "Total number of Bits:", len(b2i(random_bytes)))      # print the generated bytes converted in the list of integers
