import matplotlib.pyplot as plt
import scipy.stats as stats
import hashlib
import os
from Tests_NIST import burstiness_para, memory_coeff

# -------------------------  user input  --------------------------------------------------------------------
# seq_len = 256                                    # sequence length
seed = os.urandom(32)                           # Select any random value as seed >32

# -------------------------  Hash RNG function  --------------------------------------------------------------


def Hash_RNG(initial_seed, length_bits):

    hash_256 = hashlib.sha256(initial_seed)     # Initiate the basic hash object
    num_bytes = (length_bits + 7) // 8          # Convert unsigned integer to >= nearest bytes
    bytes_seq = b''                             # Create empty list for bytes

    while len(bytes_seq) < num_bytes:           # Generate random bytes using the hash_256
        hash_256.update(bytes_seq)              # Update with a current object using the all updated bytes
        bytes_seq += hash_256.digest()          # take the Hash value as a sequence of bytes and Extend the sequence
    #     print("hash", hash_256)
    #     print(len(bytes_seq))
    #     print("bytes_seq", bytes_seq, '\n')
    #
    # print(len(bytes_seq))

    bin_seq = ''                                # Create empty string for binary list
    for byte in bytes_seq:
        binary_byte = format(byte, '08b')       # Convert bytes into binary with by leading zeros and 8 bit width
        bin_seq += binary_byte                  # Append the bits into the string

    bin_seq = bin_seq[:length_bits]             # Consider only required sequence length
    binary_list = [int(bit) for bit in bin_seq]  # Convert string to integer list

    return binary_list


# rnd_seq = Hash_RNG(seed, seq_len)
rnd_seq = '01101000010110110100011000100111100101001101110010010100001100001010000100100111001100010101101010001011110001000010001101000001001100110111011111010110100110010010111101100001111011101010101000101110111011100110010100011111011010000010000101010010010111110000110000101001000100111000011111000111101011110011110111011101100010001000000011011100011111001011010000101111010110110110110011010101110010111011111101100111111110111010100001010001011011001111101000111000111110101010101001100111010011001111010000111101111101011100010000101000011110001000010010101001000011110110000011001001101101010100111111100001011111110000101100100100000101110101100000111011001011010001000111000000'
rnd_seq = [int(bit) for bit in rnd_seq]
# print(rnd_seq)

# ======================================== Burstiness and Memory Coefficient ===========================================
burst = burstiness_para.B_Cal(rnd_seq)
print("Burstiness of the signal = ", burst)

memory = memory_coeff.memory_co(rnd_seq)
print("Memory Coefficient of the signal = ", memory)
# ======================= Calculate Gap Structures =============================


# Function to calculate gap structures (lengths of consecutive zeros) in a sequence
def cal_gaps(sequence):
    gap = []
    gap_counter = 0
    no_gap = 0                  # when we do not know the first bit is 1 or 0 so the condition is false

    for bits in sequence:
        if bits == 0:
            gap_counter += 1    # calculate the number of continued zeros between two ones
        elif bits == 1:         # finds the 1s in a list start checking for no gaps.
            if no_gap:          # if there are two continued 1s in a list then append the counter
                gap.append(gap_counter)  # add 0s in every step with no gap
            gap_counter = 0     # Reset the counter
            no_gap = 1          # found the no_gap in the list, it is true
    return gap


# Calculate gap structures for rnd_seq and M_sequence
rnd_gaps = cal_gaps(rnd_seq)


# ==================== Count and Normalise the gap structure ================================


def cal_norm_gaps(my_seq):                   # find the unique gaps in the sequence
    uniq_gaps = []
    counts = []
    for unq_gap_len in set(my_seq):
        count = my_seq.count(unq_gap_len)    # count repetition of same gaps
        uniq_gaps.append(unq_gap_len)        # find and store the unique gaps
        counts.append(count)                 # Total Number of similar gaps

    # Normalise the gap structures
    total = sum(my_seq)                      # sum of Gap sequence
    norm_gaps = []                           # normalised gap structures
    for count in counts:
        normalised = count / total           # normalise every count using total sum of gaps
        norm_gaps.append(normalised)         # store normalised gaps in a list
    return uniq_gaps, norm_gaps


rnd_uniq_gaps, rnd_norm_gaps = cal_norm_gaps(rnd_gaps)
print(rnd_norm_gaps, "\n", rnd_uniq_gaps)
print(sum(rnd_norm_gaps))


# ======================== Chi-Square Test ====================================
rnd_zeros = rnd_seq.count(0)        # counting zeros in the sequence
rnd_ones = rnd_seq.count(1)         # counting ones in the sequence


print(f"Random Sequence Balance - 0s= {rnd_zeros}, 1s= {rnd_ones}")
seq_len = len(rnd_seq)
expected_value = 0.5 * seq_len      # expected values of zeros and ones


def test(zeros, ones, expected):
    # using the equation of Chi-Square test
    chi_square = (zeros - expected) ** 2 / expected + (ones - expected) ** 2 / expected

    p_val_cdf = stats.chi2.cdf(chi_square, df=1)    # get the probability value using cumulative distribution function
    p_val_pdf = stats.chi2.pdf(chi_square, df=1)    # df = 1 bcz we have only 0s and 1s

    return chi_square, p_val_cdf, p_val_pdf


# Calculate Chi-square test results and p-values for gap structures
rnd_chi, rnd_p_value_cdf, rnd_p_value_pdf = test(rnd_zeros, rnd_ones, expected_value)


# Print Chi-square test results and p-values
print("Chi-square test Result of a Random Sequence :", rnd_chi)
print("P-value (CDF) of a Random Sequence          :", rnd_p_value_cdf)
print("P-value (pDF) of a Random Sequence          :", rnd_p_value_pdf, "\n")


# ============================ Graphs ==========================================


# Plot the Gap Structures of rnd_seq and M_sequence
def plot_histogram(uniq_gaps, norm_gaps, title):
    plt.figure()
    bars = plt.bar(uniq_gaps, norm_gaps, width=0.15, align='center')
    plt.title(title)
    plt.xlabel("Gap Length")
    plt.ylabel("Count")

    for num in range(len(bars)):        # write the normalised value on top of the bars
        bar = bars[num]
        value = norm_gaps[num]
        x_pos = bar.get_x() + bar.get_width() / 2
        plt.text(x_pos, value, f"{value:.2f}", ha='center', va='bottom')


plot_histogram(rnd_uniq_gaps, rnd_norm_gaps, "The graph of a random sequence Gap-Structures")

plt.show()
