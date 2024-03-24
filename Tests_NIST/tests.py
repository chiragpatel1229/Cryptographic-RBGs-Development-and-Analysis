import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from Tests_NIST import burstiness_para
from Tests_NIST import memory_coeff
from Tests_NIST import Markov_Test
from Tests_NIST import b_chisquare_ind
from Tests_NIST import b_goodness_of_fit


# ======================= Calculate Gap Structures =====================================================================
# Function to calculate gap structures (lengths of consecutive zeros) in a sequence
def cal_gaps(_sequence):
    gap = []
    gap_counter = 0
    no_gap = 0                  # when we do not know the first bit is 1 or 0 so the condition is false

    for bits in _sequence:
        if bits == 0:
            gap_counter += 1    # calculate the number of continued zeros between two ones
        elif bits == 1:         # finds the 1s in a list start checking for no gaps.
            if no_gap:          # if there are two continued 1s in a list then append the counter
                gap.append(gap_counter)  # add 0s in every step with no gap
            gap_counter = 0     # Reset the counter
            no_gap = 1          # found the no_gap in the list, it is true
    # print("gaps: ", gap)
    return gap


# ==================== Count and Normalise the gap structure ===========================================================
def cal_norm_gaps(my_seq):                   # find the unique gaps in the sequence
    uniq_gaps_ = []
    counts_ = []
    for unq_gap_len in set(my_seq):
        count = my_seq.count(unq_gap_len)    # count repetition of same gaps
        uniq_gaps_.append(unq_gap_len)        # find and store the unique gaps
        counts_.append(count)                 # Total Number of similar gaps

    # Normalise the gap structures
    total = sum(my_seq)                      # sum of Gap sequence
    norm_gaps_ = []                           # normalised gap structures
    for count in counts_:
        normalised = count / total           # normalise every count using total sum of gaps
        norm_gaps_.append(normalised)         # store normalised gaps in a list

    # print("counts: ", counts, "unique gaps: ", uniq_gaps_, "norm gaps: ", norm_gaps_)
    return uniq_gaps_, norm_gaps_, counts_


# ======================== Chi-Square Test =============================================================================
def chi_test(zeros, ones, expected):
    # using the equation of Chi-Square test
    chi_square = (zeros - expected) ** 2 / expected + (ones - expected) ** 2 / expected

    p_val_cdf = stats.chi2.cdf(chi_square, df=1)    # get the probability value using cumulative distribution function
    p_val_pdf = stats.chi2.pdf(chi_square, df=1)    # df = 1 bcz we have only 0s and 1s

    return chi_square, p_val_cdf, p_val_pdf


# ============================ Graphs ==================================================================================
# Plot the Gap Structures of rnd_seq and M_sequence
def plot_histogram(un_gaps, no_gaps, title):
    plt.figure()
    bars = plt.bar(un_gaps, no_gaps, width=0.15, align='center')
    plt.title(title)
    plt.xlabel("Gap Length")
    plt.ylabel("Count")

    for num in range(len(bars)):        # write the normalised value on top of the bars
        bar = bars[num]
        value = no_gaps[num]
        x_pos = bar.get_x() + bar.get_width() / 2
        plt.text(x_pos, value, f"{value:.2f}", ha='center', va='bottom')

    # Fit a polynomial curve to the data points
    x_fit = np.linspace(min(un_gaps), max(un_gaps), 50)
    co_eff = np.polyfit(un_gaps, no_gaps, 3)
    y_fit = np.polyval(co_eff, x_fit)

    # Plot the smooth curve
    plt.plot(x_fit, y_fit, '-g', lw=0.5)

    plt.show()


# ============================ Bytes to a binary string ================================================================
def b2i(data):                                              # convert bytes to a list of integers
    binary_string = ''                                      # Convert each byte to a binary string and join them
    for byte in data:
        binary_string += bin(byte)[2:].zfill(8)             # convert each byte to binary of 8 characters and append
    integer_list = [int(bit) for bit in binary_string]      # Convert the binary string to a list of integers
    return integer_list


