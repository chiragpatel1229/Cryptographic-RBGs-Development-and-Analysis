import numpy as np
import scipy.stats as stats
from scipy.stats import bernoulli
from Tests_NIST import burstiness_para, memory_coeff

p = 0.5     # probability of success
n = 1000     # number of trials
sequence_1 = list(bernoulli.rvs(p, size=n))     # generate random variates
sequence_2 = list(np.random.binomial(1, p, size=n))   # generate random samples
# using the 'list' function convert an 'array' format to the 'list of integers'

print("1 = ", sequence_1)
print("2 = ", sequence_2)

rnd_zeros = sequence_1.count(0)                # counting zeros in the sequence
rnd_ones = sequence_1.count(1)                 # counting ones in the sequence

rnd_zeros_2 = sequence_2.count(0)              # counting zeros in the sequence
rnd_ones_2 = sequence_2.count(1)               # counting ones in the sequence

print(f"1st Sequence Balance - 0s= {rnd_zeros}, 1s= {rnd_ones}, diff= {rnd_zeros - rnd_ones}")
print(f"2nd Sequence Balance - 0s= {rnd_zeros_2}, 1s= {rnd_ones_2}, diff= {rnd_zeros_2 - rnd_ones_2} \n\n")


# ======================================== Burstiness and Memory Coefficient ===========================================
# burst_1 = burstiness_para.B_Cal(sequence_1)
# burst_2 = burstiness_para.B_Cal(sequence_2)
# print("Burstiness of the signal 1 = ", burst_1)
# print("Burstiness of the signal 2 = ", burst_2, "\n\n")
#
# memory_1 = memory_coeff.memory_co(sequence_1)
# memory_2 = memory_coeff.memory_co(sequence_2)
# print("Memory Coefficient of the signal 1 = ", memory_1)
# print("Memory Coefficient of the signal 2 = ", memory_2, "\n\n")

# ================================================== Chi-Square Test =================================================
expected_value = 0.5 * n              # expected values of zeros and ones


def test(zeros, ones, expected):
    # using the equation of Chi-Square test
    chi_square = (zeros - expected) ** 2 / expected + (ones - expected) ** 2 / expected

    p_val_cdf = stats.chi2.cdf(chi_square, df=1)  # get the probability value using cumulative distribution function
    p_val_pdf = stats.chi2.pdf(chi_square, df=1)  # df = 1 (degree of freedom) bcz we have only 0s and 1s

    return chi_square, p_val_cdf, p_val_pdf


# Calculate Chi-square test results and p-values for gap structures
rnd_chi, rnd_p_value_cdf, rnd_p_value_pdf = test(rnd_zeros, rnd_ones, expected_value)
o_rnd_chi, o_rnd_p_value_cdf, o_rnd_p_value_pdf = test(rnd_zeros_2, rnd_ones_2, expected_value)


# Print Chi-square test results and p-values

print("Chi-square test Result of Sequence - 1 :", rnd_chi)
print("P-value (CDF)                          :", rnd_p_value_cdf)
print("P-value (PDF)                          :", rnd_p_value_pdf, "\n")

print("Chi-square test Result of Sequence - 2 :", o_rnd_chi)
print("P-value (CDF)                          :", o_rnd_p_value_cdf)
print("P-value (PDF)                          :", o_rnd_p_value_pdf, "\n")
