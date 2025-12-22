from NeuralNetModel import NeuralNetModel
from Preprocessor import Preprocessor
from random import randint

class Individu:

    lb = [1,1,1,1]
    ub = [4,4,4,4]
    len_genom = 4

    datapath = ""

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

    def decodePreprocess(self):
        return Preprocessor(self.genom)
    
    def decodeModel(self):
        modelType = self.genom[Preprocessor.len_strat]
        if modelType == 1:
            return NeuralNetModel(self.genom)

    def evaluate(self):
        preprocess = self.decodePreprocess()
        model = self.decodeModel()
        X_train, y_train, X_test, y_test = preprocess.transform(Individu.datapath)

        model.fit(X_train, y_train)

        return model.evaluate(X_test, y_test)
    
    def __str__(self):
        return str(self.genom)