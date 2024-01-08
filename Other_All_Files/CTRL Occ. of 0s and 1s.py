import matplotlib.pyplot as plt
import scipy.stats as stats
import random
import secrets
import numpy as np
import hashlib
import os

# -------------------------  user input  --------------------------------------------------------------------

seq_len = 1024           # sequence length
seed = os.urandom(32)    # Select any random value as seed >32
# zero_prob = 0.60         # Probability of generating a zero

# ======================= a list of ones in the sequences =============================

# rnd_seq1 = np.ones(seq_len, dtype=int).tolist()
# rnd_seq1 = [1] * seq_len
# rnd_seq1 = [1 for _ in range(seq_len)]

# print(rnd_seq1)

# ======================= OS.Urandom Generator =============================

# number_of_bytes = (seq_len + 7) // 8        # Convert seq_len to bytes
# rnd_seed = os.urandom(number_of_bytes)      # Generate required random bytes
# bin_seq = ''                                # Create empty string for binary list
# for byte in rnd_seed:
#     binary_byte = format(byte, '08b')       # Convert bytes into binary with by leading zeros and 8 bit width
#     bin_seq += binary_byte                  # Append the bits into the string
#
# bin_seq = bin_seq[:seq_len]                 # Consider only required sequence length
# rnd_seq1 = [int(bit) for bit in bin_seq]    # Convert string to integer list
# secrets.SystemRandom().shuffle(rnd_seq1)    # Shuffle the sequence securely


# ======================= Rand_below Generator =============================

# rnd_seq1 = []                                   # Create empty list for new sequence
# for _ in range(seq_len):
#     random_integer = secrets.randbelow(100)     # select any random number from 0-99
#     if random_integer < zero_prob * 100:        # if the number is less than zero probability
#         rnd_seq1.append(0)                      # append a zero
#     else:
#         rnd_seq1.append(1)                      # or append a one
# secrets.SystemRandom().shuffle(rnd_seq1)        # securely shuffle the elements by creating instance of SystemRandom()


# ======================= Random bit Generator =============================
# rnd_seq1 = []                                   # Create empty list for new sequence
# for _ in range(seq_len):
#     if random.random() < zero_prob:             # generate a random float between 0-1
#         rnd_seq1.append(0)
#     else:
#         rnd_seq1.append(1)
#
# secrets.SystemRandom().shuffle(rnd_seq1)        # securely shuffle the elements by creating instance of SystemRandom()
#
# print(rnd_seq1, "\n\n")                 # Print the random binary sequence

# ======================= Hash RNG function =============================

def Hash_RNG(initial_seed, length_bits):

    hash_256 = hashlib.sha256(initial_seed)     # Initiate the basic hash object
    num_bytes = (length_bits + 7) // 8          # Convert unsigned integer to >= nearest bytes

    bytes_seq = b''                             # Create empty list for bytes
    while len(bytes_seq) < num_bytes:           # Generate random bytes using the hash_256
        hash_256.update(bytes_seq)              # Update with a current object using the all updated bytes
        bytes_seq += hash_256.digest()          # take the Hash value as a sequence of bytes and Extend the sequence

    bin_seq = ''                                # Create empty string for binary list
    for byte in bytes_seq:
        binary_byte = format(byte, '08b')       # Convert bytes into binary with by leading zeros and 8 bit width
        bin_seq += binary_byte                  # Append the bits into the string

    bin_seq = bin_seq[:length_bits]             # Consider only required sequence length
    binary_list = [int(bit) for bit in bin_seq]  # Convert string to integer list

    return binary_list


rnd_seq1 = Hash_RNG(seed, seq_len)
# print(rnd_seq1)


# ======================= Controlling the gap of non gaps =============================


# def count_non_gaps(sequence):
#     return sum(1 for i in range(len(sequence) - 1) if sequence[i] == 1 and sequence[i + 1] == 1)
#
#
# def edit_sequence(sequence, desired_probability):
#     edited_sequence = sequence.copy()  # Make a copy of the original sequence to avoid modifying it directly
#
#     current_non_gaps = count_non_gaps(edited_sequence)
#     total_possible_insertions = len(edited_sequence) - current_non_gaps
#
#     while current_non_gaps / total_possible_insertions < desired_probability:
#         # Find a random index with a zero value to insert a one
#         index = random.randint(0, len(edited_sequence) - 1)
#
#         if edited_sequence[index] == 0:
#             edited_sequence[index] = 1
#             current_non_gaps += 1
#
#     return edited_sequence
#
#
# # Input your existing sequence as a list
# existing_sequence = rnd_seq2
#
# # Define the desired probability (e.g., 0.3 for 30% chance of two ones in a row)
# desired_prob = 0.6
#
# # Edit the sequence
# rnd_seq1 = edit_sequence(existing_sequence, desired_prob)


# ================= control bits in the random sequence ========================


def ctrl_0s_1s(sequence, prob):                          # Control the occurrence of zeros and ones in the sequence
    one_prob = 1 - prob                                  # calculate occurrence of Ones
    n_seq = []                                           # Create empty list for new sequence

    for bit in sequence:
        if bit == 0 and np.random.rand() > prob:         # check the present bit = 0 and random float is > prob
            n_seq.append(1)                              # if YES, update a new bit
        elif bit == 1 and np.random.rand() > one_prob:   # check the present bit = 1 and random float is > prob
            n_seq.append(0)                              # if YES, update a new bit
        else:
            n_seq.append(bit)                            # Otherwise keep the original value

    # secrets.SystemRandom().shuffle(n_seq)                # Shuffle the sequence securely
    return n_seq


