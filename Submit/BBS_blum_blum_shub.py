from random import randint
import secrets
import sympy
from math import gcd

'''This is a Blum Blum Shub Algorithm to generate pseudo random numbers using the prime numbers.

-> This algorithm generates a list of prime numbers between 0 to 1000, and selects random index number from the list to 
   assign it to the p and q to generate the random sequence. 
 
-> This algorithm requires the seed and modulus as a co-prime to each other, because it helps to generate the 
   uniformly distributed and secure random sequence.'''

# 0.0 =========== User Inputs ==========================================================================================

seq_length = 1024                     # Set the desired length of the sequence


# 1.0 =========== Blum Blum Shub Class =================================================================================
class BBS:

    # 1.1 =========== Define the initial variable and initiate them ====================================================
    n = 0                               # The product of p and q
    x = 0
    seed_value = 0                      # The initial value for the generator
    generatedValues = []                # The list of generated values

    # 1.2 =========== Initialize the class =============================================================================
    def __init__(self, p, q):

        # Set the values of p and q
        self.p = p
        self.q = q

        if self.p == self.q:            # Check if p and q are different
            raise ValueError('P and Q can not be equal!!!')     # If not, print an error message

        elif self.p > 0 and self.q > 0:  # If p and q are valid, it allows to set the modulus and the seed value
            self.set_N()
            self.set_Seed()

        else:
            raise ValueError("The values of p and q are not valid !!!")

    # 1.3 =========== find the next usable prime that is congruent to 3 modulo 4 =======================================

    @staticmethod
    def find_next_prime(Original_prime):
        next_usable_prime = sympy.nextprime(Original_prime)         # get the very first possible next prime number
        while next_usable_prime % 4 != 3:                           # very important to check the selected prime must be congruent to 3 modulo 4
            next_usable_prime = sympy.nextprime(next_usable_prime)  # keep trying until the condition is satisfied
        return next_usable_prime                                    # return the perfect prime number for the BBS output

    # 1.4 =========== Set the Modulus as a product of two large prime numbers ==========================================
    '''The security of Blum Blum Shub algorithm is depend on the Modulus n which is hard to factorise and find the initial
    values of p and q.'''

    def set_N(self):
        self.p = self.find_next_prime(self.p)
        self.q = self.find_next_prime(self.q)

        self.n = self.p * self.q        # set the prime numbers product value to the modulus n

    # 1.5 =========== SET THE SEED VALUE ===============================================================================
    def set_Seed(self):
        # check the greatest common divisor of the modulus and the seed, which should not be 1.
        # This algorithm requires the seed and modulus as a co-prime to each other, because it helps to generate the
        # uniformly distributed and secure random sequence.
        while gcd(self.n, self.seed_value) != 1 and self.seed_value > 1:

            self.seed_value = randint(0, self.n - 1)   # Generate a seed using the random number between 0 and n-1

        self.x = self.seed_value        # Assign the seed value to the x

    # 1.6 =========== GENERATE A UNIQUE VALUE TO PROVIDE RANDOMNESS ====================================================
    def generate_Value(self):

        while gcd(self.n, self.x) != 1:       # check the greatest common divisor of the modulus and the seed, which should not be 1.
            self.x = secrets.randbelow(self.n)  # Generate a random number between 0 and n

        self.x = pow(self.x, 2, self.n)

        return self.x                       # Return the square of x with modulo n

    # 1.7 =========== Generate the requested bits ======================================================================
    def generateBits(self, Req_Length):

        bitsArray = []                      # create an empty buffer to store the sequence

        Req_Length += 1                     # Increment the length amount by one

        for i in range(Req_Length):         # Loop for the given amount

            generatedValue = self.generate_Value()  # Generate a value using the private method
            self.generatedValues.append(generatedValue)  # Append it to the list of generated values

            if generatedValue % 2 == 0:  # Check if the value is even or odd
                bitsArray.append(0)      # If even, append 0 to the list of bits

            else:
                bitsArray.append(1)      # If odd, append 1 to the list of bits

        return bitsArray                 # Return the list of bits


# 2.0 =========== Check the provided number is prime or not ============================================================
def is_prime(C_num):                      # check the number is prime or not

    if C_num < 2:                         # Initially the Numbers less than 2 are not prime
        return False

    for i in range(2, int(C_num ** 0.5) + 1):   # Iterate from 2 to the square root of the number + 1
        if C_num % i == 0:                # Check the given number is divisible by current integer in the selected range
            return False                  # if it is divisible then return false

    return True                           # if there is no divisor of the given number return True


# 3.0 =========== Generate prime numbers in the given range a to b =====================================================
def generate_primes(a_val, b_val):

    if b_val < 1000:                        # set the minimum range at 1000 to generate the primes
        b_val = 1000
    primes = []                         # create an empty buffer to store the prime numbers
    for num in range(a_val, b_val + 1):         # iterate between the provided range
        if is_prime(num):               # check the current number is prime or not
            primes.append(num)          # if the number is prime then add it to the list

    return primes                       # return the list of prime numbers


# 4.0 =========== Generate the initial values for p and q ==============================================================

prime_list = generate_primes(0, 1000)  # Generate and store prime numbers between 0 and 1000 in a list

list_len = len(prime_list)-1            # find the total length of prime numbers list

P_ind = randint(0, list_len)            # select a random index number for p value
Q_ind = randint(0, list_len)            # select a random index number for q value

while P_ind == Q_ind:                   # The value of p and q must be different
    index_q = randint(0, list_len)

P_bit = prime_list[P_ind]               # assign the random prime number from the list to the p value
Q_bit = prime_list[Q_ind]               # assign the random prime number from the list to the q value


# 5.0 =========== call the Class and its function ======================================================================

bbs = BBS(P_bit, Q_bit)
bits = bbs.generateBits(seq_length)

print(bits)
print("Number of Zeros: ", bits.count(0), "\nNumber of Ones: ", bits.count(1))
