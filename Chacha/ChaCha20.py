import struct


def chacha20_block(key, counter, nonce):

    # 1. Block =========== state selection function to perform rounds ===================================================

    def quarter_round(a, b, c, d):      # ChaCha20 quarter round function to manage state wise operation
        a = (a + b) & 0xFFFFFFFF        # Addition and XOR operations on the states
        d = (d ^ a) & 0xFFFFFFFF
        d = (d << 16) | (d >> 16)       # performs a bit-wise circular shift to the right and left, lastly 'OR' "|" between both

        c = (c + d) & 0xFFFFFFFF
        b = (b ^ c) & 0xFFFFFFFF
        b = (b << 12) | (b >> 20)       # "<<" means 'b' to the left by 12 positions = multiplying 'b' by 2^12

        a = (a + b) & 0xFFFFFFFF
        d = (d ^ a) & 0xFFFFFFFF        # "0xFFFFFFFF" is to make sure the result will always be a 32-bit unsigned integer
        d = (d << 8) | (d >> 24)

        c = (c + d) & 0xFFFFFFFF
        b = (b ^ c) & 0xFFFFFFFF
        b = (b << 7) | (b >> 25)        # ">>" means 'b' to the right by 25 positions = dividing 'b' by 2^25

        return a, b, c, d               # Return the modified states of the selected index

    # 2. Block =========== handle the states of ChaCha Matrix ===========================================================

    def chacha_quarter_round(state, a, b, c, d):  # decide where the quarter round operation will be applied
        state[a], state[b], state[c], state[d] = quarter_round(state[a], state[b], state[c], state[d])
        # In-place modification, it replaces the values at the same indices with the result of quarter round

    # 3. Block =========== ChaCha20 block function ======================================================================

    def chacha20_block_function(key_, counter_, nonce_):

        constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
        key_state = struct.unpack('<8L', key_)              # 8 * 4 = 32 bytes values to unpack in a "<" little-endian byte order
        nonce_state = struct.unpack('<3L', nonce_)          # 3 * 4 = 12 bytes values to unpack in unsigned long integer 'L'
        counter_state = struct.unpack('<L', counter_)       # 1 * 4 = 4 bytes = 32-bit block counter parameter

        state = list(constants) + list(key_state) + list(counter_state) + list(nonce_state)
        s_state = list(state)                               # steady state list for the iterations bcz it is mutable in python
        # s_state will store the result from the for loop

        for _ in range(10):                                             # Total 20 rounds
            chacha_quarter_round(s_state, 0, 4, 8, 12)      # Column rounds
            chacha_quarter_round(s_state, 1, 5, 9, 13)      # Column rounds
            chacha_quarter_round(s_state, 2, 6, 10, 14)     # Column rounds
            chacha_quarter_round(s_state, 3, 7, 11, 15)     # Column rounds
            chacha_quarter_round(s_state, 0, 5, 10, 15)     # Diagonal rounds
            chacha_quarter_round(s_state, 1, 6, 11, 12)     # Diagonal rounds
            chacha_quarter_round(s_state, 2, 7, 8, 13)      # Diagonal rounds
            chacha_quarter_round(s_state, 3, 4, 9, 14)      # Diagonal rounds

        result = []                                         # add the original input words to the output words and
        for x, y in zip(state, s_state):                    # for 2 lists addition we use Zip function to create a single list
            result.append((x + y) & 0xFFFFFFFF)

        result = struct.pack('<16L', * result)              # serialize the result by sequencing each word in little-endian order

        return result

    key_stream = b""
    counter_bytes = struct.pack('<L', counter)

    block = chacha20_block_function(key, counter_bytes, nonce)  # Generate 64 bytes of key_in stream (only one block at a time)
    key_stream += block

    return key_stream


# 4. =========== Convert The Data Types to Store ========================================================================

def bytes_to_int(data):                                     # convert bytes to a list of integers
    binary_string = ''                                      # Convert each byte to a binary string and join them
    for byte in data:
        binary_string += bin(byte)[2:].zfill(8)             # convert each byte to binary of 8 characters and append
    integer_list = [int(bit) for bit in binary_string]      # Convert the binary string to a list of integers
    return integer_list


# 5. =========== Encryption Function ====================================================================================

def chacha20_encrypt(key, counter, nonce, plaintext):
    encrypted_message = b""                                 # empty byte string to store the encrypted message
    block_count = len(plaintext) // 64                      # calculate 64-byte block from the plain text

    for j in range(block_count):
        key_stream = chacha20_block(key, counter + j, nonce)    # +j gives a unique counter value for key_stream generation
        block_start = j * 64                                    # find the start point with index number in the plain text
        block_end = block_start + 64                            # find the end point with index number in the plain text
        block = plaintext[block_start:block_end]                # extract the 64 byte block from the text
        print(key_stream, "\n", block)

        encrypted_block = b""                               # Combine each bit of plaintext with,
        for x, y in zip(block, key_stream):                 # the corresponding bit of key-stream,
            encrypted_block += bytes([x ^ y])               # by performing XOR operation.

        encrypted_message += encrypted_block                # keep appending the encrypted block in the variable

    if len(plaintext) % 64 != 0:                            # check and consider the ending part of the text for encryption
        j = block_count                                     # get the remaining or an end block
        key_stream = chacha20_block(key, counter + j, nonce)
        block_start = j * 64                                # start point index number in the last block
        block = plaintext[block_start:]                     # get all the remaining bytes from the last block

        print("2", key_stream, "\n", block)
        remaining_block = b""
        for x, y in zip(block, key_stream):
            remaining_block += bytes([x ^ y])

        encrypted_message += remaining_block[:len(plaintext) % 64]  # append the remaining block with encryption

    return bytes_to_int(encrypted_message)                  # return the list of integers as an output


# 6. =========== user Inputs ============================================================================================

# # key_in = b'\x50' * 32  # 256-bit key_in
# key_in = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
# # nonce_in = b'\x10' * 12  # 96-bit nonce_in
# nonce_in = b'\x00\x00\x00\t\x00\x00\x00J\x00\x00\x00\x00'
# counter_in = 1
# # plaintext_in = b'Your plaintext message goes here.'
# plaintext_in = b'Ladies and Gentlemen of the class of \'99: If I could offer you only one tip for the future, sunscreen would be it.'
#
#
# encrypted_result = chacha20_encrypt(key_in, counter_in, nonce_in, plaintext_in)
# # print(encrypted_result.hex())
# print(encrypted_result)
