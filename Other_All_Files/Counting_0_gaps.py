import matplotlib.pyplot as plt
import numpy as np

# the gap structure for all the generated sequences

# ===================================== USER INPUTS ================================================================
# ===================================== USER INPUTS ================================================================

primitive_polynomial_1 = [9, 5, 3, 2]
primitive_polynomial_2 = [9, 8, 7, 2]
sequence_length = 20
initial_state = [1, 0, 0, 1, 1, 1, 0, 0, 1]

# ===================================== USER INPUTS ================================================================
# ===================================== USER INPUTS ================================================================


def generate_m_sequence(polynomial, length, state):

    # Set the shift register with the given initial state
    shift_register = state[:]

    poly = f"{sum([2**i for i in polynomial]) | 1:b}"    # optimisation of upper two lines

    # the number of bits needed to represent the polynomial for further calculation
    num_bits = len(poly) - 1

    # Extract the feedback stages from the polynomial
    feedback_stages = [int(stage) for stage in poly[:].zfill(num_bits)]

    # List to store the generated m-sequence
    m_seq = []

    for _ in range(length):

        # Capture the output bit
        output_bit = shift_register[-1]

        # Calculate the feedback bit using XOR operation
        feedback_bit = sum([feedback_stages[i] * shift_register[-i-1] for i in range(num_bits)]) % 2

        # Shift the register to the right with new input bit and remove the last bit
        shift_register = [feedback_bit] + shift_register[:-1]

        # Append the output bit to the m-sequence
        m_seq.append(output_bit)

    return m_seq, poly


def calculate_gap_structure(sequence):
    gap_structure = []
    current_gap_length = 0
    no_gap = 0                          # when we do not know the first bit is 1 or 0 makes the condition false

    for bit in sequence:
        if bit == 0:
            current_gap_length += 1
        elif bit == 1:                  # finds the 1s in a list start checking for no gaps.
            if no_gap:                  # if there are two continued 1s in a list then append the counter
                gap_structure.append(current_gap_length)    # only increase 0 in every step with no gap
            current_gap_length = 0
            no_gap = 1                  # found the no_gap in the list, it is true.

    return gap_structure


# A function to plot the histogram

def plot_histogram(data, title, x_label, y_label, bar_width=0.2):
    unique_lengths, counts = zip(*[(length, data.count(length)) for length in set(data)])

    # Calculate the relative frequency of each unique length
    total = sum(data)  # Total number of observations
    print("total length =", total)

    rel_freq = [count / total for count in counts]  # Relative frequency in percentage

    plt.figure()
    # bars = plt.bar(unique_lengths, rel_freq, width=bar_width, align='center')
    bars = plt.bar(unique_lengths, rel_freq, width=bar_width, align='center')

    plt.title(title + str(sequence_length) + " bits")
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # for bar, freq in zip(bars, rel_freq): Write the text on top of the bars
    for bar, freq in zip(bars, rel_freq):
        plt.text(bar.get_x() + bar.get_width() / 2, freq, f"{freq:.2f}", ha='center', va='bottom')

    # # Fit a polynomial curve to the data points
    # x_fit = np.linspace(min(unique_lengths), max(unique_lengths), 100)
    # co_eff = np.polyfit(unique_lengths, rel_freq, 3)
    # y_fit = np.polyval(co_eff, x_fit)
    #
    # # Plot the smooth curve
    # plt.plot(x_fit, y_fit, '-g', lw=1)

    plt.tight_layout()


# Generate the m-sequences PN1(k) and PN2(k)
PN1_sequence, poly1 = generate_m_sequence(primitive_polynomial_1, sequence_length, initial_state)
PN2_sequence, poly2 = generate_m_sequence(primitive_polynomial_2, sequence_length, initial_state)

# Calculate the gap structure and density function for PN1 and PN2 sequence
pn1_gap = calculate_gap_structure(PN1_sequence)

pn2_gap = calculate_gap_structure(PN2_sequence)

# print("1. PN1 Gap Length    = ", bit_stream)


# Generate the Gold code sequence by XORing PN1(k) and PN2(k)
# gold_sequence = [(bit1 ^ bit2) for bit1, bit2 in zip(PN1_sequence, PN2_sequence)]
# gold_gap_lengths = calculate_gap_structure(gold_sequence)


# ===================================================================================================
#                   Print the outputs
# ===================================================================================================


# Print the m-sequence for PN1(k)
num_zeros_pn1 = PN1_sequence.count(0)
num_ones_pn1 = PN1_sequence.count(1)
print("1. Primitive polynomial = ", primitive_polynomial_1)
print("1. Binary Polynomial    = ", poly1)
print(f"PN1 sequence of length {sequence_length}: {PN1_sequence}")
print(f"PN1 Balance - 0s: {num_zeros_pn1}, 1s: {num_ones_pn1}")
# print("1. Gap structure    = ", pn1_gap, "\n")

# Print the m-sequence for PN2(k)
# num_zeros_pn2 = PN2_sequence.count(0)
# num_ones_pn2 = PN2_sequence.count(1)
# print("2. Primitive polynomial = ", primitive_polynomial_2)
# print("2. Binary Polynomial    = ", poly2)
# print(f"PN2 sequence of length {sequence_length}: {PN2_sequence}")
# print(f"PN2 Balance - 0s: {num_zeros_pn2}, 1s: {num_ones_pn2}")
# print("1. Gap structure    = ", pn2_gap, "\n")


# Plot histogram for the gap structures of PN1, PN2, and Gold code sequences
plot_histogram(pn1_gap, "Gap Structure of PN1 Sequence with ", "Gap Length", "Count")
# plot_histogram(pn2_gap, "Gap Structure of PN2 Sequence with ", "Gap Length", "Count")
# plot_histogram(gold_gap_lengths, "Gap Function of Gold Code with a ", "Gap Length", "Count")

# Show all plots and keep them open until you manually close them
plt.show()
