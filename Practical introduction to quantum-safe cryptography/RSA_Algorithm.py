import random
from sympy import nextprime

'''
-> The RSA (Rivest–Shamir–Adleman) is an Asymmetric cryptography algorithm and a public-key crypto-system. 
1. A client (for example browser) sends its public key to the server and requests some data.
2. The server encrypts the data using the client’s public key and sends the encrypted data.
3. The client receives this data and decrypts it.

-> The message can be encrypted by anyone using the public key, but it can be decrypt by using the privet keys.
-> The security of RSA relies on the practical difficulty of factoring the product of two large prime numbers, 
   the "factoring problem". There are no published methods to defeat the system if a large enough key is used.
'''
# Reference: Paper - METHODS TOWARD ENHANCING RSA ALGORITHM: A SURVEY
#            Paper - Understanding the RSA algorithm


def gcd(a, b):              # Euclidean Algorithm to calculate the greatest common divisor of two numbers
    while b != 0:
        a, b = b, a % b
    return a


# The purpose of multiplicative inverse of e modulo phi is to find thd the value of d. So the number d is when
# multiply with value e and then divide by phi always gives a reminder 1


def mul_inv(e, phi):                     # Extended Euclidean Algorithm to find the multiplicative inverse of two numbers
    d = 0                                # Initialize the basic variables for the further calculation
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi                       # Make a copy of phi, used to perform the division

    while e > 0:                         # While e is greater than 0, condition is true keep iterating
        temp1 = temp_phi // e            # Keep updating the variables
        temp2 = temp_phi - temp1 * e     # until the value of e becomes 0
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:                    # If temp_phi is 1 that means e and phi are co-prime to teach other
        return d + phi                   # Return the multiplicative inverse of e mod phi


def find_next_prime(Original_prime):                        # get the next possible prime number.
    next_usable_prime = nextprime(Original_prime)           # get the very first possible next prime number
    while next_usable_prime % 4 != 3:                       # very important to check the selected prime must be congruent to 3 modulo 4
        next_usable_prime = nextprime(next_usable_prime)    # keep trying until the condition is satisfied
    return next_usable_prime


def generate_keypair(x, y):                 # Generate key pairs for encryption and decryption

    x1 = find_next_prime(x)
    y1 = find_next_prime(y)

    n = x1 * y1                             # n = pq

    phi = (x1 - 1) * (y1 - 1)               # Phi is the totient of n

    e = random.randrange(1, phi)            # Choose an integer e such that e and phi(n) are co-prime

    g = gcd(e, phi)                         # Use Euclid's Algorithm to verify that e and phi(n) are co-prime
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = mul_inv(e, phi)  # Use Extended Euclid's Algorithm to generate the private key
    # print('e:', e, 'd:', d, 'n:', n)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return (e, n), (d, n)


def encrypt(pk, plaintext):
    # encrypt message M using public key (e, n): C = M^e (mod n)

    key, n = pk                             # Unpack the key into it's components

    cipher = []

    for char in plaintext:
        # Convert each letter in the plaintext to numbers based on the character using a^b mod m
        char_value = ord(char)
        encrypted_char = pow(char_value, key, n)    # Syntax: pow(x, y, mod) = (i.e.: x**y % mod)
        cipher.append(encrypted_char)

    return cipher                           # Return the array of bytes


def decrypt(pk, ciphertext):

    key, n = pk                             # Unpack the key into its components

    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = []

    for char in ciphertext:
        # Generate the plaintext based on the ciphertext and key using a^b mod m
        decrypted_char = chr(pow(char, key, n))
        plain.append(decrypted_char)

    return ''.join(plain)                   # Return the array of bytes as a string


# Generate public and private keys using two prime numbers
p = 13000
q = 1750
public, private = generate_keypair(p, q)

# Public and private keys
print("Public Key: ", public)
print("\nPrivate Key: ", private)

# Encrypt a message
message = "Hello, World! This is a random message for testing purpose only!"
encrypted_msg = encrypt(public, message)
print("\n\nEncrypted Message: ", ''.join([format(i, '08b') for i in encrypted_msg]))

# Decrypt the message
decrypted_msg = decrypt(private, encrypted_msg)
print("\n\nDecrypted Message: ", decrypted_msg)
