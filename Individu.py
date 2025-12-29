from NeuralNetModel import NeuralNetModel
from Preprocessor import Preprocessor
from random import randint

class Individu:

    error_genoms = []

    lb = [0,0,0,0,1,1,1,1,1,1,1,50]
    ub = [4,3,4,1,1,5,30,30,30,30,30,500]
    len_genom = 12

    datapath = "C:/Users/romai/Documents/M1/S1/Python for AI/Hearth disiz/heart.csv"

    verbose = True

    def __init__(self, genom):
        self.genom = genom
        self.fitness = -1

    @staticmethod
    def generateRandom():
        genom = []
        for i in range(Individu.len_genom):
            genom.append(randint(Individu.lb[i], Individu.ub[i]))
        return Individu(genom)
    
    def mutate(self):
        index = randint(0, Individu.len_genom-1)
        self.genom[index] = randint(Individu.lb[index], Individu.ub[index])
        self.fitness = -1

    def decodePreprocess(self):
        return Preprocessor(self.genom)
    
    def decodeModel(self):
        modelType = self.genom[Preprocessor.len_strat]
        if modelType == 1:
            return NeuralNetModel(self.genom)

    def evaluate(self):
        if self.fitness != -1:
            if Individu.verbose:
                print(f"{self.genom} -> {self.fitness}")
            return self.fitness
        preprocess = self.decodePreprocess()
        model = self.decodeModel()
        X_train, y_train, X_test, y_test = preprocess.transform(Individu.datapath)

        model.fit(X_train, y_train)

        self.fitness = model.evaluate(X_test, y_test)

        if self.fitness == None:
            Individu.error_genoms.append(self.genom)
            self.fitness = 0

        if Individu.verbose:
            print(f"{self.genom} -> {self.fitness}")
        return self.fitness
    
    def resetFitness(self):
        self.fitness = -1

    @staticmethod
    def static_evaluate(individu):
        score = individu.evaluate()
        individu.fitness = score
        return score

    def __str__(self):
        return str(self.genom)
    
if __name__ == "__main__":

    genom1 = [4, 1, 4, 1, 1, 1, 25, 5, 13, 27, 3, 448]
    genom2 = [0, 0, 0, 0, 1, 1, 25, 5, 13, 27, 3, 448]

    nb = 10

    avg1 = 0
    for i in range(nb):
        ind = Individu(genom1)
        avg1 += ind.evaluate()

    print()

    avg2 = 0
    for i in range(nb):
        ind = Individu(genom2)
        avg2 += ind.evaluate()


    avg1 = avg1/nb
    avg2 = avg2/nb

    print(avg1)
    print(avg2)