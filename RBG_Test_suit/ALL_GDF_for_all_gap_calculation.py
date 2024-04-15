import matplotlib.pyplot as plt
import os
import numpy as np


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
    len_gaps = []                                          # set a buffer to store the normalised gaps
    for sequence in seq_:
        gaps = cal_gaps(sequence)                               # find the gaps from each sequence
        a, b, c = cal_norm_gaps(gaps)
        len_gaps.append(b)   # set them with a descending order to ease the further part
    return len_gaps


def mse(actual, pred):
    # Convert inputs to numpy arrays
    actual_array = np.array(actual)
    pred_array = np.array(pred)

    # Calculate the squared error
    squared_error = np.square(np.subtract(actual_array, pred_array))

    # Calculate the mean squared error
    mean_squared_error = squared_error.mean()

    return mean_squared_error


# Function to get particular gap lengths from the list of sequences ====================================================
def get_selected_gap(seq_list, gap_index_value):
    sel_gaps_in = []
    sel_gaps_out = []

    for n in seq_list:
        sel_gaps_in.append(n[gap_index_value])

        if 0.45 < n[gap_index_value] < 0.55:
            sel_gaps_out.append(0)
        else:
            sel_gaps_out.append(n[gap_index_value])

    return sel_gaps_in, sel_gaps_out

# Function to plot the normalized gap length of 0 and 1 for all sequences ==============================================
def plot_GDF_zeros(g_in, g_out, f_name=None):
    avg_norm_gap_zero = sum(g_in) / len(g_in)
    # print(f"{f_name}: {avg_norm_gap_zero:.5f}")
    plt.figure()
    plt.grid(True)
    plt.plot(g_in, label=f'V(0) {f_name}')
    plt.plot(g_out, marker='x', linestyle='None')
    plt.axhline(y=0.5, color='r', linestyle='-', linewidth=1, label='Expected = 0.50')  # Horizontal line at y = 0.5
    plt.axhline(y=avg_norm_gap_zero, color='g', linestyle='-', linewidth=1,
                label=f'Mean = {avg_norm_gap_zero:.2f}')  # Horizontal line at average value
    # plt.text(0, avg_norm_gap_zero, f'Avg: {avg_norm_gap_zero:.2f}', color='b', va='bottom')  # Add average value label
    # plt.title(f"Normalized length of 0 gap {f_name}")
    plt.xlabel("Sequence Number")
    plt.ylabel("V(0)")
    plt.legend(loc='best')
    plt.ylim(0.25, 0.75)


def plot_MSE(norm_gaps_one, file_n=None):
    avg_norm_gap_one = sum(norm_gaps_one) / len(norm_gaps_one)
    plt.figure()
    plt.grid(True)
    plt.plot(norm_gaps_one, label=f'Data')
    plt.axhline(y=0.0, color='r', linestyle='-', linewidth=1, label='Expected = 0.0')  # Horizontal line at y = 0.5
    plt.axhline(y=avg_norm_gap_one, color='g', linestyle='-', linewidth=1,
                label=f'Avg. = {avg_norm_gap_one:.5f}')  # Horizontal line at average value
    # plt.text(0, avg_norm_gap_one, f'Avg: {avg_norm_gap_one:.2f}', color='b', va='bottom')  # Add average value label
    plt.title(f"MSE of V(0) {file_n}")
    plt.xlabel("Sequence Number")
    plt.ylabel("Mean square error")
    plt.legend()
    plt.ylim(-0.00005, 0.001)



# Use the functions ====================================================================================================
# file_names = ['../RBG_data_files/QRNG.txt',
#               '../RBG_data_files/AES.txt',
#               '../RBG_data_files/ChaCha20.txt', '../RBG_data_files/CTR.txt',
#               '../RBG_data_files/Hash.txt',
#               '../RBG_data_files/HMAC.txt', '../RBG_data_files/M_sequences.txt',
#               '../RBG_data_files/RC4.txt', '../RBG_data_files/RSA.txt',
#               '../RBG_data_files/Synthetic.txt', '../RBG_data_files/bit-flip_Model.txt',
#               '../RBG_data_files/Ideal_model.txt', '../RBG_data_files/thermal_Model.txt']

file_names = ['../RBG_Algorithms_by_ChiragPatel/M_sequences.txt']

for file_name in file_names[:]:
    # get the file names
    b_n = os.path.basename(file_name)           # Extract only the file name
    base_name = os.path.splitext(b_n)[0]        # Remove file extension

    sequences = read_sequences(file_name)       # collect All the sequences
    ang = get_norm_gaps(sequences)              # all normalised gaps
    gap_in, gap_out = get_selected_gap(ang, 0)
    # get_gap1 = get_selected_gap(ang, 1)


    plot_GDF_zeros(gap_in, gap_out, base_name)
    # plt.savefig(f"Zeros_{base_name}.png")



    # actual_values = [0.5] *  len(gap_in)         # Define the list of actual values
    # mse_values = []         # Compute the MSE values for different predicted values
    # for gap in gap_in:
    #     mse_value = mse(actual_values, gap)
    #     mse_values.append(mse_value)
    #
    # plot_MSE(mse_values, base_name)
    # plt.savefig(f"Ones_{base_name}.png")

    # Use the mse functions ============================================================================================

    # avg_zero = sum(gap_in) / len(gap_in)
    # avg_zero = "{:.2f}".format(avg_zero)
    #
    # actual_values = [0.50]  # Define the list of actual values
    # mse_values = []  # Compute the MSE values for different predicted values
    # mse_value = mse(actual_values, [float(avg_zero)])
    # mse_values.append(mse_value)
    #
    # print(f"{base_name}: {mse_values[0]:.2e}      test avg: {avg_zero}")

    # Use the functions ====================================================================================================

plt.show()