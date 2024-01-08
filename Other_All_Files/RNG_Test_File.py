# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes


import hashlib
import os

seed = os.urandom(12)
hash_256 = hashlib.sha256(seed)
# print(len(hash_256.digest()))
print(hash_256.digest())  # To print the hexadecimal representation of the hash

# To update the hash with bytes, you need to provide bytes
bytes_seq = os.urandom(1)  # Use a bytes literal
hash_256.update(bytes_seq)
print(len(hash_256.hexdigest()))
print(hash_256.digest())
# print(hash_256.hexdigest())


bin_seq = ''
binary_byte = ''.join(format(x, '08b') for x in bytes_seq)  # Convert each byte into binary with 8 bits
bin_seq += binary_byte

print(bin_seq)



# # Initialize seed and nonce_in (both 128 bits)
# seed = get_random_bytes(16)
# nonce_in = get_random_bytes(16)
#
# # Initialize counter (128 bits)
# counter = 0
#
# # Initialize an empty byte array for the output
# output = bytearray()
#
# # Number of bits to generate
# num_bits = 1024
#
# # Create an AES cipher object with the derived key_in
# key_in = HMAC_SHA256(seed, nonce_in)  # You need to implement HMAC-SHA256
# cipher = AES.new(key_in, AES.MODE_CTR, nonce_in=nonce_in)
#
# while len(output) < num_bits:
#     # Encrypt the counter value and append it to the output
#     encrypted_block = cipher.encrypt(counter.to_bytes(16, byteorder='big'))
#     output.extend(encrypted_block)
#
#     # Increment the counter
#     counter += 1
#
# # Extract the first num_bits from the generated output
# random_sequence = output[:num_bits]
#
# # Convert the random bytes to a binary string
# binary_sequence = ''.join(f'{byte:08b}' for byte in random_sequence)
#
# # Print or use the binary_sequence as needed
# print(binary_sequence)

# import ctypes
# import random
#
#
# def generate_random_binary_sequence(length):
#     # Calculate the number of bytes needed to represent the given bit length
#     num_bytes = (length + 7) // 8
#     print("num_bytes", num_bytes)
#
#     # Create a buffer to hold the random bytes.
#     buf = ctypes.create_string_buffer(num_bytes)
#     print("buf", buf)
#
#     # Call CryptGenRandom to fill the buffer with random bytes.
#     ctypes.windll.advapi32.CryptGenRandom(num_bytes, buf)
#     print(f"Buffer after CryptGenRandom: {buf.raw}")
#
#     # Generate a random sequence of zeros and ones by flipping individual bits.
#     random_sequence = ''.join(format(byte ^ random.randint(0, 255), '08b') for byte in buf.raw)
#
#     # Trim the binary sequence to the desired length.
#     random_sequence = random_sequence[:length]
#     binary_list = [int(bit) for bit in random_sequence]
#
#     return binary_list
#
#
# # Generate a random binary sequence of 1024 bits.
# random_binary_sequence = generate_random_binary_sequence(1024)
#
# # Print the random binary sequence.
# print(random_binary_sequence)
