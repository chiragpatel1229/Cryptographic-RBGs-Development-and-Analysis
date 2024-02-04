from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import secrets


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


class CTRDRBG:                                      # class for CTR-DRBG mechanism
    def __init__(self, name, entropy=None):              # Data = Personalization string
        self.V = None
        self.key = None
        self.reseed_counter = None
        name = name.lower()                         # Convert the name to lowercase in case of different user input
        if name not in ['aes128', 'aes192', 'aes256']:      # Check if the name is a valid cipher name
            raise ValueError(f'This is an Unknown cipher: {name}')
        if name.startswith('aes'):
            self.cipher     = AES
            self.key_length = int(name[3:])
            self.out_length = 128
            self.is_aes     = True
        self.max_request_size = pow(2, 12)          # Maximum bytes or 2^12 < 2^19 bits  for AES mentioned in table-3 but check on Page-84
        self.reseed_interval  = 100000              # Max reseed intervals is 2^48 bits for AES but check p-84
        self.seed_length = (self.out_length + self.key_length) // 8
        if entropy:                                 # Initialize the DRBG with entropy and data if provided
            self.instantiate()

    def instantiate(self, entropy=None, data=None):
        if entropy is None:
            entropy = os.urandom(self.seed_length)       # Obtain an entropy source that can provide at least 48 bytes of random bytes
        if data is None:
            data = b'Indian cuisine is good!'            # Provide a personalization string that is unique to your application and 48 bytes long
        if len(entropy) != self.seed_length:
            raise ValueError(f'Entropy should be exactly {self.seed_length} bytes long')
        if data:                                    # If data is provided, xor it with the entropy after padding
            if len(data) > self.seed_length:
                raise ValueError(f'Only { self.seed_length} bytes of data supported.')
            bytes_padding(data, self.seed_length)
            seed_material = strings_xor(entropy, data)
        else:                                       # Otherwise, use the entropy as the seed material
            seed_material = entropy
        Key = b'\x00' * (self.key_length // 8)      # Initialize the key and the counter with zeros
        V = b'\x00' * (self.out_length // 8)
        self.key, self.V = self.update(seed_material, Key, V)   # Update the key and the counter with the seed material
        self.reseed_counter = 1

    def generate(self, count, data=None):           # Generate random bytes with optional data
        if (count * 8) > self.max_request_size:
            raise RuntimeError(f"It is not possible to generate {count} bytes which is more than 500 bytes in a single call.")
        if self.reseed_counter > self.reseed_interval:
            raise Warning("The CTR Class is require to reseeded now !!!")
        if data:                                    # if the data is provided by the user
            if len(data) > self.seed_length:        # Check the length of the data
                raise ValueError('Additional data is more than required !!!')
        else:                                       # if data is not provided then Use the internally provided data
            data = b'A user can add here anything. Based on NIST standards'  # it can be any length, later used padding in the next step
        self.key, self.V = self.update(data, self.key, self.V)
        temp = b''                                  # Initialize an empty string to buffer
        K, V = self.key, self.V                     # Copy the key and the counter
        while len(temp) < count:                    # Loop until the string buffer is filled with the requested bits
            V = long_int2bytes((bytes2long_int(V) + 1) % 2 ** self.out_length)  # Increment the counter modulo 2^outlen
            if len(V) < self.out_length // 8:       # Pad the counter with zeros if needed
                V = (b'\x00' * (self.out_length // 8 - len(V))) + V
            temp += self.cipher.new(K, AES.MODE_ECB).encrypt(V)     # Encrypt the counter with the key and append it to the buffer
        self.key, self.V = self.update(data or b'', K, V)  # Update the key and the counter with the data or zeros
        self.reseed_counter += 1
        return temp[:count]                         # Return the requested number of bytes from the buffer

    def reseed(self, data=None):                    # Reseed the DRBG with entropy and optional data
        entropy = secrets.token_bytes(self.seed_length)  # reseed_entropy must be equal to the seed length, check line: 164
        if data:                                    # Check the length of the data
            if len(data) > self.seed_length:
                raise ValueError('Additional data is more than required !!!')
        else:                                       # Use internal data if data is not provided
            data = b'A user can add here anything. Based on NIST standards'  # it can be any length, used padding in the next step
            data = bytes_padding(data, self.seed_length)
        if len(entropy) != self.seed_length:
            raise ValueError(f'Too much entropy. it should be {self.seed_length}')
        seed_material = strings_xor(entropy, bytes_padding(data, self.seed_length))     # If data is provided or not, xor it with the entropy after padding
        self.key, self.V = self.update(seed_material, self.key, self.V)
        self.reseed_counter = 1

    def update(self, provided_data, Key, V):        # Update the key and the counter with provided data
        temp = b''                                  # Initialize an empty string buffer
        cipher = self.cipher.new(Key, AES.MODE_ECB)     # Create a cipher object with the key
        while len(temp) < self.seed_length:         # Loop until the buffer is filled
            V = long_int2bytes((bytes2long_int(V) + 1) % 2 ** self.out_length)  # Increment the counter modulo 2^outlen
            if len(V) < self.out_length // 8:       # Pad the counter with zeros if needed
                V = (b'\x00' * (self.out_length // 8 - len(V))) + V
            temp += cipher.encrypt(V)               # Encrypt the counter with the key and append it to the buffer
        temp = strings_xor(temp[:self.seed_length], bytes_padding(provided_data, self.seed_length))
        Key = temp[:self.key_length // 8]           # Split the updated buffer into the new key and counter
        V   = temp[-self.out_length // 8:]
        return Key, V                               # Return the new key and counter

    @staticmethod
    def Block_Encrypt(Key, input_block):
        cipher = AES.new(Key, AES.MODE_ECB)
        output_block = cipher.encrypt(pad(input_block, AES.block_size))
        return output_block

    def BCC(self, Key, data):
        outlen = len(Key)
        assert len(data) % outlen == 0, "Length of data must be a multiple of outlen"
        chaining_value = bytes([0]*outlen)
        n = len(data) // outlen
        blocks = [data[i:i+outlen] for i in range(0, len(data), outlen)]
        for i in range(n):
            input_block = bytes(a ^ b for a, b in zip(chaining_value, blocks[i]))
            chaining_value = self.Block_Encrypt(Key, input_block)
        output_block = chaining_value
        return output_block

    def Block_Cipher_df(self, input_string, no_of_bits_to_return):
        max_number_of_bits = 512
        if no_of_bits_to_return > max_number_of_bits:
            return 'ERROR_FLAG', None

        L = len(input_string) // 8
        N = no_of_bits_to_return // 8

        S = L.to_bytes(4, 'big') + N.to_bytes(4, 'big') + input_string + b'\x80'

        while len(S) % (self.out_length // 8) != 0:
            S += b'\x00'

        temp = b''
        i = 0
        K = bytes([x for x in range(1, self.key_length // 8 + 1)])

        while len(temp) < self.key_length // 8 + self.out_length // 8:
            IV = i.to_bytes(4, 'big') + b'\x00' * ((self.out_length // 8) - 4)
            temp += self.BCC(K, IV + S)
            i += 1

        K = temp[:self.key_length // 8]
        X = temp[self.key_length // 8:self.key_length // 8 + self.out_length // 8]

        temp = b''
        while len(temp) < no_of_bits_to_return:
            X = self.Block_Encrypt(K, X)
            temp += X

        requested_bits = temp[:no_of_bits_to_return]
        return 'SUCCESS', requested_bits


# Instantiate the CTRDRBG class with 'aes128'
drbg = CTRDRBG('aes128')
drbg.instantiate()
# Generate 16 bytes of random data
random_data = drbg.generate(16)
print(f"Random Data: {random_data}")

# Reseed the CTRDRBG
drbg.reseed()

# Generate 16 bytes of random data after reseeding
random_data = drbg.generate(16)
print(f"Random Data after Reseeding: {random_data}")

# Use Block_Cipher_df function
in_put_string = b'This is a test string.'
bits_to_return = 128
status, req_bits = drbg.Block_Cipher_df(in_put_string, bits_to_return)
print(f"Status: {status}, \nRequested Bits: {req_bits}")
print(len(req_bits))
