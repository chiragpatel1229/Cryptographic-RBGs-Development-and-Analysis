import math
import numpy
import scipy.special as spc

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


seq = '11111101000110010011111000000010000011111110111101111111100000000000111100001000111111010101000101110011010000010001011011011011111010001101110110101101011111110111110100010001011000111111110000001001011100100111001011111010101101010110101000010111010011001101011110100100101011111000100010101010101010101111001001110001110010001100100111011110110010111111000001110001011011100100000101100000111010100111001111100101110101001111000101001001011011110101011111101110101000000110011001001001000101010000011011110010'
#
#
# # seq = (1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0)
#
print("Probability value: ", longest_runs(seq))
