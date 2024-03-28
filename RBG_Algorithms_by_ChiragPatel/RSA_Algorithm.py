import random
from sympy import nextprime
import secrets
'''
-> The RSA (Rivest–Shamir–Adleman) is an Asymmetric cryptography algorithm and a public-key crypto-system. 
1. A client (for example browser) sends its public key to the server and requests some data.
2. The server encrypts the data using the client’s public key and sends the encrypted data.
3. The client receives this data and decrypts it using private key.

-> The message can be encrypted by anyone using the public key, but it can be decrypt by using the privet keys.
-> The security of RSA relies on the practical difficulty of factoring the product of two large prime numbers, 
   the "factoring problem". There are no published methods to defeat the system if a large enough key is used.
   
-> e = private encryption key, d = private decryption key, n = common or public key
-> encrypt the plain message M using public key (e, n): C = M^e (mod n)
-> decrypt the cipher text C using private key (d, n): M' = C^d (mod n)
'''
# Reference: Paper - METHODS TOWARD ENHANCING RSA ALGORITHM: A SURVEY
#            Paper - Understanding the RSA algorithm (https://doi.org/10.1145/nnnnnnn.nnnnnnn)

# 0.0 =========== User Inputs ==========================================================================================
rnd_p = 700
rnd_q = 170
# message = "Hello, World! This is a random message for testing purpose only!1111"
message = "52DUb0izihzpIyehX8aKDpAuM2eT07WpYhcXxZrY40WcvYGpkLbSMJ58ffgadfgsdfgsfgcLWSdwHwWwDaKO7G0z9EwpeqfnVvbyOQ7jcuUQlSdYQm0estX4mMlHa3j3SHRgxsksZKZI7DC1KANyPle4KJujbNthh0tVYEqYFb0mppHvEvTamE8guLmFNmhxuZTeQIywsVJVCAeSdgKvX2YH8a7Cp8HP4t6YvktZzd7E6hsFkB3cuDJTiHN82RbaXfdh6exsdf"


# 1.0 =========== Function to find the common divisor ==================================================================
def gcd(a_value, b_value):              # Euclidean Algorithm to calculate the greatest common divisor of two numbers
    while b_value != 0:
        a_value, b_value = b_value, a_value % b_value
    return a_value


# 2.0 =========== find value d using the multiplicative inverse using Euclidean Algorithm ==============================

# The purpose of multiplicative inverse of e and phi is to find thd the value of d. So the number d is when
# multiply with value e and then divide by phi always gives a reminder 1: d * e / phi = 1

def mul_inv(encrypt_val, phi):                 # Extended Euclidean Algorithm to find the multiplicative inverse of two numbers
    d_Value = 0                                # Initialize the basic variables for the further calculation
    x1_val = 0
    x2_val = 1
    y1_val = 1
    temp_phi = phi                            # Make a copy of phi, used to perform the division

    while encrypt_val > 0:                    # While encrypt_val is greater than 0, condition is true keep iterating
        temp1 = temp_phi // encrypt_val       # Keep updating the variables
        temp2 = temp_phi - temp1 * encrypt_val     # until the value of encrypt_val becomes 0
        temp_phi = encrypt_val
        encrypt_val = temp2

        x = x2_val - temp1 * x1_val
        y = d_Value - temp1 * y1_val

        x2_val = x1_val
        x1_val = x
        d_Value = y1_val                # Update the value of d with the new one
        y1_val = y

    if temp_phi == 1:                   # If temp_phi is 1 that means e and phi are co-prime to teach other
        return d_Value + phi            # Return the multiplicative inverse of e mod phi


# 3.0 =========== Function to find the next usable prime number ========================================================
def find_next_prime(Original_prime):                        # get the next possible prime number.
    next_usable_prime = nextprime(Original_prime)           # get the very first possible next prime number
    while next_usable_prime % 4 != 3:                       # very important to check the selected prime must be congruent to 3 modulo 4
        next_usable_prime = nextprime(next_usable_prime)    # keep trying until the condition is satisfied
    return next_usable_prime


# 4.0 =========== Generate key pairs (e, d, n) for encryption and decryption ===========================================
def generate_keypair(chi_x, rag_y):                                     # Generate key pairs for encryption and decryption

    First_prime = find_next_prime(chi_x)
    Second_prime = find_next_prime(rag_y)

    Modulus_n = First_prime * Second_prime                     # n = pq

    phi = (First_prime - 1) * (Second_prime - 1)               # Phi is the totient of n

    encryption_key = random.randrange(1, phi)                   # Choose an integer e such that encryption_key and phi(n) are co-prime
    Co_prime_d = gcd(encryption_key, phi)                       # Use Euclid's Algorithm to verify that encryption_key and phi(n) are co-prime
    while Co_prime_d != 1:
        encryption_key = random.randrange(1, phi)
        Co_prime_d = gcd(encryption_key, phi)

    decryption_key = mul_inv(encryption_key, phi)  # Use Extended Euclid's Algorithm to generate the private key
    # print('encryption_key:', encryption_key, 'decryption_key:', decryption_key, 'Modulus_n:', Modulus_n)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return (encryption_key, Modulus_n), (decryption_key, Modulus_n)


# 5.0 =========== implementation of RSA encryption method ==============================================================
def encrypt(public_key, plaintext):
    # encrypt message M using public key (e, n): C = M^e (mod n)

    pub_key, mod_n = public_key                             # Unpack the key into it's components

    cipher_text = []

    for char in plaintext:
        # Convert each letter in the plaintext to numbers based on the character using a^b mod m
        char_value = ord(char)
        encrypted_char = pow(char_value, pub_key, mod_n)    # Syntax: pow(x, y, mod) = (i.e.: x**y % mod)
        cipher_text.append(encrypted_char)

    return cipher_text                                       # Return the array of bytes


# 6.0 =========== implementation of RSA decryption method ==============================================================
def decrypt(private_key, ciphertext):

    pri_key, mod_n = private_key                        # Unpack the key into its components

    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain_text = []

    for char in ciphertext:
        # Generate the plaintext based on the ciphertext and key using a^b mod m
        decrypted_char = chr(pow(char, pri_key, mod_n))
        plain_text.append(decrypted_char)

    return ''.join(plain_text)                               # Return the array of bytes as a string


# 7.0 =========== Algorithm execution and calling functions ============================================================
# Generate public and private keys using two prime numbers
public, private = generate_keypair(rnd_p, rnd_q)

# Public and private keys
print("Public Key: ", public)
print("\nPrivate Key: ", private)

# Encrypt a message
encrypted_msg = encrypt(public, message)
cipher_text = ''.join([format(i, '08b') for i in encrypted_msg])
print("\n\nEncrypted Message: ", len(cipher_text))

# Decrypt the message
decrypted_msg = decrypt(private, encrypted_msg)
print("\n\nDecrypted Message: ", decrypted_msg)

# 8.0 =========== end ==================================================================================================
# sec_ = secrets.SystemRandom()
# # Open a file to write
# with open("RSA_algorithm.txt", "w") as file, open("RSA_keys.txt", "w") as key_file:
#     for _ in range(100):
#         rnd_p = sec_.randrange(100 , 1000)
#         rnd_q = sec_.randrange(100 , 1000)
#         public, private = generate_keypair(rnd_p, rnd_q)
#         encrypted_msg = encrypt(public, message)
#         cipher_text = ''.join([format(i, '08b') for i in encrypted_msg])
#
#         file.write(cipher_text[:4000] + '\n')
#         key_file.write(str(public) + str(private) + '\n')  # Store the drbg_1 output
#
# print("Files are ready!")

