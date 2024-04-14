import matplotlib.pyplot as plt

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
    print("gaps: ", gap)
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

    print("counts: ", counts_, "unique gaps: ", uniq_gaps_, "norm gaps: ", norm_gaps_)
    return uniq_gaps_, norm_gaps_, counts_


# ============================ Graphs ==================================================================================
# Plot the Gap Structures of rnd_seq and M_sequence
def plot_histogram(un_gaps, no_gaps, title=None):
    plt.figure()
    bars = plt.bar(un_gaps, no_gaps, width=0.15, align='center')
    # plt.title(title)
    plt.xlabel("Gap structures (V)")
    plt.ylabel("Gap length")
    plt.grid(True)

    for num in range(len(bars)):        # write the normalised value on top of the bars
        bar = bars[num]
        value = no_gaps[num]
        x_pos = bar.get_x() + bar.get_width() / 2
        plt.text(x_pos, value, f"{value:.2f}", ha='center', va='bottom')

    # # Fit a polynomial curve to the data points
    # x_fit = np.linspace(min(un_gaps), max(un_gaps), 50)
    # co_eff = np.polyfit(un_gaps, no_gaps, 3)
    # y_fit = np.polyval(co_eff, x_fit)
    #
    # # Plot the smooth curve
    # plt.plot(x_fit, y_fit, '-g', lw=0.5)

    plt.show()


# ============================ Function to test any provided sequence ==================================================
def tests(rnd_seq):

    rnd_seq = [int(bit) for bit in rnd_seq]
    seq_len = len(rnd_seq)

    print("Sequence Length = ", seq_len)

    rnd_zeros = rnd_seq.count(0)
    rnd_ones = rnd_seq.count(1)
    print(f"Random Sequence Balance: 0s= {rnd_zeros}, 1s= {rnd_ones}")

    # Calculate Gap Structures
    rnd_gaps = cal_gaps(rnd_seq)

    # Count and Normalise the gap structure
    rnd_uniq_gaps, rnd_norm_gaps, rnd_counts_ = cal_norm_gaps(rnd_gaps)
    print("\nThe probability of zero gaps in the sequence: ", max(rnd_norm_gaps))
    print("Total Number of Unique gaps in the sequence : ", max(rnd_uniq_gaps), "\n")

    # Plot the Gap Structures
    plot_histogram(rnd_uniq_gaps, rnd_counts_, "Gap Structures")


# sequence = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0]
sequence = '111111111100000000000111100001000111111010101000101110011010000010001011011011011111010001101110110101101011111110111110100010001011000111111110000001001011100100111001011111010101101010110101000010111010011001101011110100100101011111000100010101010101010101111001001110001110010001100100111011110110010111111000001110001011011100100000101100000111010100111001111100101110101001111000101001001011011110101011111101110101000000110011001001001000101010000011011110010'
s = [1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
f = [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0]
tests(f)