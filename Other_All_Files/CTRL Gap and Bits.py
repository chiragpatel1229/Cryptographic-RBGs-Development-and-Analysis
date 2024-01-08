# import numpy as np
import copy
import matplotlib.pyplot as plt
import random
# import secrets
# import os


seq_len = 1024      # sequence length
zero_prob = 0.35     # Probability of generating a zero

# ======================= OS.Urandom Generator =============================


class PRBSGenerator:
    def __init__(self, seed, feedback, probability_of_no_gaps):
        self.seed = seed
        self.feedback = feedback
        self.probability_of_no_gaps = probability_of_no_gaps
        self.current_state = seed

    def generate(self):
        next_bit = self.current_state ^ (self.current_state >> self.feedback)
        self.current_state = (self.current_state << 1) | next_bit
        if random.random() < self.probability_of_no_gaps:
            return next_bit & 1  # Ensure the output is 0 or 1
        else:
            return None


def generate_sequence(generator, length):
    sequence = []
    while len(sequence) < length:
        bit = generator.generate()
        if bit is not None:
            sequence.append(bit)
    return sequence


generator = PRBSGenerator(seed=65485, feedback=3, probability_of_no_gaps=0.35)
rnd_seq = generate_sequence(generator, length=1000)
print(rnd_seq, "\nlen: ", len(rnd_seq))


# ======================= OS.Urandom Generator =============================


# def os_rnd_RNG(seq_length):
#     number_of_bytes = (seq_length + 7) // 8        # Convert seq_len to bytes
#     rnd_seed = os.urandom(number_of_bytes)      # Generate required random bytes
#     bin_seq = ''                                # Create empty string for binary list
#     for byte in rnd_seed:
#         binary_byte = format(byte, '08b')       # Convert bytes into binary with by leading zeros and 8 bit width
#         bin_seq += binary_byte                  # Append the bits into the string
#
#     bin_seq = bin_seq[:seq_length]                 # Consider only required sequence length
#     rnd_sequence = [int(bit) for bit in bin_seq]    # Convert string to integer list
#     secrets.SystemRandom().shuffle(rnd_sequence)    # Shuffle the sequence securely
#     return rnd_sequence
#
#
# rnd_seq = os_rnd_RNG(seq_len)
# print("rnd: ", rnd_seq, "length", len(rnd_seq))

# ======================= a list of ones in the sequences =============================

# rnd_seq = [1] * seq_len
#
# # ========================================================================== control bits in the random sequence ================================================================================
#
#
# def ctrl_0s_1s(sequence, prob):                          # Control the occurrence of zeros and ones in the sequence
#     one_prob = 1 - prob                                  # calculate occurrence of Ones
#     n_seq = []                                           # Create empty list for new sequence
#
#     for bit in sequence:
#         if bit == 0 and np.random.rand() > prob:         # check the present bit = 0 and random float is > prob
#             n_seq.append(1)                              # if YES, update a new bit
#         elif bit == 1 and np.random.rand() > one_prob:   # check the present bit = 1 and random float is > prob
#             n_seq.append(0)                              # if YES, update a new bit
#         else:
#             n_seq.append(bit)                            # Otherwise keep the original value
#
#     # secrets.SystemRandom().shuffle(n_seq)                # Shuffle the sequence securely
#     return n_seq
#
#
# rnd_seq = ctrl_0s_1s(rnd_seq1, zero_prob)                # generate a controlled sequence
print("Ctrl. length", len(rnd_seq))

rnd_zeros = rnd_seq.count(0)                # counting zeros in the sequence
rnd_ones = rnd_seq.count(1)                 # counting ones in the sequence
print(f"Controlled Random Sequence Balance - 0s= {rnd_zeros}, 1s= {rnd_ones}")

# ========================================================================== count only no gaps between two continued ones ==========================================================================
""" Here, it is possible to find a specific gap length using this function, if a gap of 3 continued zero needs to be
    found, change 'if num == 1 to 0' and 'con_one >= 3', so it will find all the gaps with 3 continued zeros in the sequence. """


def cnt_no_gap(my_seq):                 # count no gaps in the sequence
    no_g_cntr = 0                       # Initialise the 'no gap counter' to zero
    con_one = 0                         # 'continued ones' counter set to zero
    for num in my_seq:
        if num == 1:
            con_one += 1                # Increase the counter for every single continued ones
        else:
            con_one = 0                 # if there is zero in the sequence, reset the continued ones counter

        if con_one >= 2:                # Start appending the counter after neglecting first '1' to consider a gap
            no_g_cntr += 1
    return no_g_cntr


# c_p = cnt_no_gap(rnd_seq)             # 'current probability' of no gaps in the sequence

# ========================================================================== control/Adjust no gaps in the sequence ==========================================================================


