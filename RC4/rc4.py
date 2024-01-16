# Define the RC4 class
class RC4:

    def __init__(self, key):                                # Initialize the state vector S and the key K

        self.S = list(range(256))                           # S contains values from 0 to 255

        self.k = []                                         # K is filled with repeated key values
        for i in range(256):
            index = i % len(key)
            self.k.append(key[index])

        self.K = self.k
        self.i = 0                                          # i-is the index for S
        self.j = 0                                          # j is the index for K

    def KSA(self):                                          # Perform the key scheduling algorithm (KSA) to permute S
        for i in range(256):
            self.j = (self.j + self.S[i] + self.K[i]) % 256         # j is updated based on S, K and i
            self.S[i], self.S[self.j] = self.S[self.j], self.S[i]   # swap S[i] and S[j]

    def generate(self):                                     # PRGA - Generate a key-stream byte using the pseudo-random generation algorithm (PRGA)
        self.i = (self.i + 1) % 256                         # increment i by 1 modulo 256
        self.j = (self.j + self.S[self.i]) % 256            # update j based on S and i
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]  # swap S[i] and S[j]
        t = (self.S[self.i] + self.S[self.j]) % 256         # compute t as the sum of S[i] and S[j] modulo 256
        return self.S[t] ^ self.S[self.i]                   # return the key-stream byte from S XORed with S[i]

    def crypt(self, message):                               # Encrypt or decrypt a message by XORing it with the key-stream
        cipher = []                                         # initialize an empty list to store the cipher
        self.KSA()                                          # call the KSA method to permute S
        for byte in message:                                # for each byte in the message
            keystream_byte = self.generate()                # generate a key-stream byte using PRGA
            cipher_byte = keystream_byte ^ byte             # XOR the key-stream byte with the message byte
            cipher.append(cipher_byte)                      # append the cipher byte to the cipher list
        return bytes(cipher)                                # return the cipher as bytes
