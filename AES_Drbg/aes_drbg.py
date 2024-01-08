import pyaes
# import os

class AES_DRBG(object):

    def __init__(self, keylen):

        self.aes = None
        self.keylen = keylen

        self.reseed_counter = 0
        self.key = False
        self.ctr = False

        self.outlen = 16  # same for all

        if keylen == 256:
            self.seedlen = 48
            self.keylen = 32

        elif keylen == 192:
            self.seedlen = 40
            self.keylen = 24

        elif keylen == 128:
            self.seedlen = 32
            self.keylen = 16

        else:
            raise ValueError("Keylen not supported")

        self.reseed_interval = 2 ** 48  # same for all

    def instantiate(self, entropy_in, per_string=b''):

        if len(entropy_in) != self.seedlen:
            raise ValueError("Length of entropy input must be equal to seedlen")

        # if len(per_string) < self.seedlen:
        #
        #     raise ValueError("Length of personalization string must be equal to seedlen")

        else:

            per_string = b"\x00" * self.seedlen

        seed_material = int(entropy_in.hex(), 16) ^ int(per_string.hex(), 16)
        seed_material = seed_material.to_bytes(self.seedlen, byteorder='big', signed=False)

        self.key = seed_material[0:self.keylen]
        self.ctr = pyaes.Counter(initial_value=int(seed_material[-self.outlen:].hex(), 16))

        self.aes = pyaes.AESModeOfOperationCTR(self.key, counter=self.ctr)

        self.reseed_counter = 1

    def _update(self, provided_data):

        temp = b""

        while len(temp) < self.seedlen:
            output_block = self.aes.encrypt(b"\x00" * self.outlen)  # generate key stream
            temp = temp + output_block  # concat key stream

        temp = temp[0:self.seedlen]

        # check if provided_data is empty
        if provided_data:
            # xor key stream only if provided_data is not empty
            temp = int(temp.hex(), 16) ^ int(provided_data.hex(), 16)
            temp = temp.to_bytes(self.seedlen, byteorder='big', signed=False)

        self.key = temp[0:self.keylen]
        self.ctr = pyaes.Counter(initial_value=int(temp[-self.outlen:].hex(), 16))

        self.aes = pyaes.AESModeOfOperationCTR(self.key, counter=self.ctr)  # update the key and the counter

    def reseed(self, entropy_in, add_in=b''):

        if self.reseed_counter > self.reseed_interval:
            raise Warning("the DRBG should be reseeded !!!")

        if len(entropy_in) != self.seedlen:
            raise ValueError("Length of entropy input must be equal to seedlen")

        if len(add_in) != 0:

            if len(add_in) != self.seedlen:
                raise ValueError("Length of additional input must be equal to seedlen")

        else:

            add_in = b"\x00" * self.seedlen

        seed_material = int(entropy_in.hex(), 16) ^ int(add_in.hex(), 16)
        seed_material = seed_material.to_bytes(self.seedlen, byteorder='big', signed=False)

        self._update(seed_material)

        self.reseed_counter = 1

    def generate(self, req_bytes, add_in=b''):

        if self.reseed_counter > self.reseed_interval:
            raise Warning("the DRBG should be reseeded !!!")

        if len(add_in) != 0:

            if len(add_in) != self.seedlen:
                raise ValueError("Length of additional input must be equal to seedlen")

            self._update(add_in)

        temp = b''

        while len(temp) < req_bytes:
            output_block = self.aes.encrypt(b"\x00" * self.outlen)  # generate random bytes
            temp = temp + output_block

        returned_bytes = temp[0:req_bytes]

        self._update(add_in)

        self.reseed_counter = self.reseed_counter + 1

        return returned_bytes
