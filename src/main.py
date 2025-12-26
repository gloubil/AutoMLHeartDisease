from Population import Population
from multiprocessing import freeze_support

# [3, 2, 0, 1, 1, 2, 14, 21, 23, 2, 5, 221] -> 0.7511 no sampling
# [1, 2, 4, 1, 1, 1, 18, 18, 21, 21, 26, 209] -> 0.7706 no sampling

if __name__ == "__main__":
    freeze_support()


    iterations = 20

    pop = Population.generateRandom()

    print(pop)

    for i in range(iterations):
        pop = pop.nextGeneration()
        print()
        print()
        print(pop)