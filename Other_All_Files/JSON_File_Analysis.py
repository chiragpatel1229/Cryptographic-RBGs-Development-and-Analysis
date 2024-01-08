import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import json

# the gap structure and density function for all the generated sequences

# ===================================== USER INPUTS ================================================================
# ===================================== USER INPUTS ================================================================

file_path = r"C:\Users\Chirag Patel\OneDrive\CRYPTOGRAPHY\Reports\RNG json files\Hash_SHA_256_1.json"
with open(file_path, 'r') as bits:
    # bits = open('Random sequence of 21000 bits.json', 'r')   # open the json file to just read the data
    data = json.load(bits)  # read the binary data from the file

# Convert the binary sequence string to a list of integers
bit_stream = []
for bits in data:
    bit_integer = int(bits)
    bit_stream.append(bit_integer)

# bit_stream = [int(bit) for bit in data]


# count the number of bits in the .Json file
num_bits = len(bit_stream)


# ===================================================================================================
#                   HistoGram Function
# ===================================================================================================


def plot_density_function(seq, gap_len, title, x_label, y_label, bandwidth=None):
    unique_lengths, counts = zip(*[(length, gap_len.count(length)) for length in set(gap_len)])

    # Calculate the relative frequency of each unique length
    total = len(seq)  # Total number of observations
    rel_freq = [count / total * 100 for count in counts]  # Relative frequency in percentage

    plt.figure()
    bars = plt.bar(unique_lengths, rel_freq, width=0.2, align='center')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # write the unique number on top of the bars
    for bar, freq in zip(bars, rel_freq):
        plt.text(bar.get_x() + bar.get_width() / 2, freq, f"{freq:.2f}%", ha='center', va='bottom')

    # Density estimation using Gaussian Kernel Density Estimation
    kde = gaussian_kde(gap_len, bw_method=bandwidth)
    x_fit = np.linspace(min(unique_lengths), max(unique_lengths), 100)
    density_estimation = kde(x_fit)

    # Plot the density estimation curve on top of the bars
    plt.plot(x_fit, density_estimation * 25, '-g', lw=1)

    plt.tight_layout()


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
#                   ACF Function
# ===================================================================================================


def calculate_acf(ci, cj, v_bits):
    m = len(ci)
    s = 0
    for mu in range(m):
        i = (mu + v_bits) % m
        s += ci[i] * cj[mu]
    return s / m

# def calculate_acf(stream, num):
#     M = len(stream)
#     c = np.zeros(M, dtype=np.complex64)
#
#     for i, bit in enumerate(stream):
#         if bit == 'O':
#             c[i] = 1
#         elif bit == 'I':
#             c[i] = -1j
#
#     acf = np.zeros(num, dtype=np.complex64)
#
#     for v in range(num):
#         for mu in range(M):
#             acf[v] += c[(mu + v) % M] * c[mu]
#
#         acf[v] /= M
#
#     return acf


# ===================================================================================================
#                   Calculate the gap structure for bit stream
# ===================================================================================================

bit_stream_gap = calculate_gap_structure(bit_stream)


# ===================================================================================================
#                   Plot Gap Structure Histograms of sequences
# ===================================================================================================

plot_density_function(bit_stream, bit_stream_gap,  "Gap & Density Function of bit stream ",
                      "Gap Length", "Density (%)", bandwidth=0.23)


# ===================================================================================================
#                            ACF of the Bit_stream
# ===================================================================================================
acf_seq = []
for v in range(num_bits):
    acf = calculate_acf(bit_stream, bit_stream, v)
    acf_seq.append(acf)

plt.figure()
plt.bar(list(range(len(acf_seq))), acf_seq, width=0.3)
plt.title('ACF of a Random Sequence')
plt.xlabel('Shift Value (v)')
plt.ylabel('ACF Value')


# ===================================================================================================
#                                   Print the outputs
# ===================================================================================================


# Print the m-sequence for PN1(k)
num_zeros = bit_stream.count(0)
num_ones = bit_stream.count(1)
print(f"Bit_stream Balance - 0s: {num_zeros}, 1s: {num_ones}")

plt.show()
