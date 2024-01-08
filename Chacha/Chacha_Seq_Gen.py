from ChaCha20 import chacha20_block
import os

# ======================================================================================================================
''' Enter the number of sequences! '''
Enter_the_Number_of_Seq_To_Generate = 1000
# ======================================================================================================================


def bytes_to_binary(bytes_str: bytes) -> str:
    return ''.join(format(b, '08b') for b in bytes_str)


def generate_random_sequence(number_of_sequences):

    # Define the key and nonce
    key = os.urandom(32)
    counter = 1

    sequences_file = open("ChaCha20_Stream_Cipher_Sequences.txt", "w")
    parameters_file = open("inputs_for_chacha.txt", "w")

    # Generate 10 different sequences by incrementing the counter
    for i in range(number_of_sequences):

        counter_in = counter + i

        nonce = os.urandom(12)

        sequence = chacha20_block(key, counter_in, nonce)

        # Convert the output to a binary string of 0s and 1s
        output_bits = bytes_to_binary(sequence)

        # Write the output bits to the sequences file
        sequences_file.write(output_bits + "\n")

        # Create a string with the input parameters and the output in the given format
        input_output_string = "COUNT = {}\nKey = {}\ncounter = {}\nnonce = {}\n".format(i, key, counter_in, nonce)

        # Write the string to the parameters file
        parameters_file.write(input_output_string)

    # Close the files
    sequences_file.close()
    parameters_file.close()


generate_random_sequence(Enter_the_Number_of_Seq_To_Generate)
