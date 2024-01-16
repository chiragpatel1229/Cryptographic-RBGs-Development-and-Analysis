# Import the classes
from accumulator import Accumulator
from seedcreator import SeedCreator
import os
from generator import Generator

# Create an instance of the Accumulator class and initialize it with a seed value
accumulator = Accumulator()
seed = os.urandom(2)
print("Generated random seed:", seed)


accumulator.generator.reseed(seed)

# Create an instance of the SeedCreator class and call its seed_update method
seed_creator = SeedCreator()
seed_creator.seed_update(accumulator)

# Call the random_data method of the Accumulator instance with the number of bytes you want to generate
pseudo_random_data = accumulator.random_data(16)
print(pseudo_random_data)
