import matplotlib.pyplot as plt
import os
import random

class Runs_tests:
    def __init__(self, data):
        self.data = data

    # Helper for 5.1.2, 5.1.3, and 5.1.4
    # Builds a list of the runs of consecutive values
    # Appends -1 to the list if the value is > than the next
    # Appends +1 to the list if the value is <= than the next
    # Requires non-binary data

        self.ret = []
        for i in range(len(self.data)-1):
            if self.data[i] > self.data[i+1]:
                self.ret.append(-1)
            else:
                self.ret.append(1)



    # 5.1.2 Number of Directional Runs
    # Determines the number of runs in the sequence.
    # A run is when multiple consecutive values are all >= the prior
    # or all < the prior
    # Requires data from alt_sequence1, binary data needs conversion1 first
    # 5.1.5 Number of Runs Based on the Median
    # Determines the number of runs that are constructed with respect
    # to the median of the dataset
    # This is similar to a normal run, but instead of being compared
    # to the previous value, each value is compared to the median
    # Requires data from alt_sequence2

    def num_directional_runs(self):
        # print(alt_seq)
        num_runs = 0
        if len(self.ret) > 0:
            num_runs += 1
        for i in range(1, len(self.ret)):
            if self.ret[i] != self.ret[i-1]:
                num_runs += 1
        return num_runs


    # 5.1.3 Length of Directional Runs
    # Determines the length of the longest run
    # Requires data from alt_sequence1, binary data needs conversion1 first
    # 5.1.6 Length of Runs Based on the Median
    # Determines the length of the longest run that is constructed
    # with respect to the median
    # Requires data from alt_sequence2

    def len_directional_runs(self):
        max_run = 0
        run = 1
        for i in range(1, len(self.ret)):
            if self.ret[i] == self.ret[i-1]:
                run += 1
            else:
                if run > max_run:
                    max_run = run
                run = 1
        if run > max_run:
            max_run = run
        return max_run

    # 5.1.4 Number of Increases and Decreases
    # Determines the maximum number of increases or decreases between
    # consecutive values
    # Requires data from alt_sequence1, binary data needs conversion1 first

    def num_increases_decreases(self):
        positive = 0
        for i in range(len(self.ret)):
            if self.ret[i] == 1:
                positive += 1
        reverse_positive = len(self.ret) - positive
        if positive > reverse_positive:
            return positive
        else:
            return reverse_positive

    def calculate_all_test_statistics(self):
        num_directional_runs = self.num_directional_runs()
        len_directional_runs = self.len_directional_runs()
        num_increases_decreases = self.num_increases_decreases()

        return num_directional_runs, len_directional_runs, num_increases_decreases


# Fisher yates shuffle =================================================================================================
def fisher_yates_shuffle(sequence):
    for i in range(len(sequence) - 1, 0, -1):
        j = random.randint(0, i)
        sequence[i], sequence[j] = sequence[j], sequence[i]
    return sequence


# Permutation testing to find the statistics are iid or not ============================================================
def permutation_test(S):
    S = list(S)
    runs_tests = Runs_tests(S)
    Ti = runs_tests.calculate_all_test_statistics()
    C = [0, 0, 0]

    for _ in range(2000):
        # S = fisher_yates_shuffle(S)
        random.shuffle(S)
        runs_tests = Runs_tests(S)
        T = runs_tests.calculate_all_test_statistics()

        for i in range(3):
            if T[i] > Ti[i]:
                C[i] += 1
            elif T[i] == Ti[i]:
                C[i] += 1
    for i in range(3):
        if C[i] <= 5 or C[i] >= 9995:
            return 0.0
    return 1.0

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
def Runs_of_all_sequences(seq_):
    all_runs = []                                          # set a buffer to store the normalised gaps
    f = 0
    for sequence in seq_:
        statics = permutation_test(sequence)
        all_runs.append(statics)                           # set them with a descending order to ease the further part
        f += 1
        print('P =', f)
    return all_runs


# Function to plot the normalized gap length of 0 and 1 for all sequences ==============================================
def plot_burstiness(norm_gaps_zero):
    plt.figure()
    plt.grid(True, which='both')  # Specify grid lines for both axes
    plt.plot(norm_gaps_zero, marker='x', label=f'Data')
    plt.axhline(y=1.0, color='r', linestyle='-', linewidth=1, label='Expected = 1')  # Horizontal line at y = 1
    plt.xlabel("Sequence Number")
    plt.ylabel("IID-assumption")
    plt.legend(loc='best')
    plt.ylim(0, 2)


# Use the functions ====================================================================================================
file_names = ['../RBG_data_files/QRNG.txt',
              '../RBG_data_files/AES_DRBG.txt',
              '../RBG_data_files/ChaCha20.txt', '../RBG_data_files/CTR_DRBG.txt',
              '../RBG_data_files/hash_drbg.txt',
              '../RBG_data_files/hmac_drbg.txt', '../RBG_data_files/M_sequences.txt',
              '../RBG_data_files/RC4_algorithm.txt', '../RBG_data_files/RSA_algorithm.txt',
              '../RBG_data_files/Synthetic_RBG.txt', '../RBG_data_files/Q_bit-flip_noice_Model.txt',
              '../RBG_data_files/Ideal Q-simulator.txt', '../RBG_data_files/Q_thermal_noice_Model.txt']

for file_name in file_names[:1]:
    # get the file names
    b_n = os.path.basename(file_name)           # Extract only the file name
    base_name = os.path.splitext(b_n)[0]        # Remove file extension

    sequences = read_sequences(file_name)       # collect All the sequences
    Runs = Runs_of_all_sequences(sequences)  # all normalised gaps

    plot_burstiness(Runs)
    plt.savefig(f"IID_Num_Runs_{base_name}")

plt.show()