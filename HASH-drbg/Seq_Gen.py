from hash_drbg import Hash_DRBG
import os

# for the input selection the NIST doc is considered from the section 1.01 -> Table 2


# function to convert a byte string to binary string
def bytes_to_binary(bytes_str: bytes) -> str:
    return ''.join(format(b, '08b') for b in bytes_str)


def generate_random_sequence(num_bytes: int, security_strength: int = 256, num_seq: int = 1):

    random_seq = None       # Assign a default value to random_seq

    if num_seq > 1:
        sequences_file = open("Hash_DRBG_Sequences.txt", "w")
        parameters_file = open("inputs_for_Hash.txt", "w")

        for i in range(num_seq):
            # Generate a random entropy input of the required length
            # The length should be at least 1.5 times the security strength
            # The length should not exceed 1000 bits
            entropy_length = max(security_strength * 3 // 2, 256) // 8
            entropy_length = min(entropy_length, 1000 // 8)
            entropy = os.urandom(entropy_length)

            # Generate a random nonce of the required length
            # The length should be equal to half the security strength
            # The length should not exceed 256 bits
            nonce_length = security_strength // 2 // 8
            nonce_length = min(nonce_length, 256 // 8)
            nonce = os.urandom(nonce_length)

            # Generate a random personalization string of the required length
            # The length should be equal to the security strength
            # The length should not exceed 256 bits
            personalization_length = security_strength // 8
            personalization_length = min(personalization_length, 256 // 8)
            personalization = os.urandom(personalization_length)

            # Instantiate the Hash_DRBG object with the generated parameters
            drbg = Hash_DRBG(entropy + nonce, security_strength, personalization)

            # Generate a random entropy input for reseeding of the required length
            # The length should be at least 1.5 times the security strength
            # The length should not exceed 1000 bits
            entropy_input_reseed = os.urandom(entropy_length)

            # Generate a random additional input for reseeding of the required length
            # The length should be equal to the security strength
            # The length should not exceed 256 bits
            additional_input_reseed = b"Chirag Patel"

            # Reseed the Hash_DRBG object with the generated entropy input and additional input
            drbg.reseed(entropy_input_reseed, additional_input_reseed)

            # Generate the random sequence of bytes using the Hash_DRBG object
            # The number of bytes should not exceed 7500 bits
            random_o = drbg.generate(num_bytes)
            # Convert the output to a binary string of 0s and 1s
            output_bits = bytes_to_binary(random_o)

            # Write the output bits to the sequences file
            sequences_file.write(output_bits + "\n")

            # Convert the input values and the output to hexadecimal format
            entropy_input = entropy.hex()
            nonce = nonce.hex()
            personalization_string = personalization.hex()
            output = random_o.hex()
            entropy_input_reseed = entropy_input_reseed.hex()
            additional_input_reseed = additional_input_reseed.hex()

            # Create a string with the input parameters and the output in the given format
            input_output_string = "COUNT = {}\nEntropyInput = {}\nNonce = {}\nPersonalizationString = {}\n" \
                                  "EntropyInputReseed = {}\nAdditionalInputReseed = {}\nReturnedBits = {}\n" \
                                  "\n".format(i, entropy_input, nonce, personalization_string, entropy_input_reseed, additional_input_reseed, output)

            # Write the string to the parameters file
            parameters_file.write(input_output_string)

        # Close the files
        sequences_file.close()
        parameters_file.close()

    else:
        # Generate a random entropy input of the required length
        # The length should be at least 1.5 times the security strength
        # The length should not exceed 1000 bits
        entropy_length = max(security_strength * 3 // 2, 256) // 8
        entropy_length = min(entropy_length, 1000 // 8)
        entropy = os.urandom(entropy_length)

        # Generate a random nonce of the required length
        # The length should be equal to half the security strength
        # The length should not exceed 256 bits
        nonce_length = security_strength // 2 // 8
        nonce_length = min(nonce_length, 256 // 8)
        nonce = os.urandom(nonce_length)

        # Generate a random personalization string of the required length
        # The length should be equal to the security strength
        # The length should not exceed 256 bits
        personalization_length = security_strength // 8
        personalization_length = min(personalization_length, 256 // 8)
        personalization = os.urandom(personalization_length)

        # Instantiate the Hash_DRBG object with the generated parameters
        drbg = Hash_DRBG(entropy + nonce, security_strength, personalization)

        # Generate a random entropy input for reseeding of the required length
        # The length should be at least 1.5 times the security strength
        # The length should not exceed 1000 bits
        entropy_input_reseed = os.urandom(entropy_length)

        # Generate a random additional input for reseeding of the required length
        # The length should be equal to the security strength
        # The length should not exceed 256 bits
        additional_input_reseed = b"Chirag Patel"

        # Reseed the Hash_DRBG object with the generated entropy input and additional input
        drbg.reseed(entropy_input_reseed, additional_input_reseed)

        # Generate the random sequence of bytes using the Hash_DRBG object
        # The number of bytes should not exceed 7500 bits
        random_seq = drbg.generate(num_bytes)

    # Return the random sequence of bytes
    return random_seq


# Test the generate_random_sequence function with some examples
# The examples use different values for the number of bytes and the security strength
# The examples print the random sequence of bytes in hexadecimal format
# print("Example 1:")
# num_bytes = 16
# security_strength = 128
# random_sequence = generate_random_sequence(num_bytes, security_strength)
# print(random_sequence.hex(), "\n")
#
#
# print("Example 2:")
# num_bytes = 32
# security_strength = 192
# random_sequence = generate_random_sequence(num_bytes, security_strength)
# print(random_sequence.hex(), "\n")
#
#
# print("Example 3:")
# num_bytes = 64
# security_strength = 256
# random_sequence = generate_random_sequence(num_bytes, security_strength)
# print(random_sequence.hex(), "\n")


print("Example 4:")
num_bytes = 64
security_strength = 256
random_sequence = generate_random_sequence(num_bytes, security_strength, 1000)

# ======================================================================================================================


