from Model import Model
from random import randint

class Individu:

    lb = []
    ub = []
    len_genom = 0

    def __init__(self, genom):
        self.genom = genom

    @staticmethod
    def generateRandom():
        genom = []
        for i in range(Individu.len_genom):
            genom.append(randint(Individu.lb[i], Individu.ub[i]))
        return Individu(genom)
    
    def mutate(self):
        index = randint(0, Individu.len_genom-1)
        self.genom[index] = randint(Individu.lb[index], Individu.ub[index])

    def decode(self):
        # TODO waiting for code
        return Model()

    def evaluate(self):
        model = self.decode()
        return model.evaluate()