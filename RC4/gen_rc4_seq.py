import rc4

# Create an RC4 object with a key
rc = rc4.RC4(b'secret')

# Encrypt a message
message = b'Hello, world!'
# rnd = rc.generate()
# print('rnd', rnd)
cipher = rc.crypt(message)
print(cipher)               # b'\x1c\x0b\x04\x15N\x1a\r\x1fMR\x0e\x1b\x1a'
print(len(cipher))

# Decrypt the cipher
rc1 = rc4.RC4(b'secret')    # create a new RC4 object with the same key
plain = rc1.crypt(cipher)
print(plain)                # b'Hello, world!'
