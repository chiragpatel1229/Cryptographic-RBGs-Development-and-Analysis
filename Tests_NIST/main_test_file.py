import adaptive__repetition_count
import b_chisquare_ind
import b_goodness_of_fit
import burstiness_para
import chi_square
import Markov_Test
import memory_coeff

""" if the input sequence length is not (256 or 512) the binary_chisquare_independence_test results will differ, in that case the 
 upper and lower values of 'score_i' has to be changed manually """
#


def test_sequences(file_path):

    # Read and get a list of binary sequences from the selected file. ==================================================

    sequences = []
    with open(file_path, 'r') as file:
        for each_seq in file:
            sequences.append(each_seq.strip())

    # count the total numbers of sequences =============================================================================

    total_sequences = len(sequences)

    # Test each sequence using selected test algorithms ===============================================================

    passed_sequences = []                                       # store the sequence that has passed the test
    for index, sequence in enumerate(sequences, start=1):

        rct = adaptive__repetition_count.rct(sequence)
        apt = adaptive__repetition_count.apt(sequence)
        score_i, df_i = b_chisquare_ind.bcit(sequence)
        score_g, df_g = b_goodness_of_fit.bgoft(sequence)
        B_Cal = burstiness_para.B_Cal(sequence)
        chisquare = chi_square.chisquare(sequence)
        min_entropy = Markov_Test.markov_test(sequence)
        m_co = memory_coeff.memory_co(sequence)

        # Adjust limits based on the Chi-square independence test results ==============================================
        if df_i == 14:
            low, up = 0, 36.123
        elif df_i == 6:
            low, up = 0, 22.458
        elif df_i == 9:
            low, up = 0, 16.919
        else:
            low, up = 0, 1  # Define default limits

        # Check if the results are within the decided limits ===========================================================
        if rct is True and \
                apt is True and \
                low <= score_i <= up and \
                0 <= score_g <= 27.887 and \
                0 <= B_Cal <= 0.5 and \
                0 <= chisquare <= 3.841 and \
                0.712 <= min_entropy <= 1.000 and \
                -0.2 <= m_co <= 0.2:
            passed_sequences.append(index)
        else:
            # print('\n\n')

            # print out which test is being Failed for which sequence ==================================================
            # if not rct:
            #     print(f"Sequence {index} failed the Repetition Test.")
            # if not apt:
            #     print(f"Sequence {index} failed the Adaptive Test.")
            if not (low <= score_i <= up):
                print(f"Sequence {index} failed the Independence Test")
            if not (0 <= score_g <= 16.919):
                print(f"Sequence {index} failed the Goodness of Fit Test.")
            # if not (0 <= B_Cal <= 0.2):
            #     print(f"Sequence {index} failed the Burstiness Parameter Test.")
            # if not (0 <= chisquare <= 3.841):
            #     print(f"Sequence {index} failed the Chi-square Test.")
            if not (0.712 <= min_entropy <= 1.000):
                print(f"Sequence {index} failed the Markov = min_entropy Test.")
            # if not (-0.2 <= m_co <= 0.2):
            #     print(f"Sequence {index} failed the Memory Coefficient Test.")

    # print if all the tests are passed ================================================================================
    if len(passed_sequences) == total_sequences:

        print("\n1. Repetition Count Test: Passed \n2. Adaptive Proportion Test: Passed \n3. Chi-square Independence Test: Passed \n"
              "4. Chi-square Goodness of Fit Test: Passed \n5. Chi-square Test: Passed \n6. Burstiness Test: Passed \n7. Markov Test: Passed \n8. Memory Coefficient Test: Passed")
        print("\nAll the Provided Sequences has Successfully Passed all the Tests.")

    # print the relative data for the failed sequences =================================================================
    else:
        print(f"\nTotal sequences passed the test: {len(passed_sequences)}")
        print(f"\nSequences that failed the test: {total_sequences - len(passed_sequences)}")
        print(f"\nFailed sequences: {set(range(1, total_sequences + 1)) - set(passed_sequences)}")

    return passed_sequences


# provide the file paths
file1_path = '../Chacha/ChaCha20_Stream_Cipher_Sequences.txt'

# Test sequences and get the list of passed sequences
test_sequences(file1_path)
