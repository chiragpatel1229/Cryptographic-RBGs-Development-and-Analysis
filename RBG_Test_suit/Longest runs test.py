import math
import numpy
import scipy.special as spc
import matplotlib.pyplot as plt
import os

"""
2.2.7 Input Size Recommendation
It is recommended that each sequence to be tested consist of a minimum of 100 bits (i.e., n ≥ 100). Note
that n ≥ MN. The block size M should be selected such that M ≥ 20, M > .01n and N < 100.                     In this code N = 32
2.2.8 Example
(input) ε = 11001001000011111101101010100010001000010110100011
00001000110100110001001100011001100010100010111000
(input) n = 100
(input) M = 10
(processing) N = 10
(processing) χ 2 = 7.2
(output) P-value = 0.706438
(conclusion) Since P-value ≥ 0.01, accept the sequence as random.
"""
def longest_runs(bin_data: str):

    """
    Note that this description is taken from the NIST documentation [1] and git repo [2]
    [1] http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf
    [2] https://gist.github.com/StuartGordonReid/bde6c2bc31f19bfd2a91
    The focus of the tests is the longest run of ones within M-bit blocks. The purpose of this test is to determine
    whether the length of the longest run of ones within the tested sequences is consistent with the length of the
    longest run of ones that would be expected in a random sequence. Note that an irregularity in the expected
    length of the longest run of ones implies that there is also an irregularity ub tge expected length of the long
    est run of zeroes. Therefore, only one test is necessary for this statistical tests of randomness

    It takes binary data as an input argument and returns a probability p-value
    """

    if len(bin_data) < 128:
        print("\t", "Not enough data to run test!")
        return -1.0
    elif len(bin_data) < 256:
        k, m = 3, 8
        v_values = [1, 2, 3, 4]
        pik_values = [0.21484375, 0.3671875, 0.23046875, 0.1875]
    elif len(bin_data) < 6272:
        k, m = 5, 128
        v_values = [4, 5, 6, 7, 8, 9]
        pik_values = [0.1174035788, 0.242955959, 0.249363483, 0.17517706, 0.102701071, 0.112398847]
    elif len(bin_data) < 41472:
        k, m = 5, 512
        v_values = [6, 7, 8, 9, 10, 11]
        pik_values = [0.1170, 0.2460, 0.2523, 0.1755, 0.1027, 0.1124]
    elif len(bin_data) < 113000:
        k, m = 5, 1000
        v_values = [7, 8, 9, 10, 11, 12]
        pik_values = [0.1307, 0.2437, 0.2452, 0.1714, 0.1002, 0.1088]
    else:
        k, m = 6, 10000
        v_values = [10, 11, 12, 13, 14, 15, 16]
        pik_values = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]

    num_blocks = math.floor(len(bin_data) / m)
    frequencies = numpy.zeros(k + 1)
    block_start, block_end = 0, m
    for i in range(num_blocks):

        # Slice the binary string into a block
        block_data = bin_data[block_start:block_end]

        # Keep track of the number of ones
        max_run_count, run_count = 0, 0             # check the counts of 0s and 1s in the sequence
        for j in range(0, m):
            if block_data[j] == '1':
                run_count += 1
                max_run_count = max(max_run_count, run_count)
            else:
                max_run_count = max(max_run_count, run_count)
                run_count = 0

        max_run_count = max(max_run_count, run_count)           # consider whatever is maximum
        if max_run_count < v_values[0]:
            frequencies[0] += 1
        for j in range(k):
            if max_run_count == v_values[j]:
                frequencies[j] += 1
        if max_run_count > v_values[k - 1]:
            frequencies[k] += 1

        block_start += m                # update the block size with each iteration
        block_end += m

    # print(frequencies)
    chi_squared = 0
    for i in range(len(frequencies)):
        chi_squared += (pow(frequencies[i] - (num_blocks * pik_values[i]), 2.0)) / (num_blocks * pik_values[i])
    p_val = spc.gammaincc(float(k / 2), float(chi_squared / 2))

    return p_val


