# from BBS import BBS
# from Tests import Tests
#
# bits = BBS(101, 31)
# bits = bits.generateBits(100)
# # print(bits)
# print(Tests().series(bits))
# print(Tests().singleBit(bits))


from BBS_Test_file import BBS
from Tests import Tests

bits = BBS(14, 31)
bits = bits.generateBits(100)
print(bits)
print(Tests().series(bits))
print(Tests().singleBit(bits))
