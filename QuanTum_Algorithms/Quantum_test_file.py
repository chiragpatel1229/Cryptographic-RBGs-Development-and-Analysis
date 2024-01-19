# import secrets

# s = secrets.SystemRandom()
# k = secrets.randbelow(5 * 10 ** 100)
# k = sel_int = s.randrange(3 * 10 ** 100, 4 * 10 ** 100)   # select an integer between given range
# qc_entropy_pool = "{0:b}".format(sel_int)      # converted the selected integer into the binary format
# print(k)

with open('my_API_token.txt', 'r') as API_token:
    ibmqx_token = API_token.read().strip()

b = '01001011001110000100011000010110110101000111001101111101110010011001110111010101011001110110111001110110011100011110001000111001'
v = int(b, 2)
# print(v)
# print(ibmqx_token)


def bits_to_bytes(bit_string):
    # Ensure the length of the bit string is a multiple of 8
    bit_string = bit_string.zfill((len(bit_string) + 7) // 8 * 8)

    # Convert the bit string to an integer
    integer_value = int(bit_string, 2)

    # Calculate the number of bytes required
    num_bytes = (len(bit_string) + 7) // 8

    # Convert the integer to a byte string
    byte_string = integer_value.to_bytes(num_bytes, byteorder='big')

    return byte_string

# call the bits_to_bytes method with the bitstring as an argument
bytes_object = bits_to_bytes(b)

# print the bytes object
print(bytes_object)