# Function to read sequences from a .txt file ==========================================================================
def read_sequences(file_name_):
    with open(file_name_, 'r') as file:                      # open the file in a read mode
        _sequences = []                                      # set a buffer to store the sequences
        for line in file:
            # stripped_line = line.strip()                     # extract each sequence as a separate line
            # mapped_line = list(map(int, stripped_line))      # convert each line to the list of integers
            mapped_line = line.strip()
            _sequences.append(mapped_line)                   # append each sequence as a list to the buffer
    return _sequences                                        # return the list of sequences


# Function to calculate Burstiness of each sequence =======================================================
def Longest_of_all_sequences(seq_):
    all_bursty_data = []                                          # set a buffer to store the normalised gaps
    for sequence in seq_:
        L_ = longest_runs(sequence)                               # find the gaps from each sequence
        all_bursty_data.append(L_)   # set them with a descending order to ease the further part
    return all_bursty_data


# Function to plot the normalized gap length of 0 and 1 for all sequences ==============================================
def plot_longest(g_in, f_name=None):
    avg_norm_gap_zero = sum(g_in) / len(g_in)
    print(f"{f_name}: {avg_norm_gap_zero:.5f}")
    plt.figure()
    plt.grid(True)
    plt.plot(g_in, label='data')
    plt.axhline(y=0.1, color='r', linestyle='-', linewidth=1, label='Expected = 0.1')  # Horizontal line at y = 0.5
    plt.axhline(y=avg_norm_gap_zero, color='g', linestyle='-', linewidth=1,
                label=f'Avg. = {avg_norm_gap_zero:.5f}')  # Horizontal line at average value
    # plt.text(0, avg_norm_gap_zero, f'Avg: {avg_norm_gap_zero:.2f}', color='b', va='bottom')  # Add average value label
    # plt.title(f"Normalized length of 0 gap {f_name}")
    plt.xlabel("Sequence Number")
    plt.ylabel("P-value")
    plt.legend(loc='best')
    plt.ylim(-0.10, 1.3)


# seq = '11111101000110010011111000000010000011111110111101111111100000000000111100001000111111010101000101110011010000010001011011011011111010001101110110101101011111110111110100010001011000111111110000001001011100100111001011111010101101010110101000010111010011001101011110100100101011111000100010101010101010101111001001110001110010001100100111011110110010111111000001110001011011100100000101100000111010100111001111100101110101001111000101001001011011110101011111101110101000000110011001001001000101010000011011110010'
# # # seq = (1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0)
# a = longest_runs(seq)
# print("Probability value: ", a)
# plot_longest(a)



# Use the functions ====================================================================================================
file_names = ['../RBG_data_files/AES_DRBG.txt',
              '../RBG_data_files/ChaCha20.txt', '../RBG_data_files/CTR_DRBG.txt',
              '../RBG_data_files/hash_drbg.txt', '../RBG_data_files/QRNG.txt',
              '../RBG_data_files/hmac_drbg.txt', '../RBG_data_files/M_sequences.txt',
              '../RBG_data_files/RC4_algorithm.txt', '../RBG_data_files/RSA_algorithm.txt',
              '../RBG_data_files/Synthetic_RBG.txt', '../RBG_data_files/Q_bit-flip_noice_Model.txt',
              '../RBG_data_files/Ideal Q-simulator.txt', '../RBG_data_files/Q_thermal_noice_Model.txt']

# file_names = ['../RBG_data_files/Q_thermal_noice_Model.txt']

for file_name in file_names[:]:
    # get the file names
    b_n = os.path.basename(file_name)           # Extract only the file name
    base_name = os.path.splitext(b_n)[0]        # Remove file extension

    sequences = read_sequences(file_name)       # collect All the sequences
    burst = Longest_of_all_sequences(sequences)     # all normalised gaps

    plot_longest(burst, base_name)
#     plt.savefig(f"Longest_{base_name}")
#
# plt.show()