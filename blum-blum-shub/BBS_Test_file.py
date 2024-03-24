from random import randint
import secrets
from math import gcd

'''This is a Blum Blum Shub Algorithm to generate pseudo random numbers using the prime numbers.

-> This algorithm generates a list of prime numbers between 0 to 1000, and selects random index number from the list to 
   assign it to the p and q to generate the random sequence. 
 
-> This algorithm requires the seed and modulus as a co-prime to each other, because it helps to generate the 
   uniformly distributed and secure random sequence.'''

# 0.0 =========== User Inputs ==========================================================================================

seq_length = 10000                           # Set the desired length of the sequence


# 1.0 =========== Blum Blum Shub Class =================================================================================
class BBS:

    # 1.1 =========== Define the initial variable and initiate them ====================================================
    n = 0                               # The product of p and q
    seed = 0                            # The initial value for the generator
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

    # 1.3 =========== Set the Modulus as a product of two large prime numbers ==========================================
    '''The security of Blum Blum Shub algorithm is depend on the Modulus n which is hard to factorise and find the initial
    values of p and q.'''

    def set_N(self):
        self.n = self.p * self.q        # set the prime numbers product value to the modulus n

        if self.n == 0:                 # Check if n is zero
            raise ValueError('N is equal to 0 due to P or Q are not prime number!!!')

    # 1.4 =========== SET THE SEED VALUE ===============================================================================
    def set_Seed(self):
        # check the greatest common divisor of the modulus and the seed, which should not be 1.
        # This algorithm requires the seed and modulus as a co-prime to each other, because it helps to generate the
        # uniformly distributed and secure random sequence.
        while gcd(self.n, self.seed) != 1 and self.seed > 1:

            self.seed = secrets.randbelow(self.n)   # Generate a seed using the random number between 0 and n-1

    # 1.5 =========== GENERATE A UNIQUE VALUE TO PROVIDE RANDOMNESS ====================================================
    def generate_Value(self):

        x = self.seed                    # Assign the seed value to the x
        while gcd(self.n, x) != 1:       # check the greatest common divisor of the modulus and the seed, which should not be 1.
            x = secrets.randbelow(self.n)      # Generate a random number between 0 and n

        return pow(x, 2) % self.n        # Return the square of x modulo n

    # 1.6 =========== Generate the requested bits ======================================================================
    def generateBits(self, Length):

        bitsArray = []                  # create an empty buffer to store the sequence

        Length += 1                     # Increment the length amount by one

        for i in range(Length):         # Loop for the given amount

            generatedValue = self.generate_Value()  # Generate a value using the private method
            self.generatedValues.append(generatedValue)  # Append it to the list of generated values

            if generatedValue % 2 == 0:  # Check if the value is even or odd
                bitsArray.append(0)      # If even, append 0 to the list of bits

            else:
                bitsArray.append(1)      # If odd, append 1 to the list of bits

        return bitsArray                 # Return the list of bits


# 2.0 =========== Check the provided number is prime or not ============================================================
def is_prime(num):

    if num < 2:                             # Initially the Numbers less than 2 are not prime
        return False

    for i in range(2, int(num**0.5) + 1):   # Iterate from 2 to the square root of the number + 1
        if num % i == 0:                    # Check the given number is divisible by current integer in the selected range
            return False                    # if it is divisible then return false

    return True                             # if there is no divisor of the given number return True


# 3.0 =========== Generate prime numbers in the given range a to b =====================================================
def generate_primes(a, b):

    primes = []                             # create an empty buffer to store the prime numbers
    for num in range(a, b + 1):             # iterate between the provided range
        if is_prime(num):                   # check the current number is prime or not
            primes.append(num)              # if the number is prime then add it to the list

    return primes                           # return the list of prime numbers


# 4.0 =========== Generate the initial values for p and q ==============================================================

prime_list = generate_primes(0, 1000)   # Generate and store prime numbers between 0 and 1000 in a list

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

# print(bits)
print(''.join(format(num, 'b') for num in bits))

print("Number of Zeros: ", bits.count(0), "\nNumber of Ones: ", bits.count(1))
