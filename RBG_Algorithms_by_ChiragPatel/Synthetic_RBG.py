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

number_of_bits = 5000        # number of bits to generate

# 1.0 Quantum random bit generator =====================================================================================


class SyntheticRNG(object):

    # 1.1 Initiate the quantum class ===================================================================================

    def __init__(self, Token_file_path):

        # https://docs.python.org/3/library/secrets.html
        # Using secure source of randomness provided by the operating system

        self.reseed_count = 0  # set the reseed interval counter to 0
        self.reseed_interval = 2048  # reseed entropy pool based on the requirements

        self.Token_file_path = Token_file_path
        self.sec_ = secrets.SystemRandom()                 # create an instance of the system random class

        sel_int = self.sec_.randrange(5 * 10 ** 1000, 7 * 10 ** 10000)   # select an integer between given range (a, b-1)
        self.entropy = "{0:b}".format(sel_int)             # converted the selected integer into the binary format

        length = len(str(self.entropy))
        print("Length of the entropy:", length)

        x = self.sec_.randrange(17 * 10 ** 100, 31 * 10 ** 100)  # Get the first random int to create a random prime
        y = self.sec_.randrange(17 * 10 ** 100, 31 * 10 ** 100)  # Get the second random int to create a random prime
        # self._update()                                         # just to show that the quantum bits are being added to the entropy pool

        self.p = self.next_prime(x)                        # set the prime number for p based on the x value
        self.q = self.next_prime(y)                        # set the prime number for q based on the y value

        length = len(str(self.p))
        print("Length of the large integer P:", length)
        length = len(str(self.q))
        print("Length of the large integer Q:", length)

        self.seed = secrets.randbelow(7 * 10 ** 100)        # Generate a random number from 0 to the given number (0, n-1)


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
        # print("[i] Update: The entropy and the seed value is being updated.\n")

        # 1.3.1 It is the quickest way to provide reliable entropy in case of requirement ==============================

        if len(self.entropy) < 1024:                     # use the system entropy bcz the generating quantum bits takes time
            sel_int = self.sec_.randrange(2 * 10 ** 1000, 5 * 10 ** 1000)     # select a random number between the given range
            sel_int = sympy.nextprime(sel_int)
            local_bits = "{0:b}".format(sel_int)        # convert the random number in to its binary format
            self.entropy += local_bits                  # add this binary format to the current entropy pool
            # print(f"[ii] Update: Added {len(local_bits)} bits from local entropy pool.\n")   # inform about the added bits

        # 1.3.2 Call the quantum bit generation process in a separate thread to keep this algorithm stress free ========

        if len(self.entropy) < 1025:                    # our major focus is on adding quantum bits to the seed value
            quantum_bits = threading.Thread(target=self.Refill_entropy, name='GenCj bitsP')   # using thread as this process takes unexpected time
            quantum_bits.start()                        # just give a start to the separate thread

        # 1.3.3 To keep the quality of the bit generation remove the used entropy bits form the pool ===================

        self.seed += int(self.entropy[:256], 2)     # convert only first 256 bits to integer and make addition with the seed value to update it
        self.entropy = self.entropy[256:]           # remove recently used bits from the entropy pool...
        self.reseed_count = 0                       # reset the counter

        # print(f"[iii] Update: Remaining bits in entropy pool: {len(self.entropy)} \n")

        return


    # 1.4 This function is to refill the entropy pool with new hashed bits =============================================

    def Refill_entropy(self):
        # print("[i] Entropy Refill process is started!\n")

        q_bits = self.Quantum_circuit()             # get the quantum generated random bit string
        # print(f"[ii] Received initial {len(q_bits)} bits from a quantum circuit!\n")
        current_e_pool = self.entropy               # assign the entropy pool to the new variable
        cjp = hashlib.sha3_256()                    # hash everything to make the most of the quantum

        for i in range(len(q_bits) // 256 + 1):  # loop to hash each quantum bit

            bits2hash = str(current_e_pool + q_bits[i * 256:(i + 1) * 256]).encode('utf-8')  # get chunks of 256 bits
            cjp.update(bits2hash)  # perform hashing on chunks of 256 bits

            # convert the hashed bytes to the binary string and add it to the entropy pool =============================
            b_str = []
            for byte in cjp.digest():               # convert the digest to the binary string
                b_2b = format(byte, '08b')
                b_str.append(b_2b)
            self.entropy += ''.join(b_str)

        # enhance the mixing of these quantum generated bits using all the bits and entire pool ========================
        C_input = str(q_bits + current_e_pool).encode('utf-8')
        cjp.update(C_input)                         # create a hashed object
        m_bytes = []                                # create a buffer to store the mixed bytes
        for byte in cjp.digest():
            b2b = format(byte, '08b')               # Convert each byte to binary
            m_bytes.append(b2b)

        # update and refill the entropy with the binary bits
        self.entropy += ''.join(m_bytes)

        # print(f"[iii] Refill: Total of {len(self.entropy)} bits available in the entropy pool.")
        # print("[i] Entropy pool is Refilled!\n")


    # 1.5 A quantum bit generator ======================================================================================

    def Quantum_circuit(self):

        # 1.5.1 Get the API token and activate the provider and set the backend for generate the bits ==================
        with open(self.Token_file_path, 'r') as API_token:      # open the file in read mode
            My_token = API_token.read().strip()                 # read the token
        # My_token = ""                                         # Comment out the text file reader and add your personal token here
        provider = IBMProvider(str(My_token))                   # set the ibm provider using the token

        backend = provider.get_backend('simulator_mps')         # set the backend that is fast and can provide more qubits
        # print("[ii] Quantum circuit: Provider and Backend is ready!\n")

        # 1.5.2 Design the quantum circuit to generate the bits ========================================================
        quantum_R = QuantumRegister(80)                         # max 100 qubits but used only 80 here for better response
        class_R = ClassicalRegister(80)                         # it should be the same as the qubits
        circuit = QuantumCircuit(quantum_R, class_R)
        circuit.h(quantum_R)                                    # apply hadamard gate
        circuit.measure(quantum_R, class_R)
        # print("[i] Quantum circuit is executed!\n")

        # 1.5.3 Collect the measured bits from the quantum bit generation process ======================================
        key_1, key_2, key_3, key_4, key_5 = "", "", "", "", ""     # buffer to store the quantum generated random bits

        for i in range(3):
            # 1.4.4 Execute the circuit and wait for the final state to be completed or performed ==========================
            job = execute(circuit, backend, shots=10)       # execute the designed circuit

            job.wait_for_final_state()  # it will keep the connection with the server open and wait until the process is done
            result = job.result()                           # returns a dictionary from an object
            counts = result.get_counts()                    # number of times - unique binary sequences
            keys = list(counts.keys())
            if len(keys) >= 5:
                # print(f"[iii] Found enough Keys in {i} iteration!\n")
                key_1 += keys[0]                            # only selecting first 3 keys from the directory
                key_2 += keys[2]
                key_3 += keys[3]
                key_4 += keys[4]
                key_5 += keys[5]

        # 1.5.5 Add up all the collected bits in a single string =======================================================
        bits = key_1 + key_2 + key_3 + key_4 + key_5        # prepare the final binary string for the entropy pool
        # print(f"[iiii] Quantum circuit: {len(bits)} bits generated successfully!\n")

        return bits                                         # return the binary string


    # 1.6 This function is to generate random bits using the unique seed value =========================================

    def Generate(self, n_req_bits=64):  # Generate random bits
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
        self.reseed_count += n_req_bits // 10  # update bits count

        return bit_string               # return a bit string



# 2.0 Execute the Quantum Random Bit Generator class ===================================================================

# Create an instance of SyntheticRNG =====================================================================================
quantum_rng = SyntheticRNG('Synthetic_API_token.txt')

# Generate random bits =================================================================================================
for _ in range(0,1):
    random_bits = quantum_rng.Generate(n_req_bits=number_of_bits)       # This function can be used in a loop for constant bit production
    print(random_bits)

# Open a file to write
# with open("Synthetic_RBG.txt", "w") as file:
#     for _ in range(100):
#         random_bits = quantum_rng.Generate(n_req_bits=number_of_bits)
#         file.write(random_bits + '\n')
#
# print("Files is ready!")