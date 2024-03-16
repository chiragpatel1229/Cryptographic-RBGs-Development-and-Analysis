from qiskit_ibm_provider import IBMProvider
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute
import sympy
import secrets
import threading
import hashlib

number_of_bits = 512
number_of_bytes = 0

class QuantumRNG(object):

    def __init__(self, Token_file_path):

        self.backend = None
        self.provider = None
        self.Token_file_path = Token_file_path
        self.sec_ = secrets.SystemRandom()
        sel_int = self.sec_.randrange(5 * 10 ** 100, 7 * 10 ** 100)
        self.entropy = "{0:b}".format(sel_int)
        self.seed = secrets.randbelow(7 * 10 ** 100)

        x = self.sec_.randrange(7 * 10 ** 100, 11 * 10 ** 100)
        y = self.sec_.randrange(7 * 10 ** 100, 11 * 10 ** 100)

        self.p = self.next_prime(x)
        self.q = self.next_prime(y)

        self.reseed_count = 0
        self.reseed_interval = 2048

    def next_prime(self, Original_prime):
        next_usable_prime = sympy.nextprime(Original_prime)
        while next_usable_prime % 4 != 3:
            next_usable_prime = sympy.nextprime(next_usable_prime)
        if self.seed % next_usable_prime == 0:
            next_usable_prime = self.next_prime(next_usable_prime + 1)
        return next_usable_prime

    def _update(self):

        if len(self.entropy) < 512:
            sel_int = self.sec_.randrange(2 * 10 ** 100, 3 * 10 ** 100)
            local_bits = "{0:b}".format(sel_int)
            self.entropy += local_bits

        if len(self.entropy) < 1025:
            quantum_bits = threading.Thread(target=self.Refill_entropy, name='GenCj bitsP')
            quantum_bits.start()

        self.seed += int(self.entropy[:256], 2)
        self.entropy = self.entropy[256:]
        self.reseed_count = 0
        return

    def Quantum_circuit(self):

        with open(self.Token_file_path, 'r') as API_token:
            My_token = API_token.read().strip()

        self.provider = IBMProvider(str(My_token))
        self.backend = self.provider.get_backend('simulator_mps')

        quantum_R = QuantumRegister(80)
        class_R = ClassicalRegister(80)
        circuit = QuantumCircuit(quantum_R, class_R)
        circuit.h(quantum_R)
        circuit.measure(quantum_R, class_R)

        key_1, key_2, key_3, key_4, key_5 = "", "", "", "", ""

        for i in range(3):
            job = execute(circuit, self.backend, shots=10)
            job.wait_for_final_state()
            result = job.result()
            counts = result.get_counts()
            keys = list(counts.keys())
            if len(keys) >= 5:
                key_1 += keys[0]
                key_2 += keys[2]
                key_3 += keys[3]
                key_4 += keys[4]
                key_5 += keys[5]

        bits = key_1 + key_2 + key_3 + key_4 + key_5
        return bits

    def Refill_entropy(self):

        q_bits = self.Quantum_circuit()
        current_e_pool = self.entropy
        cjp = hashlib.sha3_256()

        for i in range(len(q_bits) // 256 + 1):
            bits2hash = str(current_e_pool + q_bits[i * 256:(i + 1) * 256]).encode('utf-8')
            cjp.update(bits2hash)

            b_str = []
            for byte in cjp.digest():
                b_2b = format(byte, '08b')
                b_str.append(b_2b)
            self.entropy += ''.join(b_str)

        C_input = str(q_bits + current_e_pool).encode('utf-8')
        cjp.update(C_input)
        m_bytes = []
        for byte in cjp.digest():
            b2b = format(byte, '08b')
            m_bytes.append(b2b)

        self.entropy += ''.join(m_bytes)

    def ran_bits(self, n_req_bits=64):

        M = self.p * self.q

        if self.reseed_count > self.reseed_interval:
            self._update()

        x = self.seed

        bit_string = ""
        for _ in range(n_req_bits):
            x = pow(x, 2) % M
            b = x % 2
            bit_string += str(b)

        self.seed = x
        self.reseed_count += n_req_bits

        return bit_string

    def ran_bytes(self, N=0):

        b = self.ran_bits(n_req_bits=N * 8)

        b = b + '0' * (8 - len(b) % 8)

        int_v = int(b, 2)

        num_bytes = (len(b) + 7) // 8

        b_str = int_v.to_bytes(num_bytes, byteorder='big')

        return b_str

quantum_rng = QuantumRNG('API_token.txt')

# for _ in range(0,30):
#     random_bits = quantum_rng.ran_bits(n_req_bits=number_of_bits)
#     print(f"Generated random bits: {random_bits}")
#
# if number_of_bytes > 1:
#     random_bytes = quantum_rng.ran_bytes(N=number_of_bytes)
#     print(f"Generated random bytes: {random_bytes}")
r = quantum_rng.Quantum_circuit()
print(r)