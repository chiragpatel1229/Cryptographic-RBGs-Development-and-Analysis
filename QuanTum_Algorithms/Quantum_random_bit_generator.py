from qiskit_ibm_provider import IBMProvider
import asyncio
import qiskit

import math
import sympy
import secrets

import threading
import hashlib


class QuantumRNG(object):
    def __init__(self, Token_file_path):

        # https://docs.python.org/3/library/secrets.html
        # Using the most secure source of randomness provided by the operating system

        self.sec_ = secrets.SystemRandom()                 # create an instance of the system random class
        sel_int = self.sec_.randrange(5 * 10 ** 100, 7 * 10 ** 100)   # select an integer between given range (a, b-1)
        self.qc_entropy_pool = "{0:b}".format(sel_int)      # converted the selected integer into the binary format
        self.seed = secrets.randbelow(3 * 10 ** 100)        # Generate a random number from 0 to the given number (0, n-1)

        # for the CSPRNG
        x = self.sec_.randrange(7 * 10 ** 100, 11 * 10 ** 100)  # Get the first random int to create a random prime
        y = self.sec_.randrange(7 * 10 ** 100, 11 * 10 ** 100)  # Get the second random int to create a random prime
        self.do_update_entropy()

        self.p = self.next_prime(x)                         # set the prime number for p based on the x value
        self.q = self.next_prime(y)                         # set the prime number for q based on the y value

        self.reseed_count = 0                               # set the reseed interval counter to 0
        self.reseed_interval = 10 ** 3  # reseed every 10 million bits - reduce this to test the IBMQ integration. -MC

        # do qiskit-y stuff
        with open(Token_file_path, 'r') as API_token:
            ibmqx_token = API_token.read().strip()

        self.provider = IBMProvider(ibmqx_token)
        self.ibmq_backend = self.provider.get_backend('ibmq_qasm_simulator')
        self.rng_circuit = self.make_circuit(15)

    def next_prime(self, Original_prime):
        next_usable_prime = sympy.nextprime(Original_prime)         # get the very first possible next prime number
        while next_usable_prime % 4 != 3:                           # very important to check the selected prime must be congruent to 3 modulo 4
            next_usable_prime = sympy.nextprime(next_usable_prime)  # keep trying until the condition is satisfied
        if self.seed % next_usable_prime ==0:                       # check for the modulus of seed and next usable prime, find another prime number
            next_usable_prime = self.next_prime(next_usable_prime + 1)
        return next_usable_prime

    def get_rand_bitstring(self, N=64):
        M = self.p * self.q

        if self.reseed_count > self.reseed_interval:
            self.do_update_entropy()

        x = self.seed

        bit_string = ""
        for _ in range(N):
            x = pow(x, 2) % M
            b = x % 2
            bit_string += str(b)

        self.seed = x                                               # update the seed
        self.reseed_count += N                                      # update bits count

        return bit_string

    def get_rand_bytes(self, N=8):

        b = self.get_rand_bitstring(N = N * 8)

        b = b + '0' * (8 - len(b) % 8)                      # make sure the length of the bits is multiple of 8

        int_v = int(b, 2)                                   # Convert the bit to an equivalent integer number

        num_bytes = (len(b) + 7) // 8                       # Get the required bytes to generate

        b_str = int_v.to_bytes(num_bytes, byteorder='big')  # Convert an integer to byte string using the inbuilt function

        return b_str

    def do_update_entropy(self):
        # print("doing entropy update...")

        # use system entropy in times of need
        if len(self.qc_entropy_pool) < 512:
            # Just copying bits from the local entropy pool for now... Not very elegant :-/ -MC
            local_bits = "{0:b}".format(self.sec_.randrange(2 * 10 ** 100, 3 * 10 ** 100))
            self.qc_entropy_pool += local_bits
            print("[!] Added {0} bits from local entropy pool...".format(len(local_bits)))

        if len(self.qc_entropy_pool) < 1025:  # we don't want to call too much...
            # use background thread to get quantum bits... Get 1024 bits in 15-bit chunks across so many shots on the QC. -MC
            # the queues might be long, so we just have to wait...
            get_qc_thread = threading.Thread(target=self.get_quantum_bits, name="IBM-QX Computation", args=(1024,))
            get_qc_thread.start()

        # consume 64-bits of entropy...
        self.seed += int(self.qc_entropy_pool[:256], 2)
        # remove the bits we used...
        self.qc_entropy_pool = self.qc_entropy_pool[256:]
        print("[!] Remaining bits in entropy pool: {0}".format(len(self.qc_entropy_pool)))
        # reset the count
        self.reseed_count = 0
        return

    @staticmethod
    def make_circuit(n=15):
        # This quantum circuit takes n-many qubits, and then puts them into
        # superposition with a Hadamard operation (transpiled to a Z-rotation, usually).
        # We then measure each qubit and put the outputs into a register of n-bits in length
        # and then return that back. -MC
        qr = qiskit.QuantumRegister(n)
        cr = qiskit.ClassicalRegister(n)
        circ = qiskit.QuantumCircuit(qr, cr)
        circ.h(qr)
        circ.measure(qr, cr)
        return circ

    @staticmethod
    def get_bits_from_counts(counts):
        bits = ""
        for i in [k for k, v in counts.items() if v == 1]:
            bits += i
        return bits

    def run_ibmq_circuit(self, shots=35):
        # our circuit will have 2^n bits of entropy of output, but the maximum number of shots allowed
        # on the big IBMQ 16-qubit machine in Melbourne is 2^14... so in theory we can run this
        # up to 2^14 times, and get 15 bits each time with little risk of things overlapping!
        # (Why? Because pigeonhole principle, and random...)
        # Thus in one job we can theoretically get up to 122,880 (15*8292) bits of good, pure,
        # quantum-ly-derived entropy!:- D The only problem; it isn't secret to us...
        # use jobs method instead of remaining_jobs_count method
        a = len(self.ibmq_backend.jobs())
        print(a)
        if len(self.ibmq_backend.remaining_jobs_count()) > 4:
            # if enough jobs are left en queue...
            # create an event loop object
            loop = asyncio.get_event_loop()
            # use asyncio=True as a dictionary with use_asyncio and loop keys
            job = qiskit.execute(self.rng_circuit, self.ibmq_backend, shots=shots,
                                 asyncio={"use_asyncio": True, "loop": loop})
            # wait for the job to finish
            job.wait_for_final_state()
            # get the result
            result = job.result()
            # get the bits from the counts
            bits = self.get_bits_from_counts(result.get_counts())
            print(bits)
        else:
            print("[!] No free jobs - using system randomness...")
            # return some system-y randomness
            bits = "{0:b}".format(self.sec_.randrange(2 * 10 ** 100, 3 * 10 ** 100))
        return bits

    def get_quantum_bits(self, n=512):
        print("[*] running bg IBMQ process")
        # default to get ceil(512/15) random bits from QC ...
        num_shots = math.ceil(n / self.rng_circuit.width() * 2)
        # go get the quantum! -MC
        bits_from_qc = self.run_ibmq_circuit(shots=num_shots)
        # hash everything to make the most of the quantum :P
        current_e_pool = self.qc_entropy_pool
        # clear the pool. or not -MC
        # self.qc_entropy_pool = ""
        m = hashlib.sha3_512()
        # Mixing it up twice by hashing the new bits and the old pool both ways...
        # This is basically using Keccak as an 'entropy expander' twice.
        # Reason for this is that our Quantum random bits aren't secret to only us,
        # and the entropy may be mismatched with our local os.urandom output,
        # so this should normalise it. :-) -MC
        for i in range(math.floor(len(bits_from_qc) / 512)):
            m.update(str(current_e_pool + bits_from_qc[i * 512:(i + 1) * 512]).encode('utf-8'))
            self.qc_entropy_pool += ''.join(format(byte, '08b') for byte in m.digest())
        m.update(str(bits_from_qc + current_e_pool).encode('utf-8'))
        self.qc_entropy_pool += ''.join(format(byte, '08b') for byte in m.digest())
        print(
            "[i] Updated the entropy pool with {0} bits from IBMQ, {1} bits after hashing...".format(len(bits_from_qc),
                                                                                                     (math.floor(
                                                                                                         len(bits_from_qc) / 512) + 1) * 512))
        return


if __name__ == "__main__":
    # Example usage or test cases can be added here

    # Example 1: Create an instance of QuantumRNG
    quantum_rng = QuantumRNG('my_API_token.txt')

    # Example 2: Generate random bits
    random_bits = quantum_rng.get_rand_bitstring(N=128)
    print(f"Generated random bits: {random_bits}")

    # Example 3: Generate random bytes
    random_bytes = quantum_rng.get_rand_bytes(N=8)
    print(f"Generated random bytes: {random_bytes}")

