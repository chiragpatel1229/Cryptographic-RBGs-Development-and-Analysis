import matplotlib.pyplot as plt
import os


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


# Function to read sequences from a .txt file ==========================================================================
def read_sequences(file_name_):
    with open(file_name_, 'r') as file:                      # open the file in a read mode
        _sequences = []                                      # set a buffer to store the sequences
        for line in file:
            stripped_line = line.strip()                     # extract each sequence as a separate line
            mapped_line = list(map(int, stripped_line))      # convert each line to the list of integers
            _sequences.append(mapped_line)                   # append each sequence as a list to the buffer
    return _sequences                                        # return the list of sequences


# Function to calculate norm_gaps and uniq_gaps of each sequence =======================================================
def get_norm_gaps(seq_):
    all_norm_gaps = []                                          # set a buffer to store the normalised gaps
    for sequence in seq_:
        gaps = cal_gaps(sequence)                               # find the gaps from each sequence
        u_gaps, norm_gaps, count = cal_norm_gaps(gaps)          # collect only normalised gaps
        all_norm_gaps.append(norm_gaps)   # set them with a descending order to ease the further part
    return all_norm_gaps


# Function to get particular gap lengths from the list of sequences ====================================================
def get_selected_gap(seq_list, gap_index_value):
    sel_gaps = []
    for n in seq_list:
        if gap_index_value < len(n):  # Check if gap_index_value is a valid index for n
            sel_gaps.append(n[gap_index_value])
        else:
            sel_gaps.append(0)  # Append a default value if gap_index_value is not a valid index
    return sel_gaps


# Function to get particular gap lengths from the list of sequences ====================================================
def get_all_gaps(seq_list):

    lengths = []                            # Initialize an empty list to store the lengths
    for n in seq_list:
        sequence_length = len(n)            # Get the length of the current sequence
        lengths.append(sequence_length)     # Append the length to the lengths list

    max_length = max(lengths)               # Get the maximum length from the lengths list

    max_gap_index = max_length - 1          # Subtract 1 from the maximum length to get the maximum gap index

    all_gaps = []
    for gap_index in range(max_gap_index + 1):  # Loop through each gap index
        gap_values = get_selected_gap(seq_list, gap_index)
        all_gaps.append(gap_values)
    return all_gaps


# Function to plot the normalized gap length of 0 and 1 for all sequences ==============================================
def plot_GDF_zeros(norm_gaps_zero, f_name=None):
    avg_norm_gap_zero = sum(norm_gaps_zero) / len(norm_gaps_zero)
    plt.figure()
    plt.plot(norm_gaps_zero, label=f'Expected = 0.50\nAvg. = {avg_norm_gap_zero:.5f}')
    plt.axhline(y=0.5, color='r', linestyle='-', linewidth=1)  # Horizontal line at y = 0.5
    plt.axhline(y=avg_norm_gap_zero, color='g', linestyle='-', linewidth=1)  # Horizontal line at average value
    plt.text(0, avg_norm_gap_zero, f'Avg: {avg_norm_gap_zero:.2f}', color='b', va='bottom')  # Add average value label
    plt.title(f"Normalized length of 0 gap for {f_name}")
    plt.xlabel("Sequence Number")
    plt.ylabel("Normalized Gap Length")
    plt.legend()


# Function to plot the boxes for normalized gaps =======================================================================
def plot_boxplot(all_norm_gaps, f_name=None):
    # Transpose the list of all normalized gaps
    transposed_gaps = list(map(list, zip(*all_norm_gaps)))

    plt.figure()
    plt.boxplot(transposed_gaps, showfliers=True)  # Show individual data points

    # Add individual data points to the plot ===========================================================================
    # Start the enumeration from 1
    i = 1
    # Iterate over each item in transposed_gaps
    for norm_gaps in transposed_gaps:
        # Create a list of 'i' repeated len(norm_gaps) times
        x_values = [i] * len(norm_gaps)
        # Plot the data points
        plt.plot(x_values, norm_gaps, 'rx', alpha=0.3)
        # Increment the counter
        i += 1

    plt.title(f"{f_name} RBG analysis with GDF")
    plt.xlabel("Gap Lengths")
    plt.ylabel("Normalized (V)")
    plt.savefig(f"Boxplot_{f_name}.png")




# Use the functions ====================================================================================================
file_names = ['../RBG_data_files/QRNG.txt',
              '../RBG_data_files/AES.txt',
              '../RBG_data_files/ChaCha20.txt', '../RBG_data_files/CTR.txt',
              '../RBG_data_files/Hash.txt',
              '../RBG_data_files/HMAC.txt', '../RBG_data_files/M_sequences.txt',
              '../RBG_data_files/RC4.txt', '../RBG_data_files/RSA.txt',
              '../RBG_data_files/Synthetic.txt', '../RBG_data_files/bit-flip_Model.txt',
              '../RBG_data_files/Ideal_model.txt', '../RBG_data_files/thermal_Model.txt']



for file_name in file_names[4:5]:
    # get the file names
    b_n = os.path.basename(file_name)           # Extract only the file name
    base_name = os.path.splitext(b_n)[0]        # Remove file extension

    sequences = read_sequences(file_name)       # collect All the sequences
    ang = get_norm_gaps(sequences)              # all normalised gaps

    # transposed_gaps = list(map(list, zip(*ang)))
    # print(transposed_gaps)
    # get_gap0 = get_selected_gap(ang, 0)
    # get_gap1 = get_selected_gap(ang, 1)

    # plot_GDF_zeros(get_gap0, base_name)
    # plt.savefig(f"Zeros_{base_name}.png")

    plot_boxplot(ang, base_name)


plt.show()
