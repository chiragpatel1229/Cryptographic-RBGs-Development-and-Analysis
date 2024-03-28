import statistics


# ==================================== Interevent times for 0s and 1s =================================================

def inter_t(seq, eve):                  # Calculate the events from the sequence as 0s and 1s
    times = []                          # Create an empty list for storing the selected events
    counter = 0                         # set the counter
    for i in range(len(seq)):
        if seq[i] == eve:               # if the current event = selected event
            if counter != 0:            # the counter is still counting the intervals
                times.append(counter)   # append the counter for every continuous event
            counter = 0                 # reset the counter
        else:
            counter += 1                # go to the next index in the counter after storing the first interval
    return times


# ==================================== Memory Coefficient Calculation =================================================

def memory_co(sequence):                        # A function to calculate the memory coefficient M

    if isinstance(sequence, str):
        sequence = [int(bit) for bit in sequence]

    times_0 = inter_t(sequence, 0)              # Number of Time intervals for 0s
    times_1 = inter_t(sequence, 1)              # Number of Time intervals for 1s

    m1 = statistics.mean(times_0)               # Mean of 0s interevents
    m2 = statistics.mean(times_1)               # Mean of 1s interevents
    s1 = statistics.stdev(times_0)              # S.D. of 0s interevents
    s2 = statistics.stdev(times_1)              # S.D. of 0s interevents

    sum_0s = 0                                  # set up an empty variable to store the total of 0s interevents
    for i in range(len(times_0) - 1):           # calculation for 0s interevents
        product = (times_0[i] - m1) * (times_0[i + 1] - m1)  # Mean interevents and times calculation using equation
        sum_0s += product                       # Store the answers

    sum_1s = 0                                  # set up an empty variable to store the total of 0s interevents
    for i in range(len(times_1) - 1):           # calculation for 1s interevents
        product = (times_1[i] - m2) * (times_1[i + 1] - m2)  # Mean interevents and times calculation using equation
        sum_1s += product                       # Store the answers

    tau = len(set(times_0 + times_1))           # total number of interevents times of each event occurrence combined 0s and 1s
    sum_all = sum_0s + sum_1s                   # the total of 0s + 1s interevents

    m = sum_all / ((len(sequence) * tau - 1) * s1 * s2)     # Final Calculation for memory coefficient

    return m


# s = '00100000100111111100001110110111101010000100110111000000110001100101011111000110110011100001111001100001101001011110011100010000000011110110101100001111100010010100011011111001011111111001000011000000011111101110001100101100010101110111000010011111010111011100101001001110111111100101111010111100110001101011001001110001011000110001000111000011001000010001110100110000010001001010011000100010001100111101000100100101111110001010000101111111000000001011001111011010110101000001111101000001000001111000010000111001'
# b = memory_co(s)
#
# print(b)