zero_prob = 0.6
rnd_seq = ctrl_0s_1s(rnd_seq1, zero_prob)
# print("controlled: ", rnd_seq)
# print("Random: ", rnd_seq1)

# ======================= Calculate Gap Structures =============================


def cal_gaps(sequence):
    gap = []
    gap_counter = 0
    no_gap = 0                          # when we do not know the first bit is 1 or 0 so the condition is false

    for bits in sequence:
        if bits == 0:
            gap_counter += 1            # calculate the number of continued zeros between two ones
        elif bits == 1:                 # finds the 1s in a list start checking for no gaps.
            if no_gap:                  # if there are two continued 1s in a list then append the counter
                gap.append(gap_counter)  # add 0s in every step with no gap
            gap_counter = 0             # Reset the counter
            no_gap = 1                  # found the no_gap in the list, it is true
    return gap


# Calculate gap structures for rnd_seq and M_sequence
rnd_gaps = cal_gaps(rnd_seq)
o_rnd_gaps = cal_gaps(rnd_seq1)


# ==================== Count and Normalise the gap structure ================================


def cal_norm_gaps(my_seq, o_seq):                   # find the unique gaps in the sequence
    uniq_gaps = []
    counts = []
    for unq_gap_len in set(my_seq):
        count = my_seq.count(unq_gap_len)   # count repetition of same gaps
        uniq_gaps.append(unq_gap_len)       # find and store the unique gaps
        counts.append(count)                # Total Number of similar gaps

    # Normalise the gap structures
    total = sum(o_seq)                     # sum of Gap sequence
    norm_gaps = []                          # normalised gap structures
    for count in counts:
        normalised = count / total          # normalise every count using total sum of gaps
        norm_gaps.append(normalised)        # store normalised gaps in a list

    return uniq_gaps, norm_gaps


rnd_uniq_gaps, rnd_norm_gaps = cal_norm_gaps(rnd_gaps, rnd_seq)
o_rnd_uniq_gaps, o_rnd_norm_gaps = cal_norm_gaps(o_rnd_gaps, rnd_seq1)


# ======================== Chi-Square Test ====================================
rnd_zeros = rnd_seq.count(0)                # counting zeros in the sequence
rnd_ones = rnd_seq.count(1)                 # counting ones in the sequence
o_rnd_zeros = rnd_seq1.count(0)                # counting zeros in the sequence
o_rnd_ones = rnd_seq1.count(1)                 # counting ones in the sequence

print(f"Original Random Sequence Balance - 0s= {o_rnd_zeros}, 1s= {o_rnd_ones} \n\n")
print(f"Controlled Random Sequence Balance - 0s= {rnd_zeros}, 1s= {rnd_ones} \n\n")

expected_value = 0.5 * seq_len              # expected values of zeros and ones


def test(zeros, ones, expected):
    # using the equation of Chi-Square test
    chi_square = (zeros - expected) ** 2 / expected + (ones - expected) ** 2 / expected

    p_val_cdf = stats.chi2.cdf(chi_square, df=1)  # get the probability value using cumulative distribution function
    p_val_pdf = stats.chi2.pdf(chi_square, df=1)  # df = 1 bcz we have only 0s and 1s

    return chi_square, p_val_cdf, p_val_pdf


# # Calculate Chi-square test results and p-values for gap structures
# rnd_chi, rnd_p_value_cdf, rnd_p_value_pdf = test(rnd_zeros, rnd_ones, expected_value)
# o_rnd_chi, o_rnd_p_value_cdf, o_rnd_p_value_pdf = test(o_rnd_zeros, o_rnd_ones, expected_value)
# #
# #
# # # Print Chi-square test results and p-values
# print("Chi-square test Result of an Original Random Sequence :", o_rnd_chi)
# print("P-value (CDF) of an Original Random Sequence          :", o_rnd_p_value_cdf)
# print("P-value (pDF) of an Original Random Sequence          :", o_rnd_p_value_pdf, "\n")
# #
# print("Chi-square test Result of a Controlled Random Sequence :", rnd_chi)
# print("P-value (CDF) of a Controlled Random Sequence          :", rnd_p_value_cdf)
# print("P-value (pDF) of a Controlled Random Sequence          :", rnd_p_value_pdf, "\n")


# ============================ Graphs ==========================================


# Plot the Gap Structures of rnd_seq and M_sequence
def plot_histogram(uniq_gaps, norm_gaps, title):
    plt.figure()
    bars = plt.bar(uniq_gaps, norm_gaps, width=0.15, align='center')
    plt.title(title)
    plt.xlabel("Gap Length")
    plt.ylabel("Count")

    for num in range(len(bars)):            # write the normalised value on top of the bars
        bar = bars[num]
        value = norm_gaps[num]
        x_pos = bar.get_x() + bar.get_width() / 2
        plt.text(x_pos, value, f"{value:.2f}", ha='center', va='bottom')


plot_histogram(rnd_uniq_gaps, rnd_norm_gaps, "The graph of a Controlled random sequence Gap-Structures")
plot_histogram(o_rnd_uniq_gaps, o_rnd_norm_gaps, "The graph of an Original random sequence Gap-Structures")

plt.show()
