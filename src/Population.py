from Individu import Individu
from random import randint, random

class Population:

    maximize = True
    len_pop = 0
    k = 0
    mutate_rate = 0.5

    def __init__(self, individus):
        self.individus = individus

    def selectKBest(self):
        sorted_individus = self.individus.sort(key=lambda x: x.evaluate(), reverse=Population.maximize)
        return sorted_individus[:Population.k]
    
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

        return Population(newIndividus)

    @staticmethod
    def generateRandom():
        individus = [Individu.generateRandom() for i in range(Population.len_pop)]
        return Population(individus)
    

if __name__ == "__main__":
    ind1 = Individu.generateRandom()
    ind2 = Individu.generateRandom()

    child1, child2 = Population.cross(ind1, ind2)

    for i in range(1000):
        child1, child2 = Population.cross(child1, child2)
        assert len(child1.genom) == Individu.len_genom and len(child2.genom) == Individu.len_genom

print("Cross Test OK !")