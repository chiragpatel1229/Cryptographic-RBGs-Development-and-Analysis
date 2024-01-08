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
    burstiness = (mean_time - std_dev) / (mean_time + std_dev)  # correction of Burstiness Parameter "B" for a signal

    return burstiness


# s = '00100000100111111100001110110111101010000100110111000000110001100101011111000110110011100001111001100001101001011110011100010000000011110110101100001111100010010100011011111001011111111001000011000000011111101110001100101100010101110111000010011111010111011100101001001110111111100101111010111100110001101011001001110001011000110001000111000011001000010001110100110000010001001010011000100010001100111101000100100101111110001010000101111111000000001011001111011010110101000001111101000001000001111000010000111001'
# b = B_Cal(s)
#
# print(b)
