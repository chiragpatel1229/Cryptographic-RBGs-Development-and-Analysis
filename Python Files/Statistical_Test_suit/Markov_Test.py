import math
import matplotlib.pyplot as plt
import os

""" OKAY
Section 6.3.3 - Markov Estimate, data is assumed to be list of binary integers or a bit string
The recommended input bits should be 1000

If the entropy source is used for cryptographic applications, the min-entropy per symbol(output) should be close to ~1.
check the foot note on page 40:
The min-entropy according to the MCV estimator is 0.712, while the true min-entropy is 0.795.
The min-entropy estimate is based on the entropy present in any subsequence (i.e., chain) of outputs, instead of an estimate of the min-entropy per output.
"""

''' This Function Is Tested OKAY with the Given Data In The NIST Document 6.3.3.4'''


def markov_test(data, print_output: int = None):

    if isinstance(data, str):                   # convert the bit string to the list of integers
        data = [int(bit) for bit in data]

    i, C_0, C_1, C_00, C_10 = 0, 0, 0, 0, 0     # Initialize the variables for counts

    s_len = len(data)                           # Get the length of the input sequence

    # Get counts for unconditional and transition probabilities as in section 6.3.3
    for i in range(s_len - 1):
        if data[i] == 0:                        # Append the counter if the bit is 0
            C_0 += 1
            if data[i + 1] == 0:                # append the counter if the bit is 00
                C_00 += 1
        elif data[i + 1] == 0:                  # append the counter if the bit is 10
            C_10 += 1                           # created the lists: C_0, C_00, C_10 ======

    # C_0 is now the number of 0s bits from S[0] to S[len-2]
    C_1 = s_len - 1 - C_0                       # C_1 is the number of 1s bits from S[0] to S[len-2]

    # Calculate all the sub-set symbols in the sequence
    # Note that P_X1 = C_X1 / C_X = (C_X - C_X0) / C_X = 1.0 - C_X0 / C_X = 1.0 - P_X0
    if C_0 > 0:
        P_00 = C_00 / C_0
        P_01 = 1.0 - P_00
    else:
        P_00 = 0.0
        P_01 = 0.0

    if C_1 > 0:
        P_10 = C_10 / C_1
        P_11 = 1.0 - P_10
    else:
        P_10 = 0.0
        P_11 = 0.0

    # Account for the last symbol or bit in the sequence
    if data[s_len - 1] == 0:
        C_0 += 1                                # C_0 is now the number of 0 bits from S[0] to S[len-1]

    P_0 = C_0 / s_len                           # Normalise the number of 0s
    P_1 = 1.0 - P_0                             # get the Normalise the number of 1s

    if print_output == 0:                        # if user ask for the printed results
        print(f"Markov Estimate: P_0 ..= {P_0:.17g}")
        print(f"Markov Estimate: P_1 ..= {P_1:.17g}")
        print(f"Markov Estimate: P_0,0 = {P_00:.17g}")
        print(f"Markov Estimate: P_0,1 = {P_01:.17g}")
        print(f"Markov Estimate: P_1,0 = {P_10:.17g}")
        print(f"Markov Estimate: P_1,1 = {P_11:.17g}")

    H_min = 128.0

    # In the next block, note that if P_0X > 0.0, then P_0 > 0.0
    # and similarly if P_1X > 0.0, then P_1 > 0.0

    # apply the formula and logic to calculate the probability of each sub-set of symbols as in section 6.3.3.3

    # Sequence 00...0
    if P_00 > 0.0:
        tmp_min_entropy = -math.log2(P_0) - 127.0 * math.log2(P_00)
        if tmp_min_entropy < H_min:
            H_min = tmp_min_entropy

    # Sequence 0101...01
    if P_01 > 0.0 and P_10 > 0.0:
        tmp_min_entropy = -math.log2(P_0) - 64.0 * math.log2(P_01) - 63.0 * math.log2(P_10)
        if tmp_min_entropy < H_min:
            H_min = tmp_min_entropy

    # Sequence 011...1
    if P_01 > 0.0 and P_11 > 0.0:
        tmp_min_entropy = -math.log2(P_0) - math.log2(P_01) - 126.0 * math.log2(P_11)
        if tmp_min_entropy < H_min:
            H_min = tmp_min_entropy

    # Sequence 100...0
    if P_10 > 0.0 and P_00 > 0.0:
        tmp_min_entropy = -math.log2(P_1) - math.log2(P_10) - 126.0 * math.log2(P_00)
        if tmp_min_entropy < H_min:
            H_min = tmp_min_entropy

    # Sequence 1010...10
    if P_10 > 0.0 and P_01 > 0.0:
        tmp_min_entropy = -math.log2(P_1) - 64.0 * math.log2(P_10) - 63.0 * math.log2(P_01)
        if tmp_min_entropy < H_min:
            H_min = tmp_min_entropy

    # Sequence 11...1
    if P_11 > 0.0:
        tmp_min_entropy = -math.log2(P_1) - 127.0 * math.log2(P_11)
        if tmp_min_entropy < H_min:
            H_min = tmp_min_entropy

    entEst = min(H_min / 128.0, 1.0)            # Calculate the Min-Entropy using the formula in 6.3.3.4

    if print_output == 0:
        print(f"Markov Estimate: p-hat_max.. = {2.0 ** (-H_min):.17g}")
        print(f"Markov Estimate: min entropy = {entEst:.17g}")

    return entEst


