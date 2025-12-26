from Individu import Individu
from random import randint, random
from multiprocessing import Pool

class Population:

    maximize = True
    len_pop = 20
    k = 5
    mutate_rate = 0.5
    process_pool_size = 5

    def __init__(self, individus, generation = 0):
        self.individus = individus
        self.generation = generation

    def selectKBest(self):
        sorted_individus = sorted(self.individus, key=lambda x: x.evaluate(), reverse=Population.maximize)
        return sorted_individus[:Population.k]
    
    def selectTheBest(self):
        sorted_individus = sorted(self.individus, key=lambda x: x.evaluate(), reverse=Population.maximize)
        return sorted_individus[:1][0]
    
    @staticmethod
    def cross(ind1 : Individu, ind2 : Individu):
        l1 = ind1.genom
        l2 = ind2.genom

        cut1 = randint(0, Individu.len_genom-1)
        cut2 = randint(cut1, Individu.len_genom-1)

        genom_child1 = l1[:cut1] + l2[cut1:cut2] + l1[cut2:]
        genom_child2 = l2[:cut1] + l1[cut1:cut2] + l2[cut2:]

        return Individu(genom_child1), Individu(genom_child2)

    def nextGeneration(self):
        Population.evaluate_population(self.individus)

        kBests = self.selectKBest()
        fifo = []
        len_fifo = 0
        # Prepare Childs
        while Population.k + len_fifo < Population.len_pop:
            a1 = randint(0, Population.k-1)
            a2 = randint(0, Population.k-1)
            child1, child2 = Population.cross(kBests[a1], kBests[a2])
            fifo.append(child1)
            fifo.append(child2)
            len_fifo += 2

        # Mutate childs
        for i in range(len_fifo):
            if random() < Population.mutate_rate:
                fifo[i].mutate()

        # Adding childs
        i = 0
        newIndividus = kBests
        while i < Population.len_pop - Population.k:
            newIndividus.append(fifo.pop(0))
            i += 1

        return Population(newIndividus, self.generation + 1)

    @staticmethod
    def generateRandom():
        individus = [Individu.generateRandom() for i in range(Population.len_pop)]
        return Population(individus)

    @staticmethod
    def evaluate_population(individus, len_pop = None):
        if len_pop == None:
            len_pop = len(individus)
        with Pool(Population.process_pool_size) as p:
            scores = p.map(Individu.static_evaluate, individus)
        for i in range(len_pop):
            individus[i].fitness = scores[i]

    def __str__(self):
        result = f"------Generation {self.generation}------"
        endLength = len(result)

        best = self.selectTheBest()
        result += f"\nMeilleur Individu : {best.genom}"
        result += f"\nFitness : {best.evaluate()}\n"


        for i in range(endLength):
            result += "-"

        return result + "\n"


if __name__ == "__main__":
    # ind1 = Individu.generateRandom()
    # ind2 = Individu.generateRandom()

    # child1, child2 = Population.cross(ind1, ind2)

    # for i in range(1000):
    #     child1, child2 = Population.cross(child1, child2)
    #     assert len(child1.genom) == Individu.len_genom and len(child2.genom) == Individu.len_genom

    # print("Cross Test OK !")

    # pop = Population.generateRandom()

    # best1 = pop.selectTheBest()

    # print("Pop Init OK !")

    # pop.selectKBest()

    # print("SelectKbest OK !")

    # pop = pop.nextGeneration()

    # print("Next gen OK !")

    # best = pop.selectTheBest()
    # print(f"Best 1 : {best1.genom}")
    # print(f"Fitness 1 : {best1.evaluate()}")
    # print(f"Best 2 : {best.genom}")
    # print(f"Fitness 2 : {best.evaluate()}")

    # print("\nSelect the best OK !")

    ind = Individu([3, 2, 0, 1, 1, 2, 14, 21, 23, 2, 5, 50])
    print(ind.fitness)
    Population.evaluate_population([ind])
    print(ind.evaluate())
    
