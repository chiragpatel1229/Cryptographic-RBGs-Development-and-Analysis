from Crypto.Hash import SHA256
from Crypto.Util import Counter
from Crypto.Cipher import AES
import time
import os
import dill
from profilehooks import profile

class Accumulator:
    pool_number = 32
    min_pool_size = 64
    reseed_interval = 0.1
    P = []

    def __init__(self):
        self.P = [b''] * self.pool_number
        self.ReseedCnt = 0
        self.generator = Generator()
        self.last_seed = time.time()

    @profile
    def random_data(self, n):
        if len(self.P[0]) >= self.min_pool_size or time.time() - self.last_seed > self.reseed_interval:
            self.ReseedCnt += 1
            # Use list comprehension instead of loop
            s = b''.join(SHA256.new(SHA256.new(self.P[i]).digest()).digest() for i in range(self.pool_number) if self.ReseedCnt % (2 ** i) == 0)
            # Use pickle to save and load the generator object
            with open("generator.pkl", "wb") as f:
                dill.dump(self.generator, f)
            self.generator.reseed(s)
            self.last_seed = time.time()
            with open("generator.pkl", "rb") as f:
                self.generator = dill.load(f)
        return self.generator.pseudo_random_data(n)

    @profile
    def add_random_event(self, s, i, e):
        assert 0 < len(e) <= 32 and 0 <= s <= 255 and 0 <= i <= 31
        self.P[i] = self.P[i] + (str(s) + str(len(e))).encode() + e


class Generator:
    block_size = AES.block_size
    key_size = 32
    # Use __slots__ to reduce memory usage
    __slots__ = ["cipher", "counter", "key"]

    def __init__(self):
        self.cipher = None
        self.counter = Counter.new(nbits=self.block_size * 8, initial_value=0, little_endian=True)  # This is the ctr object
        self.key = None

    @profile
    def reseed(self, seed):
        if self.key is None:
            self.key = b'\00' * self.key_size
        self.set_key(SHA256.new(SHA256.new(self.key + seed).digest()).digest())
        # self.counter() # Remove this line

    @profile
    def set_key(self, key):
        self.key = key
        self.cipher = AES.new(key, AES.MODE_CTR, counter=self.counter)  # Use the ctr object as the counter parameter

    @profile
    def generate_blocks(self, n):
        assert self.key != b''
        print(self.cipher)
        result = b''
        for i in range(n):
            result += self.cipher.encrypt(self.counter())  # Use the ctr object instead of the function call
        return result

    @profile
    def pseudo_random_data(self, n):
        assert 0 <= n <= 2**20
        result = self.generate_blocks(n // 16 if n % 16 == 0 else (n // 16) + 1)[:n]
        self.key = self.generate_blocks(2)
        return result


if __name__ == '__main__':
    accumulator = Accumulator()
    # Use os.urandom() instead of /dev/random
    seed = os.urandom(64)
    assert len(seed) == 64
    accumulator.generator.reseed(seed)
    n = 1
    while n != 0:
        n = int(input("\n(Enter 0 to exit)\nPlease enter the number of bytes of the generated random number (n>0): "))
        if n == 0:
            print("Exited!\n")
            quit()
        elif n < 0:
            print("Input error!!!\n")
            quit()
        else:
            print("\nGenerate random number:\n%r" % accumulator.random_data(n).hex())
