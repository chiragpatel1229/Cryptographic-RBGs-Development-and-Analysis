# Cryptography
Random bit Generator Algorithms and RBG test files based on NIST and BSI

# AES - DRBG LOGIC:

The base 16 is selected for the conversion because it is the same as the hexadecimal system, which is a convenient way to represent binary data in a shorter and more readable form. 
Hexadecimal is a number system that uses 16 symbols: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, and F. Each symbol represents a value from 0 to 15 in decimal. 
Each hexadecimal digit corresponds to four binary bits, or a nibble. The int function in Python can convert a string to an integer, given a base as the second argument. 
The base specifies the number system that the string is using. For example, int("FF", 16) converts the hexadecimal string “FF” to the decimal integer 255, and int("1111", 2) 
converts the binary string “1111” to the decimal integer 15.

The code you posted uses the int function with the base 16 to convert the hexadecimal string seed_material[-self.outlen:].hex() to an integer. 
The seed_material is a byte string that contains the seed value for the AES_DRBG class. The [-self.outlen:] slice takes the last 16 bytes of the seed_material, 
which is the initial value of the counter. The hex method converts the byte string to a hexadecimal string. For example, if the last 16 bytes of the seed_material 
are b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10", the hexadecimal string is “0102030405060708090A0B0C0D0E0F10”. The int function with 
the base 16 converts this hexadecimal string to an integer, which is 72340172838076673.

The pyaes.Counter class is a helper class that implements a counter for the AES encryption algorithm in the counter mode of operation (CTR). 
It takes a single argument, which is the initial value of the counter. The counter is a 128-bit (16-byte) integer that is incremented by one after 
each encryption operation, and wraps around to zero when it reaches its maximum value. The counter is concatenated with a nonce to form the input to 
the AES encryption algorithm. The pyaes.Counter class has an increment method that performs the increment operation.

The code you posted creates an instance of the pyaes.Counter class with the initial value of the counter as the argument. 
The initial value of the counter is obtained by converting the last 16 bytes of the seed_material to an integer with the base 16. 
The seed_material is derived from the entropy input and the personalization string in the instantiate method of the AES_DRBG class.