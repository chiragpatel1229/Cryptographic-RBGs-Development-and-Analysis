import struct
import os


"""
-> The chacha20 block cipher generates 512 bits per execution but a very small change in the input, even a single byte
   of change in the input can produce completely different output
-> This algorithm is tested against the given parameters in the research paper
-> This algorithm is modified in way to generate 4000 bits per execution by setting the 
    block generation function in loop.
"""
# References: ChaCha20 and Poly1305 for IETF Protocols: RFC 8439


# 0.0 User INPUT, Define the key, counter and nonce ====================================================================

# key_in = os.urandom(32)                                     # the secret key should be always 32 bytes (256-bit) random string
# counter_in = 1                                              # initial counter should be 1 or 0, 4 bytes (32 bits)
# nonce_in = os.urandom(12)                                   # nonce could be any string of 12 bytes (96-bit)


# 1.0 =========== Convert The Data Types to Store ========================================================================

def b2i(data):                                              # convert bytes to a list of integers
    binary_string = ''                                      # Convert each byte to a binary string and join them
    for byte in data:
        binary_string += bin(byte)[2:].zfill(8)             # convert each byte to binary of 8 characters and append
    integer_list = [int(bit) for bit in binary_string]      # Convert the binary string to a list of integers
    return integer_list


# 2.0 =========== Convert The Data Types to Store ======================================================================

def chacha20_block(key, counter, nonce, num_bits):

    # 2.1. Block =========== state selection function to perform rounds ================================================

    def rounds(a, b, c, d):             # ChaCha20 quarter round function to manage state wise operation
        a = (a + b) & 0xFFFFFFFF        # Addition and XOR operations on the states
        d = (d ^ a) & 0xFFFFFFFF
        d = (d << 16) | (d >> 7)       # performs a bit-wise circular shift to the right and left, lastly 'OR' "|" between both

        c = (c + d) & 0xFFFFFFFF
        b = (b ^ c) & 0xFFFFFFFF
        b = (b << 12) | (b >> 9)       # "<<" means 'b' to the left by 12 positions = multiplying 'b' by 2^12

        a = (a + b) & 0xFFFFFFFF
        d = (d ^ a) & 0xFFFFFFFF        # "0xFFFFFFFF" is to make sure the result will always be a 32-bit unsigned integer
        d = (d << 8) | (d >> 13)

        c = (c + d) & 0xFFFFFFFF
        b = (b ^ c) & 0xFFFFFFFF
        b = (b << 7) | (b >> 18)        # ">>" means 'b' to the right by 25 positions = dividing 'b' by 2^25

        return a, b, c, d               # Return the modified states of the selected index

    # 2.2. Block =========== handle the states of ChaCha Matrix ========================================================

    def quarter_round(st, a, b, c, d):  # decide where the quarter round operation will be applied (st = state)
        st[a], st[b], st[c], st[d] = rounds(st[a], st[b], st[c], st[d])
        # In-place modification, it replaces the values at the same indices with the result of quarter round

    # 2.3. Block =========== ChaCha20 block function ===================================================================

    def chacha20_block_function(key_, counter_, nonce_):

        """ The Constants and the quarter rounds are based on the 'RFC 8439' document, but it can be changed 
        upon the requirements... """""

        constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
        key_state = struct.unpack('<8L', key_)              # 8 * 4 = 32 bytes values to unpack in a "<" little-endian byte order
        nonce_state = struct.unpack('<3L', nonce_)          # 3 * 4 = 12 bytes values to unpack in unsigned long integer 'L'
        counter_state = struct.unpack('<L', counter_)       # 1 * 4 = 4 bytes = 32-bit block counter parameter

        state = list(constants) + list(key_state) + list(counter_state) + list(nonce_state)
        s_s = list(state)                                   # steady state list for the iterations bcz it is mutable in python
        # steady state will store the result from the for loop

        for _ in range(10):                                 # Total 20 rounds = (8 quarter rounds) * 10
            quarter_round(s_s, 0, 4, 8, 12)   # Column rounds
            quarter_round(s_s, 1, 5, 9, 13)   # Column rounds
            quarter_round(s_s, 2, 6, 10, 14)  # Column rounds
            quarter_round(s_s, 3, 7, 11, 15)  # Column rounds
            quarter_round(s_s, 0, 5, 10, 15)  # Diagonal rounds
            quarter_round(s_s, 1, 6, 11, 12)  # Diagonal rounds
            quarter_round(s_s, 2, 7, 8, 13)   # Diagonal rounds
            quarter_round(s_s, 3, 4, 9, 14)   # Diagonal rounds

        result = []                                         # add the original input words to the output words and
        for x, y in zip(state, s_s):                        # for 2 lists addition we use Zip function to create a single list
            result.append((x + y) & 0xFFFFFFFF)             # "0xFFFFFFFF" is to make sure the result will always be a 32-bit unsigned integer

        result = struct.pack('<16L', * result)              # 16 * 4 = 64 bytes, serialize the result by sequencing each word in little-endian order

        return result

    key_stream = b""                                        # initialize an empty string buffer
    counter_bytes = struct.pack('<L', counter)              # serialize the result by sequencing each word in little-endian order

    while len(key_stream) * 8 < num_bits:
        block = chacha20_block_function(key, counter_bytes, nonce)
        key_stream += block

    return key_stream[:num_bits // 8]


# 3.0 =========== Call the function ====================================================================================

num_sequences = 100
bits_per_sequence = 4000

with open('ChaCha20.txt', 'w') as file:
    for _ in range(num_sequences):
        key_in = os.urandom(32)  # the secret key should be always 32 bytes (256-bit) random string
        counter_in = 1  # initial counter should be 1 or 0, 4 bytes (32 bits)
        nonce_in = os.urandom(12)  # nonce could be any string of 12 bytes (96-bit)
        sequence = chacha20_block(key_in, counter_in, nonce_in, bits_per_sequence)
        binary_sequence = ''.join(map(str, b2i(sequence)))
        file.write(binary_sequence + '\n')


