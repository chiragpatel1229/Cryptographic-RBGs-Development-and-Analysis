import matplotlib.pyplot as plt
import numpy as np

# the gap structure for all the generated sequences

# ===================================== USER INPUTS ================================================================
# ===================================== USER INPUTS ================================================================

primitive_polynomial_1 = [9, 5, 3, 2]
primitive_polynomial_2 = [9, 8, 7, 2]
sequence_length = 15872
initial_state = [1, 0, 0, 1, 1, 1, 0, 0, 1]

# ===================================== USER INPUTS ================================================================
# ===================================== USER INPUTS ================================================================


def generate_m_sequence(polynomial, length, state):

    shift_register = state[:]
    bin_polynomial = bin(sum([2**x for x in polynomial]))   # convert polynomial to Binary
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

    return m_seq, poly


def calculate_gap_structure(sequence):
    gap_lengths = []
    current_gap_length = 0

    for bit in sequence:
        if bit == 0:
            current_gap_length += 1
        elif current_gap_length > 0:
            gap_lengths.append(current_gap_length)
            current_gap_length = 0

    return gap_lengths


# A function to plot the histogram

def plot_histogram(real_seq_len, data, title, x_label, y_label, bar_width=0.2):
    unique_lengths, counts = zip(*[(length, data.count(length)) for length in set(data)])

    # Calculate the relative frequency of each unique length
    total = len(real_seq_len)  # Total number of observations
    print("total length =", total)

    rel_freq = [count / total * 100 for count in counts]  # Relative frequency in percentage

    plt.figure()
    # bars = plt.bar(unique_lengths, rel_freq, width=bar_width, align='center')
    bars = plt.bar(unique_lengths, counts, width=bar_width, align='center')

    plt.title(title + str(sequence_length) + " bits")
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # for bar, freq in zip(bars, rel_freq): Write the text on top of the bars
    for bar, freq in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, freq, f"{freq:.2f}%", ha='center', va='bottom')

    # # Fit a polynomial curve to the data points
    x_fit = np.linspace(min(unique_lengths), max(unique_lengths), 100)
    co_eff = np.polyfit(unique_lengths, rel_freq, 3)
    y_fit = np.polyval(co_eff, x_fit)

    # Plot the smooth curve
    # plt.plot(x_fit, y_fit, '-g', lw=1)

    plt.tight_layout()


# Generate the m-sequences PN1(k) and PN2(k)
PN1_sequence, poly1 = generate_m_sequence(primitive_polynomial_1, sequence_length, initial_state)
PN2_sequence, poly2 = generate_m_sequence(primitive_polynomial_2, sequence_length, initial_state)

# Calculate the gap structure and density function for PN1 and PN2 sequence
pn1_gap_lengths = calculate_gap_structure(PN1_sequence)
pn2_gap_lengths = calculate_gap_structure(PN2_sequence)

# print("1. PN1 Gap Length    = ", bit_stream)


# Generate the Gold code sequence by XORing PN1(k) and PN2(k)
gold_sequence = [(bit1 ^ bit2) for bit1, bit2 in zip(PN1_sequence, PN2_sequence)]
gold_gap_lengths = calculate_gap_structure(gold_sequence)

# Plot histogram for the gap structures of PN1, PN2, and Gold code sequences
plot_histogram(PN1_sequence, pn1_gap_lengths, "Gap Function of PN1 Sequence with a ", "Gap Length", "Count")
# plot_histogram(pn2_gap_lengths, "Gap Function of PN2 Sequence with a ", "Gap Length", "Count")
# plot_histogram(gold_gap_lengths, "Gap Function of Gold Code with a ", "Gap Length", "Count")

# Show all plots and keep them open until you manually close them
plt.show()
