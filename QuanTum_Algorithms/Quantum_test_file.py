import string
import random

def rnd_msg(length):
    # https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/

    # chars = string.ascii_letters + string.digits + string.punctuation       # Random message Char. selection Opts.
    chars = string.ascii_letters + string.digits                              # Random message Char. selection Opts.
    rd_msg = "".join(random.choice(chars) for _ in range(length)).encode()    # Generating random strings
    # .encode() is for converting the 'string' message into the 'bytes'
    return rd_msg

print(rnd_msg(250))
