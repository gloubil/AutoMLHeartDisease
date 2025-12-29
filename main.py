from Population import Population
from NeuralNetModel import NeuralNetModel
from Individu import Individu
from multiprocessing import freeze_support

# [0, 0, 0, 0, 1, 2, 14, 21, 23, 2, 5, 221] -> 0.7511 no sampling
# [0, 0, 0, 0, 1, 1, 18, 18, 21, 21, 26, 209] -> 0.7706 no sampling
# [4, 1, 4, 1, 1, 1, 25, 5, 13, 27, 3, 448] -> 0.9545 0.5
# [1, 2, 4, 1, 1, 5, 20, 19, 27, 27, 9, 142] -> 0.9250 0.8
# [1, 3, 3, 1, 1, 2, 17, 9, 20, 24, 8, 448] -> 0.9393 0.8 goood

if __name__ == "__main__":
    freeze_support()

    try:


        iterations = 10

        pop = Population.generateRandom()

        pop.resetFitness()

        print(pop)

        for i in range(iterations):
            if i == 2:
                NeuralNetModel.tolerance = 0.6
            if i == 3:
                NeuralNetModel.tolerance = 0.7
                Population.mutate_rate = 0.6
                pop.resetFitness()
            if i == 4:
                NeuralNetModel.tolerance = 0.8
                Population.mutate_rate = 0.7
                Population.k = 10
                pop.resetFitness()
            if i == 5:
                Population.mutate_rate = 0.9
                Population.k = 5
            pop = pop.nextGeneration()
            print()
            print()
            print(pop)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")


    for g in Individu.error_genoms:
        print(g)