import matplotlib.pyplot as plt
import random
import scipy.stats as stats

# ======================== USER INPUTS ======================================

gaps_probs = [0.4, 0.1, 0.05, 0.05, 0.1, 0.05]
print("gaps probability =", gaps_probs)

seq_len = 1024  # desired Length of random sequence

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
    rnd_seq.extend([1] * (seq_len - current_len))


# ======================= Print the outputs ====================================

zeros = rnd_seq.count(0)        # counting zeros in the sequence
ones = rnd_seq.count(1)         # counting ones in the sequence
print(f"Balance - 0s= {zeros}, 1s= {ones}")
# print(f"sequence of length {seq_len}: {rnd_seq}")
# print("Gap structure    = ", seq_gap, "\n")


# ======================= Chi-Square Test ====================================

expected_value = 0.5 * seq_len                      # expected values of zeros and ones

# use the equation of Chi-Square test
chi_square = (zeros - expected_value)**2 / expected_value + (ones - expected_value)**2 / expected_value

p_value = stats.chi2.cdf(chi_square, df=1)          # get the probability value using cumulative distribution function


print("Chi-square test Result:", chi_square)        # results
print("P-value:", p_value)                          # results


# ============  A function to find gap structures ==============================

gap = []
gap_counter = 0
no_gap = 0                  # when we do not know the first bit is 1 or 0 so the condition is false

for bits in rnd_seq:
    if bits == 0:
        gap_counter += 1    # calculate the number of continued zeros between two ones
    elif bits == 1:         # finds the 1s in a list start checking for no gaps.
        if no_gap:          # if there are two continued 1s in a list then append the counter
            gap.append(gap_counter)  # add 0s in every step with no gap
        gap_counter = 0     # Reset the counter
        no_gap = 1          # found the no_gap in the list, it is true.


# ==================== gap structure calculation ================================

# find the unique gaps in from the sequence
uniq_gaps = []
counts = []
for unq_gap_len in set(gap):
    count = gap.count(unq_gap_len)           # count repetition of same gaps
    uniq_gaps.append(unq_gap_len)            # find and store the unique gaps
    counts.append(count)                     # Total Number of unique length


# Normalise the gap structures
total = sum(gap)                         # sum of Gap sequence
norm_gaps = []                           # normalised gap structures
for count in counts:
    normalised = count / total           # normalise every count using total sum of gaps
    norm_gaps.append(normalised)         # store normalised gaps in a list


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