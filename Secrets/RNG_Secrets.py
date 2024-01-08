import matplotlib.pyplot as plt
import scipy.stats as stats
import secrets


# ------------------------------------  Randbelow Function 1  ---------------------------------------------------------
# def Secrets_RNG(length):
#     bin_seq = []  # Create an empty list
#
#     for _ in range(length):
#         rnd_int = secrets.randbelow(22)  # Select a random number from 0-21
#         bin_num = bin(rnd_int)[2:]       # Convert the selected number into binary and remove '0b' prefix
#         bin_num = bin_num.zfill(5)       # Maintain the fixed width of 5 bits
#
#         for digit in bin_num:
#             bin_seq.append(int(digit))   # Append binary digit as an integer
#
#     bin_seq = bin_seq[:length]           # Consider only required sequence length
#     return bin_seq

# ------------------------------------  Randbelow Function 2  ---------------------------------------------------------

# def Secrets_RNG(Length):
#
#     bin_seq = []                         # Create an empty list
#
#     for _ in range(Length):
#         rnd_bit = secrets.randbelow(2)   # Select between 0 and 1
#         bin_bit = bin(rnd_bit)[2:]       # Convert an integer to binary
#         bin_seq.append(int(bin_bit))     # Append the bit as an integer in the list
#
#     return bin_seq


# ------------------------------------  Randbits  --------------------------------------------------------------

# def Secrets_RNG(length):
#
#     rnd_int = secrets.randbits(length)         # Select bits as a K value
#     bin_seq = bin(rnd_int)[2:].zfill(length)   # convert the integer into binary and padding with zero
#     bin_seq = [int(bit) for bit in bin_seq]    # Convert binary string to integer list
#
#     return bin_seq


# ------------------------------------  Token bytes  --------------------------------------------------------------

def Secrets_RNG(length):
    # Generate random bytes and convert them to a binary string
    rnd_bytes = secrets.token_bytes((length + 7) // 8)   # generate byte string using given bit integer
    bin_seq = ''  # Create empty string

    for byte in rnd_bytes:
        bin_bits = format(byte, '08b')      # Convert bytes into binary with by leading zeros and 8 bit width
        bin_seq += bin_bits                 # Append the bits in the string

    bin_seq = bin_seq[:length]              # Consider only required sequence length
    binary_list = [int(bit) for bit in bin_seq]     # Convert binary string to integer list

    return binary_list


# ------------------------------------  user input  --------------------------------------------------------------

# Generate a random binary sequence of 1024 bits as a list of integers
seq_len = 1024
rnd_seq = Secrets_RNG(seq_len)
# print(rnd_seq)
print(f"sequence ni length: {len(rnd_seq)}")


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


# ======================== Chi-Square Test ====================================

rnd_zeros = rnd_seq.count(0)        # counting zeros in the sequence
rnd_ones = rnd_seq.count(1)         # counting ones in the sequence

print(f"Random Sequence Balance - 0s= {rnd_zeros}, 1s= {rnd_ones}")

expected_value = 0.5 * seq_len     # expected values of zeros and ones


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


# plot_histogram(rnd_uniq_gaps, rnd_norm_gaps, "The graph of a random sequence Gap-Structures")
plt.show()
