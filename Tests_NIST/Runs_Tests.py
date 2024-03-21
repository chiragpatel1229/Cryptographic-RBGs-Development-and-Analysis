
class NIST_SP_800_90B:
    def __init__(self, data):
        self.data = data
        self.median = sorted(data)[len(data)//2]

        print("median (centered value in the provided list) = ", self.median, '\n')

    # Helper for 5.1.2, 5.1.3, and 5.1.4
    # Builds a list of the runs of consecutive values
    # Appends -1 to the list if the value is > than the next
    # Appends +1 to the list if the value is <= than the next
    # Requires non-binary data

    def alt_sequence1(self):
        ret = []
        for i in range(len(self.data)-1):
            if self.data[i] > self.data[i+1]:
                ret.append(-1)
            else:
                ret.append(1)
        return ret


    # Helper for 5.1.5 and 5.1.6
    # Builds a list of the runs of values compared to the median
    # Appends +1 to the list if the value is >= the median
    # Appends -1 to the list if the value is < than the median

    def alt_sequence2(self):
        ret = []
        for i in range(len(self.data)):
            if self.data[i] < self.median:
                ret.append(-1)
            else:
                ret.append(1)
        return ret


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

    def num_directional_runs(self, alt_seq):
        print(alt_seq)
        num_runs = 0
        if len(alt_seq) > 0:
            num_runs += 1
        for i in range(1, len(alt_seq)):
            if alt_seq[i] != alt_seq[i-1]:
                num_runs += 1
        return num_runs


    # 5.1.3 Length of Directional Runs
    # Determines the length of the longest run
    # Requires data from alt_sequence1, binary data needs conversion1 first
    # 5.1.6 Length of Runs Based on the Median
    # Determines the length of the longest run that is constructed
    # with respect to the median
    # Requires data from alt_sequence2

    def len_directional_runs(self, alt_seq):
        max_run = 0
        run = 1
        for i in range(1, len(alt_seq)):
            if alt_seq[i] == alt_seq[i-1]:
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

    def num_increases_decreases(self, alt_seq):
        positive = 0
        for i in range(len(alt_seq)):
            if alt_seq[i] == 1:
                positive += 1
        reverse_positive = len(alt_seq) - positive
        if positive > reverse_positive:
            return positive
        else:
            return reverse_positive

    def print_outputs(self):
        alt_seq1 = self.alt_sequence1()
        alt_seq2 = self.alt_sequence2()
        print("Number of Directional Runs: ", self.num_directional_runs(alt_seq1))
        print("Length of Directional Runs: ", self.len_directional_runs(alt_seq1))
        print("Number of Increases and Decreases: ", self.num_increases_decreases(alt_seq1))
        print("Number of Runs Based on the Median: ", self.num_directional_runs(alt_seq2))
        print("Length of Runs Based on the Median: ", self.len_directional_runs(alt_seq2))


s = '100010111101000'

rnd_seq = [int(bit) for bit in s]


rnd_zeros = rnd_seq.count(0)
rnd_ones = rnd_seq.count(1)
print(f"Random Sequence Balance: 0s= {rnd_zeros}, 1s= {rnd_ones}\n\n")

print('length of the sequence:', len(s), '\n')
a  = [5, 15, 12, 1, 13, 9, 4]
nist = NIST_SP_800_90B(s)
nist.print_outputs()