def ad_no_gaps(my_se, d_prob):                  # Adjust desired no gaps in the sequence
    c_p = cnt_no_gap(my_se) / sum(my_se)        # 'current probability' of no gaps in the sequence

    while c_p != d_prob:                        # enter the while loop if the current no gaps != desired no gaps

        if c_p < d_prob:                        # Increase no gaps by replacing zeros with ones
            zero_at_i = []                      # Create an empty list to store places of zeros in the sequence
            for i, num in enumerate(my_se):
                if num == 0:                    # Check if the current element 'num' is 0
                    zero_at_i.append(i)         # If yes, add the index 'i' to the 'zero_at_i' list
            if not zero_at_i:                   # if there is no zero in the sequence, break the loop
                break

            # sel_rnd_i = secrets.randbelow(len(zero_at_i))       # select random places to replace zeros to ones
            sel_rnd_i = random.choice(zero_at_i)
            my_se[sel_rnd_i] = 1                                # Replace the zero with one
            my_se[(sel_rnd_i + 1) % len(my_se)] = 0             # Manage the bits balance in the sequence

        else:                                                   # Reduce no gaps by replacing ones with zeros
            one_at_i = []
            for i, num in enumerate(my_se):                     # iterate through every index and value
                if num == 1:                                    # Check if the current element 'num' is 1
                    one_at_i.append(i)                          # If yes, add the index 'i' to the 'one_at_i' list
            if len(one_at_i) < 2:                               # if there is only single or no one in the sequence, break the loop
                break

            # sel_rnd_i = secrets.randbelow(len(one_at_i))        # select random places to replace ones to zeros
            sel_rnd_i = random.choice(one_at_i)
            my_se[sel_rnd_i] = 0                                # two zeros should be added to manage the no gaps
            my_se[(sel_rnd_i + 1) % len(my_se)] = 1             # manage the bits balance in the sequence

        c_p = cnt_no_gap(my_se) / sum(my_se)                    # again check the current no gaps in the sequence

    return my_se


prob = 0.45                                                 # desired probability for no gaps in the sequence
seq_copy = copy.deepcopy(rnd_seq)                           # Create a copy of rnd_seq
adj_seq = ad_no_gaps(seq_copy, prob)                        # A sequence with Adjusted/controlled no gaps
# print("ad:  ", adj_seq)
print("Ad. length", len(adj_seq))

ct_rnd_zeros = adj_seq.count(0)                                 # counting zeros in the controlled gap sequence
ct_rnd_ones = adj_seq.count(1)                                  # counting ones in the controlled gap sequence
print(f"Adjusted Random Sequence Balance - 0s= {ct_rnd_zeros}, 1s= {ct_rnd_ones} \n")


# ========================================================================== Calculate Gap Structures ==========================================================================


def cal_gaps(sequence):
    gap = []
    gap_counter = 0
    no_gap = 0                          # when we do not know the first bit is 1 or 0 so the condition is false

    for bits in sequence:
        if bits == 0:
            gap_counter += 1            # calculate the number of continued zeros between two ones
        elif bits == 1:                 # finds the 1s in a list start checking for no gaps.
            if no_gap:                  # if there are two continued 1s in a list then append the counter
                gap.append(gap_counter)  # add 0s in every step with no gap
            gap_counter = 0             # Reset the counter
            no_gap = 1                  # found the no_gap in the list, it is true
    return gap


# Calculate gap structures for rnd_seq and M_sequence
rnd_gaps = cal_gaps(rnd_seq)
ad_rnd_gaps = cal_gaps(adj_seq)
# print("rnd gap:    ", rnd_gaps, "\nad_rnd gap: ", ad_rnd_gaps)

# ========================================================================== Count and Normalise the gap structure ==========================================================================


def cal_norm_gaps(my_seq, o_seq):                   # find the unique gaps in the sequence
    uniq_gaps = []
    counts = []
    for unq_gap_len in set(my_seq):
        count = my_seq.count(unq_gap_len)   # count repetition of same gaps
        uniq_gaps.append(unq_gap_len)       # find and store the unique gaps
        counts.append(count)                # Total Number of similar gaps

    # Normalise the gap structures
    total = sum(o_seq)                     # sum of Gap sequence
    norm_gaps = []                          # normalised gap structures
    for count in counts:
        normalised = count / total          # normalise every count using total sum of gaps
        norm_gaps.append(normalised)        # store normalised gaps in a list

    return uniq_gaps, norm_gaps


rnd_uniq_gaps, rnd_norm_gaps = cal_norm_gaps(rnd_gaps, rnd_seq)
ad_rnd_uniq_gaps, ad_rnd_norm_gaps = cal_norm_gaps(ad_rnd_gaps, adj_seq)
# print("r_u_g: ", rnd_uniq_gaps, "\nr_n_g: ", rnd_norm_gaps)
# print("a_r_u_g: ", ad_rnd_uniq_gaps, "\na_r_n_g: ", ad_rnd_norm_gaps)

# ========================================================================== Graphs ==========================================================================


# Plot the Gap Structures of rnd_seq and M_sequence
def plot_histogram(uniq_gaps, norm_gaps, title):
    plt.figure()
    bars = plt.bar(uniq_gaps, norm_gaps, width=0.15, align='center')
    plt.title(title)
    plt.xlabel("Gap Length")
    plt.ylabel("Count")

    for num in range(len(bars)):            # write the normalised value on top of the bars
        bar = bars[num]
        value = norm_gaps[num]
        x_pos = bar.get_x() + bar.get_width() / 2
        plt.text(x_pos, value, f"{value:.2f}", ha='center', va='bottom')


plot_histogram(rnd_uniq_gaps, rnd_norm_gaps, "The graph of a Controlled random sequence Gap-Structures")
plot_histogram(ad_rnd_uniq_gaps, ad_rnd_norm_gaps, "The graph of a Adjusted random sequence Gap-Structures")
plt.show()