# NIST recommendation on min-entropy calculation =======================================================================
def min_entropy(seq__):
    if isinstance(seq__, str):                   # convert the bit string to the list of integers
        seq__ = [int(bit) for bit in seq__]

    zeros = seq__.count(0)
    ones = seq__.count(1)

    p0 = zeros / len(seq__)
    p1 = ones / len(seq__)

    max_ = max(p1, p0)

    min_en = -math.log2(max_)

    return min_en


# ======================================================================================================================
# seq = '111111111100000000000111100001000111111010101000101110011010000010001011011011011111010001101110110101101011111110111110100010001011000111111110000001001011100100111001011111010101101010110101000010111010011001101011110100100101011111000100010101010101010101111001001110001110010001100100111011110110010111111000001110001011011100100000101100000111010100111001111100101110101001111000101001001011011110101011111101110101000000110011001001001000101010000011011110010'
# # # seq = (1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0)
# markov_test(seq, 1)
# print(min_entropy(seq))

# Function to read sequences from a .txt file ==========================================================================
def read_sequences(file_name_):
    with open(file_name_, 'r') as file:                      # open the file in a read mode
        _sequences = []                                      # set a buffer to store the sequences
        for line in file:
            stripped_line = line.strip()                     # extract each sequence as a separate line
            mapped_line = list(map(int, stripped_line))      # convert each line to the list of integers
            _sequences.append(mapped_line)                   # append each sequence as a list to the buffer
    return _sequences                                        # return the list of sequences


# Function to calculate norm_gaps and uniq_gaps of each sequence =======================================================
def Mako(seq_):
    all_mako = []                                          # set a buffer to store the normalised gaps
    for sequence in seq_:
        min__ = markov_test(sequence)
        all_mako.append(min__)
    return all_mako


def all_min(seq_):
    _all_min_ = []                                          # set a buffer to store the normalised gaps
    for sequence in seq_:
        _min__ = min_entropy(sequence)         # collect only normalised gaps
        _all_min_.append(_min__)   # set them with a descending order to ease the further part
    return _all_min_

# Function to plot the normalized gap length of 0 and 1 for all sequences ==============================================
def plot_mako(norm_gaps_zero, f_name=None, __min=None):
    avg_norm_gap_zero = sum(norm_gaps_zero) / len(norm_gaps_zero)
    plt.figure()
    print(f"{f_name}: Expected = {__min:.5f}, {avg_norm_gap_zero:.5f}")
    plt.grid(True)
    plt.plot(norm_gaps_zero, label=f'Data')
    plt.axhline(y=__min, color='r', linestyle='-', linewidth=1, label=f'Expected = {__min:.5f}')  # Horizontal line at y = 0.5
    plt.axhline(y=avg_norm_gap_zero, color='g', linestyle='-', linewidth=1, label=f'Avg. = {avg_norm_gap_zero:.5f}')  # Horizontal line at average value
    # plt.text(0, avg_norm_gap_zero, f'Avg: {avg_norm_gap_zero:.2f}', color='b', va='bottom')  # Add average value label
    # plt.title(f"Markov - min-entropy estimation for {f_name}")
    plt.xlabel("Sequence Number")
    plt.ylabel("min-entropy")
    plt.legend(loc='best')
    plt.ylim(0.80, 1.005)


# Use the functions ====================================================================================================
file_names = ['../RBG_data_files/QRNG.txt',
              '../RBG_data_files/AES.txt',
              '../RBG_data_files/ChaCha20.txt', '../RBG_data_files/CTR.txt',
              '../RBG_data_files/Hash.txt',
              '../RBG_data_files/HMAC.txt', '../RBG_data_files/M_sequences.txt',
              '../RBG_data_files/RC4.txt', '../RBG_data_files/RSA.txt',
              '../RBG_data_files/Synthetic.txt', '../RBG_data_files/bit-flip_Model.txt',
              '../RBG_data_files/Ideal_model.txt', '../RBG_data_files/thermal_Model.txt']

for file_name in file_names[:]:

    b_n = os.path.basename(file_name)           # Extract only the file name
    base_name = os.path.splitext(b_n)[0]        # Remove file extension

    sequences = read_sequences(file_name)       # collect All the sequences
    mako_min = Mako(sequences)              # all normalised gaps
    min_entropy__ = all_min(sequences)
    av_mim = sum(min_entropy__) / len(min_entropy__)

    plot_mako(mako_min, base_name, av_mim)
    plt.savefig(f"Markov_{base_name}.png")

plt.show()
