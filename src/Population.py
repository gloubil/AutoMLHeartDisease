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
    
    def cross(self, ind1, ind2):
        # TODO
        return ind1, ind2

    def nextGeneration(self):
        kBests = self.selectKBest()
        fifo = []
        len_fifo = 0
        # Prepare Childs
        while Population.k + len_fifo < Population.len_pop:
            a1 = randint(0, Population.k-1)
            a2 = randint(0, Population.k-1)
            child1, child2 = self.cross(kBests[a1], kBests[a2])
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