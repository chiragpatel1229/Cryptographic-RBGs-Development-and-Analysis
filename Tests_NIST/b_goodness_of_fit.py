import math


def bgoft(data):

    """" OK
    This function calculates the binary chi-square goodness-of-fit test
    This method is mention in section 5.2.4 in the 800-90B publication based on the NIST Special Publication 800-90B, 
    Recommendation for the Entropy Sources Used for Random Bit Generation.
    # data is a list of binary values (0 or 1), string or list of integers
    # This function returns two values: score and degree of freedom
    
    T is a chi-square random variable with nine degrees of freedom. The test fails if T is larger than the critical value at 0.001, which is 27.887.
    """""

    # convert the binary string to list of integers if not
    if isinstance(data, str):
        data = [int(bit) for bit in data]

    sample_size = len(data)              # the total number of bits will be tested

    # Get ten non-overlapping subsets in Section 5.2.4.2
    sub_length = sample_size // 10       # Find proportion of sub-sets from the whole data set

    ones = 0                             # set the counter to zero for counting Ones
    for i in range(sample_size):
        ones += data[i]                  # sum up all the ones in the sequence

    p = ones / sample_size               # calculate the number of ones in the sequence and normalise it

    T = 0                                # Initialize T to 0 as in section 5.2.4.3

    # Compute expected 0s and 1s in each sub-sequence
    e0 = (1.0 - p) * sub_length          # use the formula given in the section 5.2.4.4
    e1 = p * sub_length

    for i in range(10):

        # Let 𝑜𝑜0 and 𝑜𝑜1 be the number of zeros and ones in 𝑆𝑆𝑑𝑑, respectively. in the section 5.2.4.5
        o1 = 0                           # Count 1s in the sub-set
        for j in range(sub_length):
            o1 += data[i * sub_length + j]

        o0 = sub_length - o1             # Count 0s in the sub-set

        # Compute T -> in the section 5.2.4.5
        T += (math.pow(o0 - e0, 2) / e0) + (math.pow(o1 - e1, 2) / e1)

    score = T                   # score is the chi-square statistic
    df = 9                      # df is the degrees of freedom 10 - 1 = 9

    return score, df


# data1 = '0011000011000011000100100001100000000001010010101010101101011001110101110111011001101111111110101111010010000100111001101000100111001110001111100001100000100111000010000001101001000100101010010100111001111100011001001011111010011101011001000111001000100100000001101001001001101111001001111100010000011100100001111001011101100001010100010111010001111110111110000001010100000111010100110011000000100000101111100010101111011011000100101011101110011100100001100100100111100010000111100101110010011001100110110010111010011100000111101110000001000011100000101010010010010110110000100111010100100010001001010100001001100100011011111111100000101000111110111000010011001111100011100110101011100100100011100101000111110101001001100001110010111111110110011111001110001111111100010111011110010111011001101111010100000101100010011100010001001111110110100110100101001111010110000101111011010001110000101111010011010011101000101100000001101100010100100011000011100110110100100000111100010000110010100001001111000100'
# chi, deg_f = bgoft(data1)
# print("The chi-square statistic using goodness of fit test........... =", chi)
# print("The degree of freedom for calculating the goodness of fit test =", deg_f)
