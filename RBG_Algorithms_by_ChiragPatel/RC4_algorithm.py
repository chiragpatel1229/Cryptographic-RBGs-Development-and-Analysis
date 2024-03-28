
"""" 
The RC4 (Rivest Cipher 4) algorithm is a symmetric stream cipher. it operates on each byte using the provided key length,
for encryption and decryption.

The secret key can be provided using the secrets or os library to gain more reliable entropy.

The input key can be any length < 256,
The plain text can be any length.

"""""


# 0.0 =========== User Inputs ==========================================================================================
from os import urandom
# byte_key = urandom(12)
byte_key = b'secret key for encryption!'

# plain_text = b'This algorithm is used for encrypt and decrypt the message using the same secret key!'
plain_text = b'rKr3TsRqG2N6d4hFMqBdG5ddOSUW1dJjnmfrY3LNWpQTLqpftIotUhnPiKqtirfFaqW1quERXBntQAKjUeZwQmk17A34pEQOdEJ70GgdVMVOlZzAqiTzAv6xlqOUKpPnj5crEUWJyD4XPkyEYyPYaiMRC4eFLQb1AIG7lc25WklcVtVCzziU0CcoeXtH8Ox79HWOf5x24GVoJeOBn5qZU8rJ60yJVzjnuRUXgRcHp3TtRZcbict2Hc1uKQcvas95wdsqWEgyiu4TTpnjbKXi6r2kmcQ9hHvjLRMuq8ZPQuNE5BQhcMQ0ECSt8wBO0sXo0RtPOlwTa8qAOxFyRoLOwBkvoArCul6bbxxeF7ImbqDJJJRs2ROPONI4dlRImddAJkpgBiFzPDmwAPCtuy591XtglO9ZtdbO5qdp9XF3BeTzm3UPQEEMBEAJkpNNWoTpTqSVphe5eS0TaTCAKZHoX6BP2nEegzMrP9JMsgiBi2OKyW2iniqJ'
print(len(plain_text))

# 1.0 =========== RC4 DRBG class ======================================================================================
class RC4:

    # 1.1 ===== Initialise the class with the basic variables and values ===============================================
    def __init__(self, key):                      # Initialize the state vector and the key

        if len(key) > 256:
            raise ValueError("Key length should not be more than 256 byts !!!")

        self.State = list(range(256))             # States contains values from 0 to 255

        self.Key = []                             # Key is filled with repeated key values
        for i in range(256):
            index = i % len(key)
            self.Key.append(key[index])

        self.index_s = 0                          # the index for State
        self.index_j = 0                          # the index for Key

    # 1.2 ===== Perform key scheduling on the state and key to update the variable values ==============================
    """The state vector is prepared to encrypt or decrypt the data using the provided key in a pseudo random manner 
    in this KSA function"""

    def KSA(self):                                          # Perform the key scheduling algorithm (KSA) to permute States
        for i in range(256):
            self.index_j = (self.index_j + self.State[i] + self.Key[i]) % 256         # j is updated based on State, Key and i
            self.State[i], self.State[self.index_j] = self.State[self.index_j], self.State[i]     # swap S[i] and S[j]

    # 1.3 ===== Use the PRGA method to generate a single byte for encryption or decryption ===================================

    def generate(self):                                     # PRGA - Generate a key-stream byte using the pseudo-random generation algorithm (PRGA)
        self.index_s = (self.index_s + 1) % 256             # increment i by 1 modulo 256
        self.index_j = (self.index_j + self.State[self.index_s]) % 256          # update j based on State and index
        self.State[self.index_s], self.State[self.index_j] = self.State[self.index_j], self.State[self.index_s]  # swap State[i] and State[j]
        t = (self.State[self.index_s] + self.State[self.index_j]) % 256         # compute t (temporary vector) as the sum of State[i] and State[j] modulo 256
        return self.State[t] ^ self.State[self.index_s]     # return the key-stream byte from State of t XORed with State[i]

    # 1.4 ===== A single function for encryption and decryption of provided data =======================================

    def en_de_crypt(self, message):                         # Encrypt or decrypt a message by XORing it with the key-stream
        cipher = []                                         # initialize an empty list to store the cipher
        self.KSA()                                          # call the KSA method to permute State
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
cipher_text = drbg_1.en_de_crypt(plain_text)  # Encrypt the provided plain text using the secret key

drbg_2 = RC4(byte_key)                                      # Create an RC4 object with the user selected key
plain = drbg_2.en_de_crypt(cipher_text)  # Decrypt the cypher text using the secret key

print("Cipher Text: ", cipher_text, "\n\nBinary Bits: ", b2i(cipher_text), "\n", len(b2i(cipher_text)))          # Print the cipher text
print("Converted Plain text: ", plain)                      # print the decrypted text from cypher text

# Open a file to write
# with open("RC4_algorithm.txt", "w") as file, open("RC4_keys.txt", "w") as key_file:
#     for _ in range(100):
#         key = urandom(24)
#         drbg_1 = RC4(key)
#         cipher_text = drbg_1.en_de_crypt(plain_text)
#         file.write(b2i(cipher_text) + '\n')
#         key_file.write(key.hex() + '\n')
#
# print("Files are ready!")
