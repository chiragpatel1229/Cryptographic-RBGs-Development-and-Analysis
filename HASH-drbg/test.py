import codecs
import sys
from hash_drbg import Hash_DRBG

# Reads test vectors from HMAC_DRBG.rsp, and tests them against the HMAC_DRBG
# module.
# inputs_for_Hash.txt is from self generated parameters, which can be found in its folder
# Test Vectors archive from self generated file.

# A hacked together way to parse the rsp test vector files.


def read_entry(file, expected_name):
    name, value = file.readline().strip().split(b'=')
    name = name.strip()
    value = value.strip()

    assert name == expected_name

    return codecs.decode(value, 'hex')


algorithm = b""
tests_performed = 0
with open('inputs_for_Hash.txt', 'rb') as f:
    while True:
        line = f.readline()
        if line == b'':
            break

        line = line.strip()

        if not line.startswith(b'COUNT'):
            continue

        # Read stimulus and expected result
        EntropyInput = read_entry(f, b'EntropyInput')
        Nonce = read_entry(f, b'Nonce')
        PersonalizationString = read_entry(f, b'PersonalizationString')
        EntropyInputReseed = read_entry(f, b'EntropyInputReseed')
        AdditionalInputReseed = read_entry(f, b'AdditionalInputReseed')
        ReturnedBits = read_entry(f, b'ReturnedBits')

        # Test
        drbg = Hash_DRBG(entropy=(EntropyInput + Nonce), personalization_string=PersonalizationString)
        drbg.reseed(entropy=EntropyInputReseed, additional_input=AdditionalInputReseed)
        drbg.generate(len(ReturnedBits))
        result = drbg.generate(len(ReturnedBits))

        if result != ReturnedBits:
            print("FAILURE")
            print(f"EntropyInput = {codecs.encode(EntropyInput, 'hex')}")
            print(f"Nonce = {codecs.encode(Nonce, 'hex')}")
            print(f"PersonalizationString = {codecs.encode(PersonalizationString, 'hex')}")
            print(f"EntropyInputReseed = {codecs.encode(EntropyInputReseed, 'hex')}")
            print(f"AdditionalInputReseed = {codecs.encode(AdditionalInputReseed, 'hex')}")
            print(f"ReturnedBits = {codecs.encode(ReturnedBits, 'hex')}")
            sys.exit(-1)

        tests_performed += 1


print(f"PASSED! Performed {tests_performed} tests.")
