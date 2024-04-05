
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

def check(seq):
    seq = [int(bit) for bit in seq]
    gaps = cal_gaps(seq)
    x, y, z = cal_norm_gaps(gaps)  # all normalised gaps
    return y