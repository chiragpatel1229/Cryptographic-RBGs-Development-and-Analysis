import matplotlib.pyplot as plt
import scipy.stats as stats
from Tests_NIST import burstiness_para
from Tests_NIST import memory_coeff
from Tests_NIST import Markov_Test
from Tests_NIST import b_chisquare_ind
from Tests_NIST import b_goodness_of_fit


# ======================= Calculate Gap Structures =====================================================================
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


# ==================== Count and Normalise the gap structure ===========================================================
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


# ======================== Chi-Square Test =============================================================================
def chi_test(zeros, ones, expected):
    # using the equation of Chi-Square test
    chi_square = (zeros - expected) ** 2 / expected + (ones - expected) ** 2 / expected

    p_val_cdf = stats.chi2.cdf(chi_square, df=1)    # get the probability value using cumulative distribution function
    p_val_pdf = stats.chi2.pdf(chi_square, df=1)    # df = 1 bcz we have only 0s and 1s

    return chi_square, p_val_cdf, p_val_pdf


# ============================ Graphs ==================================================================================
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
    rnd_uniq_gaps, rnd_norm_gaps = cal_norm_gaps(rnd_gaps)
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

