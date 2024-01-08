import copy

""" This file is able to generate M-sequences using the user defined polynomials, initial states and the desired list of 
lengths. The number of lengths will be the total number of sequences for the given polynomials. 

This file also generates a Gold Code sequence using the generated M-sequences.

The user can select only two polynomial and its relevant seeds for the current code. if more parameters are require then
the code need to be modified accordingly in the sections 4.0 and 5.0"""

# 0.0 ================================= USER INPUTS ====================================================================

polynomial_1 = [5, 2]                               # Any poly. can be selected here as an input
polynomial_2 = [7, 5, 2]                            # Any poly. can be selected here as an input

seq_len = [31, 62, 127]                             # sequence length can be both a [single integer or a list]

initial_state_1 = [1, 1, 1, 0, 1]                   # The init state must be equal to the length of polynomial
initial_state_2 = [1, 0, 1, 0, 1, 0, 0]             # The init state must be equal to the length of polynomial

# select the "index-number" from the seq_len list to generate the Gold sequence ========================================
selected_index_number_for_gold_seq = 3              # select the number from 1 to end of list from seq_len (eg.: 3 = 127)

# print the results or not =============================================================================================
print_results = True                                # False for the empty console

# ======================================================================================================================

# 1.0 ===== A function to convert polynomial integers to the relevant list of integers =================================


def p_2_b_i(pol):                                   # convert the polynomial to binary and then list of integers

    """"" This example is for converting the polynomial: [5,2]
    if polynomial = 5 which means 2 ** 5 = 32, which converts using galois field with position 32 = 100000
       if polynomial = 2 which means 2 ** 2 = 4, which converts using galois field with position 4 = 100
       so, polynomial = [5, 2] which means (2 ** 5) + (2 ** 2) = 32 + 4 = 36, 
                               which converts using galois field with position 32 = 0b100100
       for the final calculations we need only this feedback taps = 10010 (remove firs 2 bits and the last bit that will be always 0)"""""

    # 1.1 === convert the user provided polynomial to Binary string ====================================================
    deg = []                                        # Collect the degrees in the provided polynomial
    for degree in pol:                              # loop through each index of the list
        deg.append(2 ** degree)                     # find the correct feedback taps from the provided polynomial

    bin_p = bin(sum(deg))                           # get the final position with the sum of total degrees and convert to binary
    poly = bin_p[2:-1]                              # Remove first two bits '0b' and a lst bit '0'

    # 1.2 === Convert the binary polynomial to the list of integers type ===============================================
    list_p = []                                     # get the feedback taps in list format
    for bit in poly:
        list_p.append(int(bit))

    return list_p


# 2.0 ===== A function to generate M-sequences =========================================================================


def generate_m_sequence(polynomial, lengths, state):

    # 2.1 === Check if the user has provided a list of lengths or just a length, it will define the number of total sequences
    if not isinstance(lengths, list):                   # Make sure lengths is a list even a single length
        lengths = [lengths]

    list_poly = p_2_b_i(polynomial)                     # convert the polynomial to binary and then to list of integers

    # 2.2 === Check the polynomial binary list and the initial state list length are equal =============================
    if len(state) != len(list_poly):
        raise ValueError("The length of initial state must be equal to the maximum number of the primitive polynomial list")

    # 2.3 === Generate number of sequences for the provided lengths ====================================================
    all_seq = []                                        # Empty List to store all the generated m-sequence
    for length in lengths:                              # generate user defined number of sequences

        state_copy = copy.copy(state)                   # making a copy of the state is must for generating number of sequences

        # 2.3.1 === perform the liner recursion method on the linear feedback shift registers (LFSR) ===================
        m_seq = []                                      # set the buffer to store the m-sequence

        for _ in range(length):                         # iterate for the user defined sequence length

            # 2.3.1.1 === set the counter and set the output bit position for each iteration ===========================
            output_bit = state_copy[-1]                 # take the right most bit as an output
            bit_counter = 0                             # set the feedback bit counter to zero

            # 2.3.1.2 === calculate the product of each bit of polynomial and initial seed to the similar position =====
            for j in range(len(list_poly)):

                p = list_poly[j] * state_copy[-j - 1]   # calculate the number of feedback bits
                # [-j - 1] for j=0: [-1], j=1: [-2], so using the state list in the reverse order

                bit_counter += p                        # count the total bits for every stage, add up all the 1s in the stage

            # 2.3.1.3 === perform the modulo operation and adjust the bits in the stages to get the output and reseeding the new bit
            bit_counter %= 2                            # Perform the modulo operation to find the right most bit or the new bit
            state_copy = [bit_counter] + state_copy[:-1]          # add a first new bit and remove the last bit
            m_seq.append(output_bit)                    # Append the output bit to the m-sequence
        all_seq.append(m_seq)
    return all_seq


# 3.0 ===== A function to Print each sequences with its number of 0s and 1s ============================================


def Gold_Sequence(s_1, s_2):

    gold_sequence = []                                  # buffer to store the gold sequence bits after XOR operation

    for bit1, bit2 in zip(s_1, s_2):                    # Generate the Gold code sequence by XORing both the sequences

        x_or_ed = bit1 ^ bit2                           # XOR each bit from both sequences and append to gold_sequence
        gold_sequence.append(x_or_ed)

    return gold_sequence

# 3.0 ===== A function to Print each sequences with its number of 0s and 1s ============================================


def print_Seq(parameters_name, seq, len_list):
    for i, seq in enumerate(seq):
        num_zeros = seq.count(0)
        num_ones = seq.count(1)
        print(f"{parameters_name} m-sequence number '{i + 1}' with length of {len_list[i]}: {seq}")
        print(f"Sequence Balance: 0s = {num_zeros}, 1s = {num_ones}\n")
    print("\n\n")


# 4.0 ===== Generate and Print the m-sequences =========================================================================
M_sequence_1 = generate_m_sequence(polynomial_1, seq_len, initial_state_1)
M_sequence_2 = generate_m_sequence(polynomial_2, seq_len, initial_state_2)

if True:
    print_Seq('1st type', M_sequence_1, seq_len)                      # print the generated results for 1st parameters
    print_Seq('2nd type', M_sequence_2, seq_len)                      # print the generated results for 2nd parameters

# 5.0 ===== Generate the gold-sequence =================================================================================

seq_1 = M_sequence_1[int(selected_index_number_for_gold_seq) - 1]     # adjust the index number because it starts from 0
seq_2 = M_sequence_2[int(selected_index_number_for_gold_seq) - 1]
G_seq = Gold_Sequence(seq_1, seq_2)

if True:
    print("Gold Sequence: ", G_seq, "\nLength of the Gold sequence: ", len(G_seq))
    print(f"Gold Sequence Balance: 0s = {seq_1.count(0)}, 1s = {seq_2.count(1)}\n")
