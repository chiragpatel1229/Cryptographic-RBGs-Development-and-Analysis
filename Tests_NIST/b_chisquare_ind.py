import math

"""" OKAY
This function calculates the binary chi-square independence test from NIST SP 800-90B

"""""


def bcit(data):

    if isinstance(data, str):           # convert the bit string to the list of integers if not
        data = [int(bit) for bit in data]

    sample_size = len(data)             # calculate the total number of bits in the sequence

    # This is equivalent to estimating p0 and p1 in Section 5.2.3.1

    p1 = 0.0                            # Compute proportion of 1s

    for i in range(sample_size):        # loop through the whole sequence
        p1 += data[i]

    p1 /= sample_size                   # normalise the value of 1s
    p0 = 1.0 - p1                       # Compute proportion of normalised 0s

    # Compute m and this is the length of the bit strings (tuples) to be tested
    # The value of m is chosen to satisfy the condition in Section 5.2.3.2
    min_p = min(p0, p1)
    m = 11
    threshold = 5
    while m > 1:
        if math.pow(min_p, m) * (sample_size / m) >= threshold:
            break
        else:
            m -= 1

    '''
    The "degrees of freedom (df)" for this test are the number of possible tuples minus two. If m is 3, math.pow(2, m) - 2 = 6
    If m is 3, the calculating tuples are 000, 001, 010, 011, 100, 101, 110, and 111, and the degrees of freedom are 6.
    '''

    tuple_count = 1 << m                # if m is 3, the binary representation of 1 is 0b1, and when shifting it left by 3
                                        # positions results in 0b1000, which is 8 in decimal.

    if m < 2:                           # The test is applied if m ≥ 2.

        score = 0.0                     # If m is less than 2, the test is not performed
        df = 0                          # The function returns 0 for both the test statistic and the degrees of freedom
        return score, df

    T = 0.0                             # Initialize the test statistic T

    # Count occurrence of m-bit tuples by converting to decimal and using as index in a list
    # This is equivalent to calculating the frequencies V_(j) for j = 0, ..., 2^m - 1
    occ = [0] * tuple_count             # the occ is initialised with number of tuple_count zeros -> [0000]
    block_count = sample_size // m      # calculate the total number of complete m-bit blocks from the sequence

    for i in range(block_count):
        symbol = 0
        for j in range(m):
            symbol = (symbol << 1) | data[i*m + j]  # This bitwise operations builds the decimal representation of the m-bit tuple.

        occ[symbol] += 1        # it is used as index to the occ list, and the corresponding element is incremented by 1
                                # this is how many times each unique m-bit tuple occurs in the input sequence can be tracked

    for i in range(len(occ)):   # this loop method is mentioned in the section 5.2.3.3

        w = bin(i).count("1")

        # Compute the expected frequency for each tuple
        # This is equivalent to computing E_(j) = p1^W_(j) * p0^(m - W_(j)) * floor(n/m)
        e = math.pow(p1, w) * math.pow(p0, m - w) * block_count

        # Update the test statistic T by adding the squared difference of observed and expected frequencies divided by expected frequency
        T += math.pow(occ[i] - e, 2) / e        # This is the formula for the chi-square test statistic in Section 5.2.3

    score = T                                   # Assign the test statistic T to the variable score

    # This is 2^m - 2 as stated in Section 5.2.3
    df = math.pow(2, m) - 2                     # Calculate the degrees of freedom for the test

    return score, df


# data1 = '00111111010010110101011110000001001101001100010111010010010110110101101010001001000101111100011100100001000001000000101111111000001110101010110000010011110010010101011100000110010111110000001000101000000000011101110010011010010001001111000111011110111010110111111101101010000010001110111101101110001101111110000001010101011110110010000001111111111010100010010011110111011100000011101011010100101101001111110101101011111110010001100111101000100001001010100111001001000010010000001010010001011011000001000011011110'
# chi, deg_f = bcit(data1)
# print("The Chi-square Independence test result........ =", chi)
# print("The degree of freedom for the independence test =", deg_f)
