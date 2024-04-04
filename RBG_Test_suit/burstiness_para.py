import matplotlib.pyplot as plt
import os


def inter_t(seq, eve):                  # Indices and interevent times difference for selected event

    # checks if the input sequence is list of integers
    if isinstance(seq, list) and all(isinstance(x, int) for x in seq):
        seq = ''.join(map(str, seq))    # Convert the list of integers to a string

    # Map an indices for the selected event (0s or 1s)
    event_time = []                     # Create an empty list to store the event's indices
    for i, x in enumerate(seq):         # loop through every index of the list
        if x == eve:                    # Check if the current value is selected value
            event_time.append(i)        # If yes, add the index 'i' to the 'event_time' list

    # Calculate the interevent times difference for each event occurrence
    time_diff = []                                  # Create an empty list
    for i in range(len(event_time) - 1):            # Iterate in the range of total number of events
        time = event_time[i + 1] - event_time[i]    # Find actual time between two consecutive events
        time_diff.append(time)                      # Add, 'Time' needed for each event occurrence

    return time_diff


def B_Cal(seq):                         # Burstiness parameter calculation for the binary sequence

    int_1s = inter_t(seq, "1")          # interevent time differences for 1s
    int_0s = inter_t(seq, "0")          # interevent time differences for 0s

    time_diff = int_1s + int_0s         # Total of both event's occurrence time differences from indices

    mean_time = sum(time_diff) / (len(time_diff))                 # Mean Interevent time calculation Based on actual equation

    # Calculation of interevent times and Mean with square
    sum_time_mean = 0                   # initialise the counter
    for time in time_diff:
        diff = (time - mean_time) ** 2  # Calculate the difference of "Interevent Time and Mean" with squared
        sum_time_mean += diff           # Addup it to the sum of 'Interevent Time and Mean' difference

    std_dev = (sum_time_mean / len(time_diff)) ** 0.5           # Standard Deviation calculation with square root

    # burstiness = (std_dev - mean_time) / (std_dev + mean_time)  # calculation of Burstiness Parameter "B" for a signal
    burstiness = -((mean_time - std_dev) / (mean_time + std_dev))  # correction of Burstiness Parameter "B" for a signal

    return burstiness


# Function to read sequences from a .txt file ==========================================================================
def read_sequences(file_name_):
    with open(file_name_, 'r') as file:                      # open the file in a read mode
        _sequences = []                                      # set a buffer to store the sequences
        for line in file:
            stripped_line = line.strip()                     # extract each sequence as a separate line
            mapped_line = list(map(int, stripped_line))      # convert each line to the list of integers
            _sequences.append(mapped_line)                   # append each sequence as a list to the buffer
    return _sequences                                        # return the list of sequences


# Function to calculate Burstiness of each sequence =======================================================
def burstiness_of_all_sequences(seq_):
    all_bursty_data = []                                          # set a buffer to store the normalised gaps
    for sequence in seq_:
        b_ = B_Cal(sequence)                               # find the gaps from each sequence
        all_bursty_data.append(b_)   # set them with a descending order to ease the further part
    return all_bursty_data


# Function to plot the normalized gap length of 0 and 1 for all sequences ==============================================
def plot_burstiness(norm_gaps_zero, f_name=None):
    avg_norm_gap_zero = sum(norm_gaps_zero) / len(norm_gaps_zero)
    plt.figure()
    plt.grid(True)
    plt.plot(norm_gaps_zero, label=f'Data')
    plt.axhline(y=0.0, color='r', linestyle='-', linewidth=1, label='Expected = 0.0')  # Horizontal line at y = 0.5
    plt.axhline(y=avg_norm_gap_zero, color='g', linestyle='-', linewidth=1, label=f'Avg. = {avg_norm_gap_zero:.5f}')  # Horizontal line at average value
    # plt.text(0, avg_norm_gap_zero, f'Avg: {avg_norm_gap_zero:.2f}', color='b', va='bottom')  # Add average value label
    # plt.title(f"Burstiness parameter 'B' for {f_name}")
    plt.xlabel("Sequence Number")
    plt.ylabel("B-parameter")
    plt.legend(loc='best')
    plt.ylim(-1, 1)



# s = '00100000100111111100001110110111101010000100110111000000110001100101011111000110110011100001111001100001101001011110011100010000000011110110101100001111100010010100011011111001011111111001000011000000011111101110001100101100010101110111000010011111010111011100101001001110111111100101111010111100110001101011001001110001011000110001000111000011001000010001110100110000010001001010011000100010001100111101000100100101111110001010000101111111000000001011001111011010110101000001111101000001000001111000010000111001'
# b = B_Cal(s)
#
# print(b)

# file_name1 = '../RBG_data_files/AES_DRBG.txt'
#
# s1 = read_sequences(file_name1)
# burst = burstiness_of_all_sequences(s1)  # all normalised gaps
# plot_burstiness(burst)
# print(burst)

# Use the functions ====================================================================================================
file_names = ['../RBG_data_files/QRNG.txt',
              '../RBG_data_files/AES_DRBG.txt',
              '../RBG_data_files/ChaCha20.txt', '../RBG_data_files/CTR_DRBG.txt',
              '../RBG_data_files/hash_drbg.txt',
              '../RBG_data_files/hmac_drbg.txt', '../RBG_data_files/M_sequences.txt',
              '../RBG_data_files/RC4_algorithm.txt', '../RBG_data_files/RSA_algorithm.txt',
              '../RBG_data_files/Synthetic_RBG.txt', '../RBG_data_files/Q_bit-flip_noice_Model.txt',
              '../RBG_data_files/Ideal Q-simulator.txt', '../RBG_data_files/Q_thermal_noice_Model.txt']

for file_name in file_names[:]:
    # get the file names
    b_n = os.path.basename(file_name)           # Extract only the file name
    base_name = os.path.splitext(b_n)[0]        # Remove file extension

    sequences = read_sequences(file_name)       # collect All the sequences
    burst = burstiness_of_all_sequences(sequences)     # all normalised gaps

    plot_burstiness(burst, base_name)
    plt.savefig(f"B_{base_name}")

plt.show()