# ============================ Function to test any provided sequence ==================================================
def tests(rnd_seq, markov=0, bm=0, chi=0):
    print("\n===============================================================================")
    print("===============================================================================")
    print("\nThe provided results are different tests to check the generated sequence!\n")
    if isinstance(rnd_seq, bytes):
        rnd_seq = b2i(rnd_seq)

    rnd_seq = [int(bit) for bit in rnd_seq]
    seq_len = len(rnd_seq)

    print("Sequence Length = ", seq_len)

    rnd_zeros = rnd_seq.count(0)
    rnd_ones = rnd_seq.count(1)
    print(f"Random Sequence Balance: 0s= {rnd_zeros}, 1s= {rnd_ones}")

    # Calculate Gap Structures
    rnd_gaps = cal_gaps(rnd_seq)

    # Count and Normalise the gap structure
    rnd_uniq_gaps, rnd_norm_gaps, _ = cal_norm_gaps(rnd_gaps)
    print("\nThe probability of zero gaps in the sequence: ", max(rnd_norm_gaps))
    print("Total Number of Unique gaps in the sequence : ", max(rnd_uniq_gaps), "\n")

    if bm == 1:
        # Burstiness and Memory Coefficient
        burst = burstiness_para.B_Cal(rnd_seq)
        print("Burstiness of the signal         = ", burst)

        memory = memory_coeff.memory_co(rnd_seq)
        print("Memory Coefficient of the signal = ", memory, "\n")

    if markov == 1:
        m_entropy = Markov_Test.markov_test(rnd_seq, 1)
        if 0.712 <= m_entropy <= 1.000:
            print('Passed the Markov Test')

    # Chi-Square Test
    if chi == 1:
        expected_value = 0.5 * seq_len

        score_i, df_i = b_chisquare_ind.bcit(rnd_seq)
        score_g, df_g = b_goodness_of_fit.bgoft(rnd_seq)

        chi, cdf, pdf = chi_test(rnd_zeros, rnd_ones, expected_value)

        if chi < 3.841:
            a = 'value is good! (< 3.841)'
        else:
            a = 'value is not good! (> 3.841)'

        print("\nChi-square test Result of a Random Sequence :", chi, a)
        print("P-value (CDF) of a Random Sequence          :", cdf, "(Should be > 0.05)\n")
        print("\nThe chi-square independence test    = ", score_i, "With degree of freedom = ", df_i)
        print("The chi-square goodness of fit test = ", score_g, "With degree of freedom = ", df_g)

    # Plot the Gap Structures
    plot_histogram(rnd_uniq_gaps, rnd_norm_gaps, "The graph of a random sequence Gap-Structures")


# sequence = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0]
sequence = '0110101111001011100111101000001000001000001010010110100001110111101101100111100100100101011110101011001011101001111111010010010111100001110111000010011011011110001011101100100101110000010001011100010100111001001011101010101011001001000110010000011111110100001000001111100111001001011000011011111011001000100111000010000111011111001011101100101010110001101110101001001100111101010011110111011111001110000110001011110001100001100011111100011001010010101111110010101010100100100001010111100110100111111101011001000011010000011000000111110110011110000101110001011011000000101101111101010111000010000001010001010110011101100110110011101010010001110110110000110111011011001000101100011000101000001110101101100011001100001111110001001000010111111100000001001011010010010001010101000010011001000000110100011000111000001110111111000100111100010100110101100100101011111101111000111010001100110100101100010011001101010101000111010000001111100111110110000101000001001101100001111010000111111000010111110001010101111101011101011001010010110111001100110000011011111000111111011010000110000100111101010001011111101101101000010100010010111000001110100111000100011010001000011111110011010010111011111000101100100110110111010010111111000010001001100000110000011110100100100110001000010111110000110010011010100000001101000001011010010101011111011100010001011011111101000010000000010110101111100000010110011010000111101111000001001001111011110001010010001101100001100100100110100010101000010101010000010100010110010010100011001100111101000010110011001010000011010101110010100110111100110101010100001011101100000111001010101011101011001000010001000010010100001101001000001000100110000101011111001110001111001010000000111110100001010100111010010111111100000011111000100010000110010110101110011001011101111110001011010010111101110010101101100110110010011111011100010001110111111100010001110010101001101110011111110011110110110110010110000111111011011001101001110000001000100100010101100101000101111010001110110010110110010000010001001010010000111101111000001110001100001011101110110000111000110110110111110100110011011001101011001000110111110110100011010001110001100011011000100010101011101110011100011010100010001000100001101111111110010000101100011001100010110001010011111000000010110111101101111010001001101101001111100001111001011001000000101101001101000001110100001110111010111110011001110100100001100010100100101111001111110101000111110011001100000000010001001100000101100001111011100010100101101000001100111011000101001111011001000000001001101100101000011000001010110011111110001100110011010001001000011001110011101000101001010011111000101101110010100110010111100111010001111110011110111011100010100110000111010010000111000010111001000010010111000110001000010001110000101000101000001100110011000111100010110010100001000000100111110110000011110000110100010001000000010111111010101101110011101011001010010100001010001010101010000110000100001101101000011111011110000110101111011000111101001001101010000000010011000010011100001000000010000011111110110000110101100010111100001000101010110011111111011111000010101100110010010101111010110100010011111010110111011100001000011101011110100011101110001101000110110011111100001011111111100000100110101010000111101111110001100011001000100000101010000111010101101010110100100110111000111110111010100011001100111001111010001010110110110110110111010010111101111000001100000101001110110010001010000011101110111000011110011110011000010011101001011011111001011000011011101101001001010001100000011011000100001111001011011010110100111101111101110001111001101101101011000000001010100101101101111101110110110100000100110001110100100111100001110111001011000011111010011010010110001001110101010100101101100001101100011011010110111011000110110011110101010101000111111001001000101010010111010001100100100011010101011100001000010100111100001101100010100111100111001011100000111110111110101110100010110111010001000000011010100100101001001101111011111100111001001100000001100110111001011010000101'
tests(sequence)
