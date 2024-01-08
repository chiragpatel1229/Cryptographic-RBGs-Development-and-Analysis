import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

# the gap structure and density function for all the generated sequences

# ===================================== USER INPUTS ================================================================
# ===================================== USER INPUTS ================================================================

primitive_polynomial_1 = [5, 3]
primitive_polynomial_2 = [5, 3, 2, 1]
sequence_length = 100
initial_state = [1, 0, 0, 1, 1]

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


# ===================================================================================================
#                   ACF & CCF Function
# ===================================================================================================


def calculate_ccf(ci, cj, v):
    m = len(ci)
    s = 0
    for mu in range(m):
        i = (mu + v) % m
        s += ci[i] * cj[mu]
    return s / m


# ===================================================================================================
#                   Gap Structure Function
# ===================================================================================================


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


# ===================================================================================================
#                   HistoGram Function
# ===================================================================================================


def plot_density_function(seq, data, title, x_label, y_label, bandwidth=None):
    unique_lengths, counts = zip(*[(length, data.count(length)) for length in set(data)])

    # Calculate the relative frequency of each unique length
    total = len(seq)  # Total number of observations
    rel_freq = [count / total * 100 for count in counts]  # Relative frequency in percentage

    plt.figure()
    bars = plt.bar(unique_lengths, rel_freq, width=0.2, align='center')
    plt.title(title + str(sequence_length) + " bits")
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # write the unique number on top of the bars
    for bar, freq in zip(bars, rel_freq):
        plt.text(bar.get_x() + bar.get_width() / 2, freq, f"{freq:.2f}%", ha='center', va='bottom')

    # Density estimation using Gaussian Kernel Density Estimation
    kde = gaussian_kde(data, bw_method=bandwidth)
    x_fit = np.linspace(min(unique_lengths), max(unique_lengths), 100)
    density_estimation = kde(x_fit)

    # Plot the density estimation curve on top of the bars
    plt.plot(x_fit, density_estimation * 20, '-g', lw=1)

    plt.tight_layout()


# ===================================================================================================
#                  Generate PN1, PN2, Gold and Gap Lengths Sequence
# ===================================================================================================


# Generate the m-sequences PN1(k) and PN2(k)
PN1_sequence, poly1 = generate_m_sequence(primitive_polynomial_1, sequence_length, initial_state)
PN2_sequence, poly2 = generate_m_sequence(primitive_polynomial_2, sequence_length, initial_state)

# Generate the Gold code sequence by XORing PN1(k) and PN2(k)
gold_sequence = [(bit1 ^ bit2) for bit1, bit2 in zip(PN1_sequence, PN2_sequence)]

# Calculate the gap structure and density function for PN1 and PN2 sequence
pn1_gap_lengths = calculate_gap_structure(PN1_sequence)
pn2_gap_lengths = calculate_gap_structure(PN2_sequence)
gold_gap_lengths = calculate_gap_structure(gold_sequence)


# ===================================================================================================
#                   Plot Gap Structure Histograms of PN1, PN2 and Gold code sequences
# ===================================================================================================


plot_density_function(PN1_sequence, pn1_gap_lengths, "Gap Function of PN1 Sequence with a ",
                      "Gap Length", "Density (%)", bandwidth=0.23)
# plot_density_function(PN2_sequence, pn2_gap_lengths, "Gap Function of PN2 Sequence with a ",
#                       "Gap Length", "Density (%)", bandwidth=0.23)
# plot_density_function(gold_sequence, gold_gap_lengths, "Gap Function of Gold Code with a ",
#                       "Gap Length", "Density (%)", bandwidth=0.23)


# ===================================================================================================
#                   Print the outputs
# ===================================================================================================


# Print the m-sequence for PN1(k)
num_zeros_pn1 = PN1_sequence.count(0)
num_ones_pn1 = PN1_sequence.count(1)
print("1. Primitive polynomial = ", primitive_polynomial_1)
print("1. Binary Polynomial    = ", poly1)
# print(f"PN1 sequence of length {sequence_length}: {PN1_sequence}")
print(f"PN1 Balance - 0s: {num_zeros_pn1}, 1s: {num_ones_pn1}\n")

# Print the m-sequence for PN2(k)
num_zeros_pn2 = PN2_sequence.count(0)
num_ones_pn2 = PN2_sequence.count(1)
print("2. Primitive polynomial = ", primitive_polynomial_2)
print("2. Binary Polynomial    = ", poly2)
# print(f"PN2 sequence of length {sequence_length}: {PN2_sequence}")
print(f"PN2 Balance - 0s: {num_zeros_pn2}, 1s: {num_ones_pn2}\n")

# Print the Gold code
num_zeros_gold = gold_sequence.count(0)
num_ones_gold = gold_sequence.count(1)
# print(f"Gold sequence of length {sequence_length}: {gold_sequence}")
print(f" Gold Balance - 0s: {num_zeros_gold}, 1s: {num_ones_gold}\n")

# Print the Gap Structures
# print("Gap Length of PN1 sequence: ", bit_stream, "\nGap Length of PN2 sequence: ", pn2_gap_lengths,
#       "\nGap Length of Gold sequence: ", gold_gap_lengths, '\n')


# ===================================================================================================
#                   Plot PN1, PN2, and Gold sequence Graphs
# ===================================================================================================


# # Plot histogram for PN1_sequence
# plt.figure()
# plt.bar(range(len(PN1_sequence)), PN1_sequence, width=0.6, align='edge')
# plt.title("PN1 Sequence")
# plt.xlabel("Bit Location")
# plt.ylabel("Bit Value")
# plt.ylim(0, max(PN1_sequence) + 0.5)
# plt.grid()
#
# # Plot histogram for PN2_sequence
# plt.figure()
# plt.bar(range(len(PN2_sequence)), PN2_sequence, width=0.6, align='edge')
# plt.title("PN2 Sequence")
# plt.xlabel("Bit Location")
# plt.ylabel("Bit Value")
# plt.ylim(0, max(PN2_sequence) + 0.5)
# plt.grid()
#
# # Plot histogram for gold_sequence
# plt.figure()
# plt.bar(range(len(gold_sequence)), gold_sequence, width=0.6, align='edge')
# plt.title("Gold Sequence")
# plt.xlabel("Bit Location")
# plt.ylabel("Bit Value")
# plt.ylim(0, max(gold_sequence) + 0.5)
# plt.grid()


# ===================================================================================================
#                   ACF and CCF Graphs
# ===================================================================================================


# # Calculate the Cross-Correlation Function (CCF) of PN1 and PN2
# ccf_values = []
# for v in range(sequence_length):
#     ccf = calculate_ccf(PN1_sequence, PN2_sequence, v)
#     ccf_values.append(ccf)
#
# # Plot histogram for the normalized Cross-Correlation Function (CCF) of PN1 and PN2
# plot_density_function(ccf_values, "Normalized Cross-Correlation of PN1 and PN2",
#                       "Shift Value (v)", "CCF Value", bandwidth=0.17)
#
#
# # Calculate the Auto-Correlation Function (ACF) of the Gold code sequence
# gold_sequence_acf = []
# for v in range(sequence_length):
#     acf = calculate_ccf(gold_sequence, gold_sequence, v)
#     gold_sequence_acf.append(acf)
#
# # Plot histogram for the Auto-Correlation Function (ACF) of the Gold code sequence
# plot_density_function(gold_sequence_acf, "Auto-Correlation of Gold Code",
#                       "Shift Value (v)", "ACF Value", bandwidth=0.17)

# Show all plots and keep them open until you manually close them
plt.show()
