"""
The RC4 (Rivest Cipher 4) algorithm is a symmetric stream cipher. it operates on each byte using the provided key length,
for encryption and decryption.

The secret key can be provided using the secrets or os library to gain more reliable entropy.
Here, S is the state vector, and K is the key vector.

The input key length can be from 1 to 256 bytes (8 to 2048 bits), the suggested key length is minimum 40 bytes according to wiki
The plain text can be any length as it

This algorithm is referenced from the wiki and the geeksforgeeks.
"""


# 0.0 =========== User Inputs ==========================================================================================
byte_key = b'secret key for encryption!'
plain_text = b'This algorithm is used for encrypt and decrypt the message using the same secret key!'


# 1.0 =========== RC4 DRBG class ======================================================================================


class RC4:

    # 1.1 ==============================================================================================================
    def __init__(self, key):                                # Initialize the state vector S and the key K

        self.S = list(range(256))                           # S contains values from 0 to 255

        self.K = []                                         # K is filled with repeated key values
        for i in range(256):
            index = i % len(key)
            self.K.append(key[index])

        self.i = 0                                          # i-is the index for S
        self.j = 0                                          # j is the index for K

    # 1.2 ==============================================================================================================
    """The state vector (S) is prepared to encrypt or decrypt the data using the provided key in a pseudo random manner 
    in this KSA function"""

    def KSA(self):                                          # Perform the key scheduling algorithm (KSA) to permute S
        for i in range(256):
            self.j = (self.j + self.S[i] + self.K[i]) % 256         # j is updated based on S, K and i
            self.S[i], self.S[self.j] = self.S[self.j], self.S[i]   # swap S[i] and S[j]

    # 1.3 ==============================================================================================================

    def generate(self):                                     # PRGA - Generate a key-stream byte using the pseudo-random generation algorithm (PRGA)
        self.i = (self.i + 1) % 256                         # increment i by 1 modulo 256
        self.j = (self.j + self.S[self.i]) % 256            # update j based on S and i
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]  # swap S[i] and S[j]
        t = (self.S[self.i] + self.S[self.j]) % 256         # compute t as the sum of S[i] and S[j] modulo 256
        return self.S[t] ^ self.S[self.i]                   # return the key-stream byte from S XORed with S[i]

    # 1.4 ==============================================================================================================

    def crypt(self, message):                               # Encrypt or decrypt a message by XORing it with the key-stream
        cipher = []                                         # initialize an empty list to store the cipher
        self.KSA()                                          # call the KSA method to permute S
        for byte in message:                                # for each byte in the message
            keystream_byte = self.generate()                # generate a key-stream byte using PRGA
            cipher_byte = keystream_byte ^ byte             # XOR the key-stream byte with the message byte
            cipher.append(cipher_byte)                      # append the cipher byte to the cipher list
        return bytes(cipher)                                # return the cipher as bytes


# 2.0 =========== Convert The Data Types to Store ======================================================================

def b2i(data):                                              # convert bytes to a list of integers
    binary_string = ''                                      # Convert each byte to a binary string and join them
    for byte in data:
        binary_string += bin(byte)[2:].zfill(8)             # convert each byte to binary of 8 characters and append
    # integer_list = [int(bit) for bit in binary_string]      # Convert the binary string to a list of integers
    return binary_string


# 3.0 =========== call the Class and its function ======================================================================

drbg_1 = RC4(byte_key)                                      # Create an RC4 object with the user selected key
cipher_text = drbg_1.crypt(plain_text)                      # Encrypt the provided plain text using the secret key

drbg_2 = RC4(byte_key)                                      # Create an RC4 object with the user selected key
plain = drbg_2.crypt(cipher_text)                           # Decrypt the cypher text using the secret key

print(cipher_text, "\n\n", b2i(cipher_text), "\n")          # Print the cipher text
print(plain)                                                # print the decrypted text from cypher text
