from math import log2, sqrt


def most_common_value(sequence, Output=0):

    # Constant Z is selected from this reference point
    # https://www.statology.org/how-to-find-z-alpha-2-za-2/
    # Actually NIST recommended using 2.567 with the confidence level of 1 - 0.005 = p 41
    Z_value = 1.96  # for a 95% confidence interval

    binary_list = [int(bit) for bit in sequence]    # convert the sequence to the list of integers
    num_zeros = binary_list.count(0)                # count the number of zeros and ones
    num_ones = binary_list.count(1)
    mode = max(num_ones, num_zeros)                 # find the maximum occurred bits in the sequence

    # Calculate p-hat and p_u
    p_hat = mode / len(sequence)                   # from Page 41 in NIST 800-90B
    p_u = min(1.0, p_hat + Z_value * sqrt((p_hat * (1.0 - p_hat)) / (len(sequence) - 1)))

    # Calculate min-entropy
    min_entropy = -log2(p_u)

    # Verbose output
    if Output == 2:
        print(f"MCV Estimate: mode = {mode}, p-hat = {p_hat}, p_u = {p_u}, min_entropy = {min_entropy}")
    elif Output == 3:
        print(f"Most Common Value Estimate: Mode count = {mode}")
        print(f"Most Common Value Estimate: p-hat = {p_hat}")
        print(f"Most Common Value Estimate: p_u = {p_u}")
        print(f"Most Common Value Estimate: min entropy = {min_entropy}")

    return min_entropy


seq = '110101100000011110001001011010001111010010010100101001011001001110100010010100101100100111010001110010010001101110111000100010000110110110011011100110110100011101001111010000000101010001011110010010001101110111010001000111100011111001001010010110010011101000100001100000010100011110110101110100001000010101110011011010001110100100101010110000001001100110110100011110100100101010111101010001000001011100110110100011101001000001101100000100101110100001111110110011001110111001001000110111011101110011011010001110100110000101111001110100011110001001010011101100101000011000000101000111000011111101100110011101100010010100111011001011001101111011110000011011100110110100011101001010111101010001000001100010010100111011001010111100100110011101010011000100101001110110010101110011011010001110100101011110101000100000110001001010011101100101100110111101111000001101110011011010001110100110101101001111010011011100101100111100001101001101111100010111011111011000100101001110110010110000101111001110100011100000110110000010010111010000110000001010001111001011010000001010111010110010101000000001011000011111101100110011101000111111000011100001101101111001001100111010100100001101010100111001001010010110010011101000101011110101000100000111001001000110111011101010111011011110000111110010010000110000011001'
s = [0, 1, 1, 2, 0, 1, 2, 2, 0, 1, 0, 1, 1, 0, 2, 2, 1, 0, 2, 1]
print(len(s))
most_common_value(s, 2)
