import codecs
import sys
from hmac_drbg import HMAC_DRBG

# Reads test vectors from HMAC_DRBG.rsp, and tests them against the HMAC_DRBG
# module.
# HMAC_DRBG.rsp is from drbg_vectors_pr_false.zip, which can be found in the DRBG
# Test Vectors archive from http://csrc.nist.gov/groups/STM/cavp/.

# A hacked together way to parse the rsp test vector files.


def read_entry(file, expected_name):
    name, value = file.readline().strip().split(b'=')
    name = name.strip()
    value = value.strip()

    assert name == expected_name

    return codecs.decode(value, 'hex')


algorithm = b""
tests_performed = 0
with open('NIST_test_data.rsp', 'rb') as f:
    while True:
        line = f.readline()
        if line == b'':
            break

        line = line.strip()

        if line.startswith(b'[') and b'=' not in line:
            algorithm = line

        if algorithm != b'[SHA-256]':
            continue

        if not line.startswith(b'COUNT'):
            continue

        # Read stimulus and expected result
        EntropyInput = read_entry(f, b'EntropyInput')
        Nonce = read_entry(f, b'Nonce')
        PersonalizationString = read_entry(f, b'PersonalizationString')
        EntropyInputReseed = read_entry(f, b'EntropyInputReseed')
        AdditionalInputReseed = read_entry(f, b'AdditionalInputReseed')
        AdditionalInput0 = read_entry(f, b'AdditionalInput')
        AdditionalInput1 = read_entry(f, b'AdditionalInput')
        ReturnedBits = read_entry(f, b'ReturnedBits')

        # This implementation does not support additional input
        if AdditionalInputReseed != b'' or AdditionalInput0 != b'' or AdditionalInput1 != b'':
            continue

        # Test
        drbg = HMAC_DRBG(entropy=(EntropyInput + Nonce), personalization_string=PersonalizationString)
        drbg.reseed(entropy=EntropyInputReseed)
        drbg.generate(len(ReturnedBits))
        result = drbg.generate(len(ReturnedBits))

        if result != ReturnedBits:
            print("FAILURE")
            print(f"EntropyInput = {codecs.encode(EntropyInput, 'hex')}")
            print(f"Nonce = {codecs.encode(Nonce, 'hex')}")
            print(f"PersonalizationString = {codecs.encode(PersonalizationString, 'hex')}")
            print(f"EntropyInputReseed = {codecs.encode(EntropyInputReseed, 'hex')}")
            print(f"AdditionalInputReseed = {codecs.encode(AdditionalInputReseed, 'hex')}")
            print(f"AdditionalInput = {codecs.encode(AdditionalInput0, 'hex')}")
            print(f"AdditionalInput = {codecs.encode(AdditionalInput1, 'hex')}")
            print(f"ReturnedBits = {codecs.encode(ReturnedBits, 'hex')}")
            sys.exit(-1)

        tests_performed += 1


print(f"PASSED! Performed {tests_performed} tests.")
