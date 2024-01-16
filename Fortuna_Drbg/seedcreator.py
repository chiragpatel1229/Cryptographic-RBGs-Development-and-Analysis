import time
import random


class SeedCreator:
    def __init__(self):
        self.seed_interval = None
        self.accumulator = None
        self.last_seed = time.time()
        self.source = 0
        self.index = 0

    def seed_update(self, accumulator):
        self.accumulator = accumulator
        self.seed_interval = 600  # Set the seed update time to 600s
        with open("seed_file.txt", 'wb') as f:
            f.write(accumulator.random_data(64))

        if time.time() - self.last_seed >= self.seed_interval:
            with open("seed_file.txt", 'rb+') as f:
                s = f.read()
                assert len(s) == 64
                accumulator.generator.reseed(s)
                f.seek(0)  # Move the file pointer to the beginning
                f.truncate()  # Empty the file
                f.write(accumulator.randomdata(64))
            self.seed_interval = time.time()

        # with open('/dev/random', 'rb') as subject_source:
        #     subject_source.seek(32, 2)
        #     subject = subject_source.read(random.randint(1, 32))
        #     self.accumulator.add_random_event(self.source, self.index, subject)
        #     self.source = (self.source + 1) % 256
        #     self.index = (self.index + 1) % 32
