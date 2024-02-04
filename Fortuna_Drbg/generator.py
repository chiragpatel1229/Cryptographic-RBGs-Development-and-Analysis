from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


class Generator:
    block_size = AES.block_size     # Number of blocks
    key_size = 32

    def __init__(self):
        self.cipher = None
        self.counter = None
        self.key = None

    # Regenerate seed
    def reseed(self, seed):
        # seed Seed
        if self.key is None:
            self.key = b'\0' * self.key_size
        self.counter = Counter.new(nbits=self.block_size * 8, initial_value=0, little_endian=True)  # Instantiate Counter here
        self.set_key(SHA256.new(SHA256.new(self.key + seed).digest()).digest())

    # Generate new key
    def set_key(self, key):
        self.key = key
        self.cipher = AES.new(key, AES.MODE_CTR, counter=self.counter)

    # Block Generate AES encrypted data block
    def generate_blocks(self, n):
        # n Number of blocks
        # Fake 16n bytes of random byte string
        assert self.key != b''
        result = b''
        for i in range(n):
            result += self.cipher.encrypt(self.counter(), )
        return result

    # Generate random data
    def pseudo_random_data(self, n):
        # n The number of bytes of random data to be generated
        # Return n bytes of random data
        assert 0 <= n <= 2**20
        result = self.generate_blocks(n // 16 if n % 16 == 0 else (n // 16) + 1)[:n]
        self.key = self.generate_blocks(2)

        return result
