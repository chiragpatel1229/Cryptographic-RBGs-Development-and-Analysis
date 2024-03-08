from qiskit_ibm_provider import IBMProvider
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute
import sympy
import secrets
import threading
import hashlib

'''
-> This algorithm takes carefully consider quantum random bits using hash.sha-3 function to produce a seed value 
    for the bit generation process using the blum blum shub method.
    
-> For the quick and convenient process of bit generation and analysis, currently a simulator is being used as a
    Backend provider.    
    
-> IBM-backend can be changed in section 1.4 and the user API token should be loaded in the separate file name 
    'my_API_token.txt' for the convenience. Also the Backend provider can be a real quantum device check section 1.4.
    
-> This algorithm does not utilise the quantum generated bits directly, instead it performs hashing on each bit first
    and then add them to the entropy pool for the further bit production.
'''
# 0.0  User Inputs =====================================================================================================

number_of_bits = 256        # number of bits to generate

number_of_bytes = 0         # number of byts to generate

# 1.0 Quantum random bit generator =====================================================================================


class QuantumRNG(object):

    # 1.1 Initiate the quantum class ===================================================================================

    def __init__(self, Token_file_path):

        # https://docs.python.org/3/library/secrets.html
        # Using secure source of randomness provided by the operating system

        self.Token_file_path = Token_file_path
        self.sec_ = secrets.SystemRandom()                 # create an instance of the system random class
        sel_int = self.sec_.randrange(5 * 10 ** 100, 7 * 10 ** 100)   # select an integer between given range (a, b-1)
        self.entropy = "{0:b}".format(sel_int)             # converted the selected integer into the binary format
        self.seed = secrets.randbelow(3 * 10 ** 100)       # Generate a random number from 0 to the given number (0, n-1)

        x = self.sec_.randrange(7 * 10 ** 100, 11 * 10 ** 100)  # Get the first random int to create a random prime
        y = self.sec_.randrange(7 * 10 ** 100, 11 * 10 ** 100)  # Get the second random int to create a random prime
        # self._update()                                        # just to show that the quantum bits are being added to the entropy pool

        self.p = self.next_prime(x)                        # set the prime number for p based on the x value
        self.q = self.next_prime(y)                        # set the prime number for q based on the y value

        self.reseed_count = 0                              # set the reseed interval counter to 0
        self.reseed_interval = 10 ** 3                     # reseed the seed bits at least on (10**7)

    # 1.2  A function to find the next possible prime number to generate the modulus ===================================

    def next_prime(self, Original_prime):
        next_usable_prime = sympy.nextprime(Original_prime)  # get the very first possible next prime number
        while next_usable_prime % 4 != 3:                    # very important to check the selected prime must be congruent to 3 modulo 4
            next_usable_prime = sympy.nextprime(next_usable_prime)  # keep trying until the condition is satisfied
        if self.seed % next_usable_prime == 0:               # check for the modulus of seed and next usable prime, find another prime number
            next_usable_prime = self.next_prime(next_usable_prime + 1)
        return next_usable_prime

    # 1.3 The update function will be called automatically while refilling the entropy pool is required ================

    def _update(self):
        print("[i] The entropy and the seed value is being update.\n")

        # 1.3.1 It is the quickest way to provide reliable entropy in case of requirement ==============================

        if len(self.entropy) < 512:                     # use the system entropy bcz the generating quantum bits takes time
            sel_int = self.sec_.randrange(2 * 10 ** 100, 3 * 10 ** 100)     # select a random number between the given range
            local_bits = "{0:b}".format(sel_int)        # convert the random number in to its binary format
            self.entropy += local_bits                  # add this binary format to the current entropy pool
            print(f"[!] Added {len(local_bits)} bits from local entropy pool.\n")   # inform about the added bits

        # 1.3.2 Call the quantum bit generation process in a separate thread to keep this algorithm stress free ========

        if len(self.entropy) < 1025:                    # our major focus is on adding quantum bits to the seed value
            quantum_bits = threading.Thread(target=self.Refill_entropy, name='GenCj bitsP')   # using thread as this process takes unexpected time
            quantum_bits.start()                        # just give a start to the separate thread

        # 1.3.3 To keep the quality of the bit generation remove the used entropy bits form the pool ===================

        self.seed += int(self.entropy[:256], 2)     # convert only first 256 bits to integer and make addition with the seed value to update it
        self.entropy = self.entropy[256:]           # remove recently used bits from the entropy pool...
        self.reseed_count = 0                       # reset the counter

        print(f"[!] Remaining bits in entropy pool: {len(self.entropy)} \n")

        return

    # 1.4 A quantum bit generator ======================================================================================

    def Quantum_circuit(self):

        # 1.4.1 Get the API token and activate the provider and set the backend for generate the bits ==================
        with open(self.Token_file_path, 'r') as API_token:      # open the file in read mode
            My_token = API_token.read().strip()                 # read the token
        # My_token = ""                                         # Comment out the text file reader and add your personal token here
        provider = IBMProvider(str(My_token))                   # set the ibm provider using the token

        backend = provider.get_backend('simulator_mps')         # set the backend that is fast and can provide more qubits

        # 1.4.2 Design the quantum circuit to generate the bits ========================================================
        quantum_R = QuantumRegister(80)                         # max 100 qubits but used only 80 here for better response
        class_R = ClassicalRegister(80)                         # it should be the same as the qubits
        circuit = QuantumCircuit(quantum_R, class_R)
        circuit.h(quantum_R)                                    # apply hadamard gate
        circuit.measure(quantum_R, class_R)

        # 1.4.3 Execute the circuit and wait for the final state to be completed or performed ==========================
        job = execute(circuit, backend, shots=150)              # execute the designed circuit

        job.wait_for_final_state()          # it will keep the connection with the server open and wait until the process is done

        # 1.4.4 Collect the measured bits from the quantum bit generation process ======================================
        bits_seq_1, bits_seq_2, bits_seq_3 = "", "", ""     # buffer to store the quantum generated random bits

        for i in range(3):
            result = job.result()                           # returns a dictionary from an object
            counts = result.get_counts()                    # number of times - unique binary sequences
            bits_seq_1 += list(counts.keys())[0]            # only selecting first 3 keys from the directory
            bits_seq_2 += list(counts.keys())[1]
            bits_seq_3 += list(counts.keys())[2]

        # 1.4.5 Add up all the collected bits in a single string =======================================================
        bits = bits_seq_1 + bits_seq_2 + bits_seq_3         # prepare the final binary string for the entropy pool

        return bits                                         # return the binary string

    # 1.5 This function is to refill the entropy pool with new hashed bits =============================================

    def Refill_entropy(self):
        print("[i] runningC the IBM-Quantum process to generate true random bits.\n")

        q_bits = self.Quantum_circuit()             # get the quantum generated random bit string
        current_e_pool = self.entropy               # assign the entropy pool to the new variable
        cjp = hashlib.sha3_256()                    # hash everything to make the most of the quantum

        for i in range(len(q_bits) // 256 + 1):     # loop to hash each quantum bit

            bits2hash = str(current_e_pool + q_bits[i * 256:(i + 1) * 256]).encode('utf-8')     # get chunks of 256 bits
            cjp.update(bits2hash)                   # perform hashing on chunks of 256 bits
            self.entropy += ''.join(format(byte, '08b') for byte in cjp.digest())   # convert the hashed bytes to the binary string and add it to the entropy pool

        cjp.update(str(q_bits + current_e_pool).encode('utf-8'))        # enhance the mixing of these quantum generated bits using all the bits and entire pool
        self.entropy += ''.join(format(byte, '08b') for byte in cjp.digest())

        print(f"[i] Updated the entropy pool with {len(q_bits)} bits from IBMQ.\n"
              f"[i] After hashing the quantum bits, {len(self.entropy)} bits available in the entropy pool.")

        return

    # 1.6 This function is to generate random bits using the unique seed value =========================================

    def ran_bits(self, n_req_bits=64):  # Generate random bits
        M = self.p * self.q             # calculate the modulus of two prime numbers

        if self.reseed_count > self.reseed_interval:  # if the reseed count is reached the interval update the seed value
            self._update()              # update the seed value using the entropy pool

        x = self.seed                   # set the seed to generate the bits based on BBS principal

        bit_string = ""                 # Create a buffer to store the results
        for _ in range(n_req_bits):     # iterate for the requested bits times
            x = pow(x, 2) % M           # perform this operation to generate unique values
            b = x % 2                   # extract 0 or 1 from the unique value
            bit_string += str(b)        # add the binary bits to the buffer

        self.seed = x                   # update the seed value with the new unique number
        self.reseed_count += n_req_bits  # update bits count

        return bit_string               # return a bit string

    # 1.7 This function is to generate Bytes using the Random bit generator function ===================================

    def ran_bytes(self, N=0):

        b = self.ran_bits(n_req_bits=N * 8)     # use the random bits function to generate the requested bytes

        b = b + '0' * (8 - len(b) % 8)          # making sure that the length of the bits is multiple of 8

        int_v = int(b, 2)                       # Convert the bit to an equivalent integer number

        num_bytes = (len(b) + 7) // 8           # Get the required bytes to generate

        b_str = int_v.to_bytes(num_bytes, byteorder='big')  # Convert an integer to byte string using the inbuilt function

        return b_str                            # return the bytes converted from the generated random bits


# 2.0 Execute the Quantum Random Bit Generator class ===================================================================

# Create an instance of QuantumRNG =====================================================================================
quantum_rng = QuantumRNG('API_token.txt')

# Generate random bits =================================================================================================
random_bits = quantum_rng.ran_bits(n_req_bits=number_of_bits)       # This function can be used in a loop for constant bit production
print(f"Generated random bits: {random_bits}")

# Generate random bytes ================================================================================================
if number_of_bytes > 1:
    random_bytes = quantum_rng.ran_bytes(N=number_of_bytes)
    print(f"Generated random bytes: {random_bytes}")
