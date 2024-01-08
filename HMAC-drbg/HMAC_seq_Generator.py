from hmac_drbg import HMAC_DRBG
import secrets

# ======================================================================================================================
# Define the length of the input values in bytes
EntropyInputLength = 32
NonceLength = 16
PersonalizationStringLength = 0
EntropyInputReseedLength = 32

# ======================================================================================================================
'''Define the number of sequences to generate'''
num_sequences = 1000
# ======================================================================================================================

# Define the file name
parameters_filename = "inputs_for_HMAC.txt"
sequence_list_filename = "HMAC_DRBG_Sequences.txt"

# Open the files in write mode
parameters_file = open(parameters_filename, "w")
sequence_list_file = open(sequence_list_filename, "w")

# ======================================================================================================================
OutputBits = []

# Loop for each sequence
for i in range(num_sequences):
    # Generate random input values using the random module
    EntropyInput = secrets.token_bytes(EntropyInputLength)
    Nonce = secrets.token_bytes(NonceLength)
    PersonalizationString = b"Chirag Patel's Testing"
    EntropyInputReseed = secrets.token_bytes(EntropyInputReseedLength)

    # ==================================================================================================================

    # Instantiate the HMAC_DRBG object with the input values
    drbg = HMAC_DRBG(entropy=(EntropyInput + Nonce), personalization_string=PersonalizationString)

    # Reseed the HMAC_DRBG object with the EntropyInputReseed value
    drbg.reseed(EntropyInputReseed)

    # Generate 32 bytes (256 bits) of pseudorandom output
    output = drbg.generate(64)

    # Assume output is the bytes object returned by your function
    OutputBits.append(''.join(format(b, '08b') for b in output))

    # ==================================================================================================================

    # Convert the input values and the output to hexadecimal format
    EntropyInput = EntropyInput.hex()
    Nonce = Nonce.hex()
    PersonalizationString = PersonalizationString.hex()
    EntropyInputReseed = EntropyInputReseed.hex()
    output = output.hex()

    # ==================================================================================================================

    # Create a string with the input parameters and the output in the given format
    input_output_string = "COUNT = {}\nEntropyInput = {}\nNonce = {}\nPersonalizationString = {}\n" \
                          "EntropyInputReseed = {}\nReturnedBits = {}\n" \
                          "\n".format(i, EntropyInput, Nonce, PersonalizationString, EntropyInputReseed, output)

    # Write the string to the parameters file
    parameters_file.write(input_output_string)

# ======================================================================================================================

# Write the binary strings to the sequence list file
for binary_string in OutputBits:
    sequence_list_file.write(binary_string + "\n")

# ======================================================================================================================

# Close the files
parameters_file.close()
sequence_list_file.close()
