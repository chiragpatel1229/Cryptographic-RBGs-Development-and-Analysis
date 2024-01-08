
from CTR_DRBG.Test_CTR import CTR_drbg
import os


def bytes_to_binary(bytes_str: bytes) -> str:
    return ''.join(format(b, '08b') for b in bytes_str)


def generate_sequences():

    sequences = []                              # Create a list to store the sequences

    drbg = CTR_drbg.CTRDRBG('aes256')

    entropy = os.urandom(48)

    data = b'John Doe' + b'\x25'
    drbg.init(entropy, data)

    for i in range(10):

        additional_data = i.to_bytes(1, 'big')
        random_bytes = drbg.generate(32, additional_data)

        sequences.append(random_bytes)

        entropy = os.urandom(48)

        data = b'blue' + b'cat'
        drbg.reseed(entropy, data)

    return sequences
