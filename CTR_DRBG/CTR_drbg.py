from Crypto.Cipher import AES, DES3


# ======================================================================================================================

def str_xor(a, b):                               # a function to xor two byte strings
    return bytes(x ^ y for x, y in zip(a, b))


def byte_pad(a, n):                              # a function to pad or extend a byte string with zeros
    return a + b'\x00' * (n - len(a))            # example: extend the Byte String: b'\x01\x02\x03\x00\x00\x00\x00\x00'


def bytes2long(a):                              # a function to convert a byte string to a long integer
    return int.from_bytes(a, 'big')             # example: b'\x01\x02\x03\x04' = 16909060


def long2bytes(a):                              # a function to convert a long integer to a byte string
    return a.to_bytes((a.bit_length() + 7) // 8, 'big')     # example: 16909060 = b'\x01\x02\x03\x04'


# ======================================================================================================================


class CTRDRBG:                                      # a class for the CTR-DRBG mechanism

    # Initialize the class with the name of the block cipher and optional entropy and data =============================
    def __init__(self, name, entropy=None, data=None):

        self.__V = None
        self.__key = None
        name = name.lower()                         # Convert the name to lowercase

        if name not in ['aes128', 'aes192', 'aes256', 'tdea']:      # Check if the name is a valid cipher
            raise ValueError('Unknown cipher: {}'.format(name))

        # Set the cipher, key length, output length and flag for AES or TDEA ===========================================
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
        self.max_request_size = 2**13                # bytes or 2**16 bits
        self.seedlen = (self.outlen + self.keylen) // 8

        if entropy:                                  # Initialize the DRBG with entropy and data if provided
            self.init(entropy, data)

    # ==================================================================================================================

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
            seed_material = str_xor(entropy, data)

        else:                                       # Otherwise, use the entropy as the seed material
            seed_material = entropy

        Key = b'\x00' * (self.keylen // 8)          # Initialize the key and the counter with zeros
        V = b'\x00' * (self.outlen // 8)

        self.__key, self.__V = self.__update(seed_material, Key, V)     # Update the key and the counter with the seed material

    # ==================================================================================================================

    def generate(self, count, data=None):          # Generate random bytes with optional data

        if data and len(data) > self.seedlen:      # Check the length of the data
            raise ValueError('Too much data.')

        if data:                                   # If data is provided, pad it with zeros and update the key and the counter
            data += b'\x00' * (self.seedlen - len(data))
            self.__key, self.__V = self.__update(data, self.__key,
                                                 self.__V)

        temp = b''                                  # Initialize an empty string to buffer

        K, V = self.__key, self.__V                 # Copy the key and the counter

        while len(temp) < count:                    # Loop until the string buffer is filled with the requested bits

            V = long2bytes((bytes2long(V) + 1) % 2**self.outlen)    # Increment the counter modulo 2^outlen

            if len(V) < self.outlen // 8:           # Pad the counter with zeros if needed
                V = (b'\x00' * (self.outlen // 8 - len(V))) + V

            temp += self.cipher.new(self.__prepare_key(K), AES.MODE_ECB).encrypt(V)     # Encrypt the counter with the key and append it to the buffer

        self.__key, self.__V = self.__update(data or b'', K, V)     # Update the key and the counter with the data or zeros

        return temp[:count]                         # Return the requested number of bytes from the buffer

    # ======================================================================================================================

    def reseed(self, entropy, data=None):           # Reseed the DRBG with entropy and optional data

        if data and len(data) > self.seedlen:       # Check the length of the entropy and the data
            raise ValueError('Too much data.')
        if len(entropy) != self.seedlen:
            raise ValueError('Too much entropy.')

        if data:                                    # If data is provided, xor it with the entropy after padding
            seed_material = str_xor(entropy, byte_pad(data, self.seedlen))

        else:                                       # Otherwise, use the entropy as the seed material
            seed_material = entropy

        self.__key, self.__V = self.__update(seed_material,     # Update the key and the counter with the seed material
                                             self.__key, self.__V)

    # ======================================================================================================================

    def __update(self, provided_data, Key, V):      # Update the key and the counter with provided data

        temp = b''                                  # Initialize an empty string buffer

        cipher = self.cipher.new(self.__prepare_key(Key), AES.MODE_ECB)     # Create a cipher object with the key

        while len(temp) < self.seedlen:             # Loop until the buffer is filled

            V = long2bytes((bytes2long(V) + 1) % 2**self.outlen)            # Increment the counter modulo 2^outlen

            if len(V) < self.outlen // 8:           # Pad the counter with zeros if needed
                V = (b'\x00' * (self.outlen // 8 - len(V))) + V

            temp += cipher.encrypt(V)               # Encrypt the counter with the key and append it to the buffer

        temp = str_xor(temp[:self.seedlen], byte_pad(provided_data, self.seedlen))

        Key = temp[:self.keylen // 8]               # Split the buffer into the new key and counter
        V = temp[-self.outlen // 8:]

        return Key, V                               # Return the new key and counter

    # ======================================================================================================================

    def __prepare_key(self, K):                     # Prepare the key for the cipher by adding parity bits if TDEA is used
        if self.is_aes:
            return K
        new_K = bytearray()
        long_K = bytes2long(K)
        while long_K > 0:
            new_K.append((long_K & 0x7f) << 1)
            long_K >>= 7
        new_K.reverse()
        return byte_pad(bytes(new_K), 192 // 8)
