import random

# Define genetic algorithm parameters
POPULATION_SIZE = 10
BIT_STRING_LENGTH = 10
MAX_GENERATIONS = 100
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1


# Fitness function: Maximize number of alternating bits (e.g., 010101)
def fitness(bit_string):
    count = 0
    for i in range(1, BIT_STRING_LENGTH):
        if bit_string[i] != bit_string[i - 1]:
            count += 1
    return count


# Generate a random bit string
def generate_bit_string():
    return [random.randint(0, 1) for _ in range(BIT_STRING_LENGTH)]


# Selection (using tournament selection)
def select(population):
    parents = []
    for _ in range(POPULATION_SIZE // 2):
        # Select 2 individuals randomly
        individuals = random.sample(population, 2)
        # Choose the fitter individual
        parents.append(max(individuals, key=fitness))
    return parents


# Crossover (single-point crossover)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, BIT_STRING_LENGTH - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


# Mutation (bit flip)
def mutate(bit_string):
    for i in range(BIT_STRING_LENGTH):
        if random.random() < MUTATION_RATE:
            bit_string[i] = 1 - bit_string[i]
    return bit_string


# Main loop
def main():
    # Initialize population
    population = [generate_bit_string() for _ in range(POPULATION_SIZE)]

    # Run for max generations
    for generation in range(MAX_GENERATIONS):
        # Evaluate fitness
        fitness_scores = [fitness(bit_string) for bit_string in population]

        # Select parents
        parents = select(population)

        # Create offspring
        offspring = []
        for i in range(0, len(parents) - 1, 2):  # Ensure i < len(parents) - 1
            if random.random() < CROSSOVER_RATE:
                child1, child2 = crossover(parents[i], parents[i + 1])
                offspring.append(mutate(child1))
                offspring.append(mutate(child2))
            else:
                offspring.append(parents[i])
                offspring.append(parents[i + 1])

        # Handle case when number of parents is odd
        if len(parents) % 2 == 1:
            offspring.append(parents[-1])

        # Replace old population with offspring
        population = offspring

        # Print best individual each generation
        best_index = fitness_scores.index(max(fitness_scores))
        best_individual = population[best_index]
        print(f"Generation {generation + 1}: Best individual: {best_individual}, Fitness: {fitness(best_individual)}")

    # Print final best individual
    best_index = fitness_scores.index(max(fitness_scores))
    best_individual = population[best_index]
    print(f"Final best individual: {best_individual}, Fitness: {fitness(best_individual)}")


if __name__ == "__main__":
    main()
