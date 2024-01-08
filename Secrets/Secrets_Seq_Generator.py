import secrets

# ======================================================================================================================
# Enter the number of sequences!
# ======================================================================================================================
Enter_the_Number_of_Seq_To_Generate = 1000

# ======================================================================================================================
# Bytes to Binary
# ======================================================================================================================


def bytes_to_binary(bytes_str: bytes) -> str:
    return ''.join(format(b, '08b') for b in bytes_str)


# ======================================================================================================================
# Sequence Generator
# ======================================================================================================================


def generate_random_sequence(number_of_sequences):

    # with statement to make sure the file is closed properly at the end
    with open("Secrets_Sequences.txt", "w") as sequences_file:

        for i in range(number_of_sequences):

            # secrets module to generate the random sequence of desired bytes
            sequence = secrets.token_bytes(64)  # 32 bytes = 256 bits

            # Convert the output to the binary string of 0s and 1s
            output_bits = bytes_to_binary(sequence)

            # Write the output bits in the TEXT file
            sequences_file.write(output_bits + "\n")


generate_random_sequence(Enter_the_Number_of_Seq_To_Generate)
