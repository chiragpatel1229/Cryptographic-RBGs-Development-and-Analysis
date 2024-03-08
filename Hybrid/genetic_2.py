# Constants
POPULATION_SIZE = 100
BIT_STRING_LENGTH = 256
MAX_GENERATIONS = 3
CROSSOVER_RATE = 0.7


# Generate initial bit string
def generate_bit_string(generation):
    return [str((i + generation) % 2) for i in range(BIT_STRING_LENGTH)]


# Fitness function
def fitness(bit_string):
    return sum(int(bit) for bit in bit_string)


# Selection function
def select(population):
    # For simplicity, let's use tournament selection
    return sorted(population, key=fitness, reverse=True)[:len(population) // 2]


# Crossover function
def crossover(parent1, parent2):
    # For simplicity, let's use one-point crossover
    crossover_point = len(parent1) // 2
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


# Mutation function
def mutate(bit_string):
    # For simplicity, let's flip a random bit
    bit_to_flip = (generation + fitness(bit_string)) % BIT_STRING_LENGTH
    bit_string[bit_to_flip] = '1' if bit_string[bit_to_flip] == '0' else '0'
    return bit_string


# Main loop
def main():
    # Initialize population
    global generation, fitness_scores
    population = [generate_bit_string(generation) for generation in range(POPULATION_SIZE)]

    # Run for max generations
    for generation in range(MAX_GENERATIONS):
        # Select parents
        parents = select(population)

        # Create offspring
        offspring = []
        for i in range(0, len(parents), 2):  # Iterate over all parents
            if i < len(parents) - 1:  # If there is a pair of parents
                if (i / len(parents)) < CROSSOVER_RATE:
                    child1, child2 = crossover(parents[i], parents[i + 1])
                    offspring.append(mutate(child1))
                    offspring.append(mutate(child2))
                else:
                    offspring.append(parents[i])
                    offspring.append(parents[i + 1])
            else:  # If there is only one parent left
                offspring.append(parents[i])

        # Handle case when number of parents is odd
        if len(parents) % 2 == 1:
            offspring.append(parents[-1])

        # Replace old population with offspring
        population = offspring

        # Evaluate fitness
        fitness_scores = [fitness(bit_string) for bit_string in population]

        # Print best individual each generation
        best_index = fitness_scores.index(max(fitness_scores))
        best_individual = population[best_index]
        print(
            f"Generation {generation + 1}: Best individual: {''.join(best_individual)}, Fitness: {fitness(best_individual)}")

    # Print final best individual
    best_index = fitness_scores.index(max(fitness_scores))
    best_individual = population[best_index]
    print(f"Final best individual: {''.join(best_individual)}, Fitness: {fitness(best_individual)}")


if __name__ == "__main__":
    main()
