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
    # print("gaps: ", gap)
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

    # print("counts: ", counts, "unique gaps: ", uniq_gaps_, "norm gaps: ", norm_gaps_)
    return uniq_gaps_, norm_gaps_, counts_


# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================

# Function to read sequences from a .txt file ==========================================================================
def read_sequences(file_name):
    with open(file_name, 'r') as file:                      # open the file in a read mode
        sequences = []                                      # set a buffer to store the sequences
        for line in file:
            stripped_line = line.strip()                    # extract each sequence as a separate line
            mapped_line = list(map(int, stripped_line))     # convert each line to the list of integers
            sequences.append(mapped_line)                   # append each sequence as a list to the buffer
    return sequences                                        # return the list of sequences


# Function to calculate norm_gaps and uniq_gaps of each sequence =======================================================
def get_norm_gaps(sequences):
    all_norm_gaps = []                                          # set a buffer to store the normalised gaps
    for sequence in sequences:
        gaps = cal_gaps(sequence)                               # find the gaps from each sequence
        u_gaps, norm_gaps, count = cal_norm_gaps(gaps)          # collect only normalised gaps
        all_norm_gaps.append(sorted(norm_gaps, reverse=True))   # set them with a descending order to ease the further part
    return all_norm_gaps


# Function to plot the normalized gap length of 0 and 1 for all sequences ==============================================
def plot_norm_gaps_zero(all_norm_gaps):
    norm_gaps_zero = [norm_gaps[0] if len(norm_gaps) > 0 else 0 for norm_gaps in all_norm_gaps]
    norm_gaps_one = [norm_gaps[1] if len(norm_gaps) > 1 else 0 for norm_gaps in all_norm_gaps]
    plt.figure()
    plt.plot(norm_gaps_zero, label='Gap Length 0', marker='.')
    plt.plot(norm_gaps_one, label='Gap Length 1')
    plt.axhline(y=0.5, color='r', linestyle='-', linewidth=1)  # Add a horizontal line at y = 50
    plt.title("Normalized Gap Length of 0 and 1 for All Sequences with 512-bits")
    plt.xlabel("Sequence Number")
    plt.ylabel("Normalized Gap Length")
    plt.legend()


# Use the functions ====================================================================================================
file_name1 = '../data/Ideal_seq.txt'
file_name2 = '../data/Flip_bit_seq.txt'
file_name3 = '../data/Thermal_seq.txt'

s1 = read_sequences(file_name1)
ang1 = get_norm_gaps(s1)            # all normalised gaps
plot_norm_gaps_zero(ang1)

s2 = read_sequences(file_name2)
ang2 = get_norm_gaps(s2)
plot_norm_gaps_zero(ang2)

s3 = read_sequences(file_name3)
ang3 = get_norm_gaps(s3)
plot_norm_gaps_zero(ang3)
plt.show()
