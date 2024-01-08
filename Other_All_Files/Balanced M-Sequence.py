import matplotlib.pyplot as plt

# ===================================== USER INPUTS ================================================================

primitive_polynomial = [5, 2]
seq_len = 100
initial_state = [1, 1, 1, 0, 1]

# ===================================== USER INPUTS ================================================================


def generate_m_sequence(polynomial, length, state):

    shift_register = state[:]
    bin_polynomial = bin(sum([2**degree for degree in polynomial]))   # convert polynomial to Binary
    poly = bin_polynomial[2:-1]                             # Remove first two bits '0b' and a lst bit '0'
    num_bits = len(poly)                                    # remove previously added bit
    feedback_stages = [int(f_stage) for f_stage in poly]    # create a list of f_stages using bin_polynomials
    m_seq = []

    for _ in range(length):
        output_bit = shift_register[-1]         # take the right most bit as an output
        bit_counter = 0                         # Initialize feedback bit counter
        for j in range(num_bits):
            bits_at_fb_stages = feedback_stages[j] * shift_register[-j - 1]  # calculate the number of feedback bits
            bit_counter += bits_at_fb_stages    # count the bits for every stage
        bit_counter %= 2                        # XOR operation
        shift_register = [bit_counter] + shift_register[:-1]   # add a first new bit and remove the last bit
        m_seq.append(output_bit)                # Append the output bit to the m-sequence

    return m_seq


# Generate the m-sequences
M_sequence = generate_m_sequence(primitive_polynomial, seq_len, initial_state)
print(M_sequence)
# Print
num_zeros = M_sequence.count(0)
num_ones = M_sequence.count(1)
print(f"Balance - 0s: {num_zeros}, 1s: {num_ones}\n")

# ============  A function to find gap structures ==============================

gap = []
gap_counter = 0
no_gap = 0                  # when we do not know the first bit is 1 or 0 so the condition is false

for bits in M_sequence:
    if bits == 0:
        gap_counter += 1    # calculate the number of continued zeros between two ones
    elif bits == 1:         # finds the 1s in a list start checking for no gaps.
        if no_gap:          # if there are two continued 1s in a list then append the counter
            gap.append(gap_counter)  # add 0s in every step with no gap
        gap_counter = 0     # Reset the counter
        no_gap = 1          # found the no_gap in the list, it is true.

print("gap", gap)
# ==================== gap structure calculation ================================

# find the unique gaps in from the sequence
uniq_gaps = []
counts = []
for unq_gap_len in set(gap):
    count = gap.count(unq_gap_len)           # count repetition of same gaps
    uniq_gaps.append(unq_gap_len)            # find and store the unique gaps
    counts.append(count)                     # Total Number of unique length

print("uniq_gaps", uniq_gaps)

# Normalise the gap structures
total = sum(gap)                         # sum of Gap sequence
norm_gaps = []                           # normalised gap structures
for count in counts:
    normalised = count / total           # normalise every count using total sum of gaps
    norm_gaps.append(normalised)         # store normalised gaps in a list
print("norm_gaps", norm_gaps)

# ===========================  Plot the histogram ==============================

plt.figure()
bars = plt.bar(uniq_gaps, norm_gaps, width=0.15, align='center')
plt.title("Gap Structure of Random Sequence with " + str(seq_len) + " bits")
plt.xlabel("Gap Length")
plt.ylabel("Count")

for i in range(len(bars)):          # Write text on top of the bars
    bar = bars[i]                   # Get the number of bars in the plot
    value = norm_gaps[i]
    x_pos = bar.get_x() + bar.get_width() / 2
    plt.text(x_pos, value, f"{value:.2f}", ha='center', va='bottom')

plt.show()
