# @title Control only no gaps
import matplotlib.pyplot as plt
# import numpy as np
import random

# ======================== USER INPUTS ======================================

# prob = 0.4    # Set a probability of no gaps / 0 gaps

seq_len = 5000  # desired Length of random sequence


# ============  A function to find gap structures ==============================

def gap(sequence):              # find gaps in the sequence
    gaps = []
    gap_counter = 0
    no_gap = 0                  # when we do not know the first bit is 1 or 0 so the condition is false

    for bits in sequence:
        if bits == 0:
            gap_counter += 1
        elif bits == 1:         # finds the 1s in a list start checking for no gaps.
            if no_gap:          # if there are two continued 1s in a list then append the counter
                gaps.append(gap_counter)  # add 0s in every step with no gap
            gap_counter = 0     # Reset the counter
            no_gap = 1          # found the no_gap in the list, it is true.

    return gaps


# ============  A function to plot the histogram ==============================

def plot_histogram(data, title, x_label, y_label, bar_width=0.2):

    plt.figure()
    bars = plt.bar(uniq_gaps, data, width=bar_width, align='center')
    plt.title(title + str(seq_len) + " bits")
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    for i in range(len(bars)):          # Write text on top of the bars
        bar = bars[i]
        value = data[i]
        x_pos = bar.get_x() + bar.get_width() / 2
        plt.text(x_pos, value, f"{value:.2f}", ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


# =============  A function to generate random sequence  ======================

def g_seq(length, probability):      # generate a random sequence
    sequence = []
    for i in range(length):
        num_gaps = random.randint(0, 5)     # Generate random numbers between 1-5
        sequence.extend([1] * num_gaps)
        if random.random() < probability:
            sequence.append(1)
        else:
            sequence.append(0)
    return sequence


# ======================= Call the functions ====================================

prob = 0.3                          # Set a probability of no gaps / 0 gaps
rnd_seq = g_seq(seq_len, prob)      # Generate a random binary sequence

seq_gap = gap(rnd_seq)              # Calculate the gap structure

# ==================== gap structure calculation ================================

# find the unique gaps in from the sequence
uniq_gaps = []
counts = []
for unq_gap_len in set(seq_gap):
    count = seq_gap.count(unq_gap_len)       # count repetition of same gaps
    uniq_gaps.append(unq_gap_len)            # find and store the unique gap values
    counts.append(count)                     # store total Number of unique length


# Normalise the gap structures
total = sum(seq_gap)                     # sum of Gap sequence
norm_gaps = []                           # normalised gap structures
for count in counts:
    normalised = count / total           # normalise every count using total sum of gaps
    norm_gaps.append(normalised)         # store normalised gaps in a list

# ======================= Print the outputs ====================================

# Print the m-sequence for PN1(k)
zeros = rnd_seq.count(0)
ones = rnd_seq.count(1)
# print(f"sequence of length {seq_len}: {rnd_seq}")
print(f"Balance - 0s= {zeros}, 1s= {ones}")
# print("Gap structure    = ", seq_gap, "\n")

# ======================= Plot the outputs ====================================

plot_histogram(norm_gaps, "Gap Structure of PN1 Sequence with ", "Gap Length", "Count")

