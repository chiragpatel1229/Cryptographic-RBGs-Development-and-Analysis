import math

"""" OKAY
This is Repetition Count Test: NIST SP 800-90B
It checks the sequence has many continued ones or zeros, if the continued bits is grater than count limit it returns Fail result.
"""""
#


def rct(bitstring):             # Repetition Count Test

    # Check the type of the input bitstring
    if isinstance(bitstring, list):    # If it is a list of binary integers
        bitstring = "".join(map(str, bitstring))   # Convert it to a binary string

    # alpha = 0.001             # acceptance or tolerance level
    # H = 0.9                   # NIST min entropy accepted level as mentioned in the document
    # C = 1 + math.ceil(-math.log2(alpha) / H)
    # print(C)  # output: 12

    C = 12  # general repetition count limit, this can be calculated by using the given formula in the 4.4.1 section

    current = bitstring[0]      # Initialize the current bit and the counter
    counter = 1
    
    for bit in bitstring[1:]:   # Loop through the remaining bits

        if bit == current:      # Check the bit is equal to the current bit
            counter += 1        # Increment the counter
            
            if counter > C:     # Check if the counter is more than the limit
                return False    # Return False to indicate a failure
        else:                   # Reset the current bit and the count
            current = bit
            counter = 1
    print("The sequence has passed the Repetition Count Test!!!")
    return True                 # Return True to indicate a success


# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================

def apt(bitstring):                     # Adaptive Proportion Test

    # Check the type of the input bitstring
    if isinstance(bitstring, list):    # If it is a list of binary integers
        bitstring = "".join(map(str, bitstring))   # Convert it to a binary string

    # Define the parameters for the test
    H = 0.712                           # min-entropy estimate mentioned in foot-note on Pg.: 40 (NIST Doc.)
    W = len(bitstring)                  # window size
    alpha = 2**(-20)                    # significance level also check the section 4.4

    window = bitstring[:W]              # Consider the whole sequence as a window
    count = window.count("1")           # count the total number of 1s in the sequence
    
    p = 2**(-H)                         # mentioned on page 34 line number 1st

    # Calculate the cutoff value as given in the Table - 2
    cutoff = W * (p + math.sqrt((1 - p) * p * math.log(1 / alpha) / (2 * W)))

    if count > cutoff:                  # Check if the count exceeds the cutoff
        return False                    # Return False to indicate a failure
    
    # Loop through the remaining bits
    for bit in bitstring[W:]:

        count = count - int(window[0]) + int(bit)  # Update the count by subtracting the first bit and adding the new bit

        window = window[1:] + bit       # Update the window by removing the first bit and appending the new bit

        if count > cutoff:              # Check if the count exceeds the cutoff
            return False                # Return False to indicate a failure
    print("The sequence has passed the Adaptive Proportion Test!!!")
    # Return True to show a success
    return True


# seq = [0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0]
#
# # seq = (1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0)
#
# seq = '110101100000011110001001011010001111010010010100101001011001001110100010010100101100100111010001110010010001101110111000100010000110110110011011100110110100011101001111010000000101010001011110010010001101110111010001000111100011111001001010010110010011101000100001100000010100011110110101110100001000010101110011011010001110100100101010110000001001100110110100011110100100101010111101010001000001011100110110100011101001000001101100000100101110100001111110110011001110111001001000110111011101110011011010001110100110000101111001110100011110001001010011101100101000011000000101000111000011111101100110011101100010010100111011001011001101111011110000011011100110110100011101001010111101010001000001100010010100111011001010111100100110011101010011000100101001110110010101110011011010001110100101011110101000100000110001001010011101100101100110111101111000001101110011011010001110100110101101001111010011011100101100111100001101001101111100010111011111011000100101001110110010110000101111001110100011100000110110000010010111010000110000001010001111001011010000001010111010110010101000000001011000011111101100110011101000111111000011100001101101111001001100111010100100001101010100111001001010010110010011101000101011110101000100000111001001000110111011101010111011011110000111110010010000110000011001'
#
# a = apt(seq)
# b = rct(seq)
# print(a)
# print(b)
