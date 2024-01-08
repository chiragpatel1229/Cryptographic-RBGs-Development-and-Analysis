import scipy.stats as stats


def chisquare(sequence):

    if isinstance(sequence, str):
        sequence = [int(bit) for bit in sequence]

    rnd_zeros = sequence.count(0)        # counting zeros in the sequence
    rnd_ones = sequence.count(1)         # counting ones in the sequence

    # print(f"Random Sequence Balance - 0s= {rnd_zeros}, 1s= {rnd_ones}")
    seq_len = len(sequence)
    expected_value = 0.5 * seq_len      # expected values of zeros and ones

    def test(zeros, ones, expected):
        # using the equation of Chi-Square test
        chi_square = (zeros - expected) ** 2 / expected + (ones - expected) ** 2 / expected

        p_val_cdf = stats.chi2.cdf(chi_square, df=1)    # get the probability value using cumulative distribution function
        p_val_pdf = stats.chi2.pdf(chi_square, df=1)    # df = 1 bcz we have only 0s and 1s Probability density function ≤ 0.05.

        return chi_square, p_val_cdf, p_val_pdf

    # Calculate Chi-square test results and p-values for gap structures
    rnd_chi, rnd_p_value_cdf, rnd_p_value_pdf = test(rnd_zeros, rnd_ones, expected_value)

    # Print Chi-square test results and p-values
    # print("Chi-square test Result of a Random Sequence :", rnd_chi)
    # print("P-value (CDF) of a Random Sequence          :", rnd_p_value_cdf)
    # print("P-value (pDF) of a Random Sequence          :", rnd_p_value_pdf, "\n")

    return rnd_chi
