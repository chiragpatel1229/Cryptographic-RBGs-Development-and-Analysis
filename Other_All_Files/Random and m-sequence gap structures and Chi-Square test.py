import matplotlib.pyplot as plt
import random
import scipy.stats as stats

# ======================== USER INPUTS ======================================

gaps_probs = [0.4, 0.2, 0.05, 0.05, 0.1]
print("gaps probabilities for random sequence =", gaps_probs, "\n")

seq_len = 1024  # desired Length of the sequence

# =============  Generate random sequence  ======================

rnd_seq = []                            # Generate a random binary sequence using Probabilities
current_len = 0                         # set the counter to the initial state

for i in range(seq_len):
    index = range(len(gaps_probs))      # Get the different gap probabilities from the list
    selected_index = random.choices(index, weights=gaps_probs)  # select index randomly and it's value
    num_gaps = selected_index[0]        # Extract the 0 position bits from the list

    if current_len + num_gaps + 1 <= seq_len:   # keep an eye on the sequence length before extension
        rnd_seq.extend([0] * num_gaps)  # extend the sequence by the selected number of gaps
        rnd_seq.append(1)               # append 1 after adding a selected gaps
        current_len += num_gaps + 1     # update the counter of the sequence length
    else:
        break
if current_len < seq_len:               # Complete the length by adding zeros if not
    rnd_seq.extend([0] * (seq_len - current_len))


# =================== Generate an m-sequence =================================

primitive_polynomial = [5, 2]
initial_state = [1, 1, 1, 0, 1]


def generate_m_sequence(polynomial, length, state):

    state = state[:]
    bin_polynomial = bin(sum([2**degree for degree in polynomial]))   # convert polynomial to Binary
    poly = bin_polynomial[2:-1]                             # Remove first two bits '0b' and a lst bit '0'
    num_bits = len(poly)                                    # remove previously added bit
    feedback_stages = [int(f_stage) for f_stage in poly]    # create a list of f_stages using bin_polynomials
    m_seq = []

    for _ in range(length):
        output_bit = state[-1]         # take the right most bit as an output
        bit_counter = 0                         # Initialize feedback bit counter
        for j in range(num_bits):
            bits_at_fb_stages = feedback_stages[j] * state[-j - 1]  # calculate the feedback bit
            bit_counter += bits_at_fb_stages    # count the bits for every stage
        bit_counter %= 2                        # XOR operation
        state = [bit_counter] + state[:-1]   # add a first new bit and remove the last bit
        m_seq.append(output_bit)                # Append the output bit to the m-sequence

    return m_seq


# Generate the m-sequence
M_sequence = generate_m_sequence(primitive_polynomial, seq_len, initial_state)
# print(M_sequence)
# ======================= Calculate Gap Structures =============================


# Function to calculate gap structures (lengths of consecutive zeros) in a sequence
def cal_gap_str(sequence):
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
rnd_gap_str = cal_gap_str(rnd_seq)
m_gap_str = cal_gap_str(M_sequence)

# ==================== gap structure calculation ================================


def cal_norm_gaps(my_seq):                   # find the unique gaps in the sequence
    uniq_gaps = []
    counts = []
    for unq_gap_len in set(my_seq):
        count = my_seq.count(unq_gap_len)    # count repetition of same gaps
        uniq_gaps.append(unq_gap_len)        # find and store the unique gaps
        counts.append(count)                 # Total Number of unique length

    # Normalise the gap structures
    total = sum(my_seq)                      # sum of Gap sequence
    norm_gaps = []                           # normalised gap structures
    for count in counts:
        normalised = count / total           # normalise every count using total sum of gaps
        norm_gaps.append(normalised)         # store normalised gaps in a list
    return uniq_gaps, norm_gaps


rnd_uniq_gaps, rnd_norm_gaps = cal_norm_gaps(rnd_gap_str)
m_uniq_gaps, m_norm_gaps = cal_norm_gaps(m_gap_str)

# ======================== Chi-Square Test ====================================
rnd_zeros = rnd_seq.count(0)        # counting zeros in the sequence
rnd_ones = rnd_seq.count(1)         # counting ones in the sequence
m_zeros = M_sequence.count(0)       # counting zeros in the sequence
m_ones = M_sequence.count(1)        # counting ones in the sequence

print(f"Random Sequence Balance - 0s= {rnd_zeros}, 1s= {rnd_ones}")
print(f"M-Sequence Balance -      0s= {m_zeros}, 1s= {m_ones} \n")

expected_value = 0.5 * seq_len      # expected values of zeros and ones


def test(zeros, ones, expected):
    # use the equation of Chi-Square test
    chi_square = (zeros - expected) ** 2 / expected + (ones - expected) ** 2 / expected

    p_val_cdf = stats.chi2.cdf(chi_square, df=1)    # get the probability value using cumulative distribution function
    p_val_pdf = stats.chi2.pdf(chi_square, df=1)

    return chi_square, p_val_cdf, p_val_pdf


# Calculate Chi-square test results and p-values for gap structures
rnd_chi, rnd_p_value_cdf, rnd_p_value_pdf = test(rnd_zeros, rnd_ones, expected_value)
m_chi, m_p_value_cdf, m_p_value_pdf = test(m_zeros, m_ones, expected_value)

# Print the results and p-values
print("Chi-square test Result of a Random Sequence :", rnd_chi)
print("P-value (CDF) of a Random Sequence          :", rnd_p_value_cdf)
print("P-value (pDF) of a Random Sequence          :", rnd_p_value_pdf, "\n")
print("Chi-square test Result of a M-sequence :", m_chi)
print("P-value (CDF) of a M-Sequence          :", m_p_value_cdf)
print("P-value (pDF) of a M-Sequence          :", m_p_value_pdf)

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
# plot_histogram(m_uniq_gaps, m_norm_gaps, "The graph of a M-sequence Gap-Structures")
plt.show()
