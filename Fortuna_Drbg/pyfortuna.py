# -*- coding: utf-8 -*

from accumulator import Accumulator
from seedcreator import SeedCreator

if __name__ == '__main__':
    accumulator = Accumulator()
    try:
        f = open('seed_file.txt', 'rb')
    except:
        with open('/dev/random', 'rb') as random_source:  # Device file under Linux kernel, recording environmental noise, can be used as random number generator
            random_source.seek(64, 2)
            seed = random_source.read(64)
            assert len(seed) == 64
    else:
        try:
            seed = f.read(64)
            assert len(seed) == 64
        finally:
            f.close()
    accumulator.generator.reseed(seed)
    SeedCreator().seed_update(accumulator)
    n = 1	                                                # Auxiliary value
    while n != 0:
        n = input("\n(Enter 0 to exit)\nPlease enter the number of bytes of the generated random number (n>0): ")
        if n == 0:
            print("Exited!\n")
            quit()
        elif n < 0:
            print("Input error!!!\n")
            quit()
        else:
            print("\nGenerate random number:\n%r" % (accumulator.random_data(int(n))).encode('hex').decode('hex'))
