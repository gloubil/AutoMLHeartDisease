from Model import Model
import keras
from keras import layers
from keras import ops
import pandas as pa
from numpy import isnan

class NeuralNetModel(Model):

    startIndex = 5
    verbose = 0
    tolerance = 0.5

    def __init__(self, genom):
        self.depth = genom[NeuralNetModel.startIndex]
        self.epochs = genom[NeuralNetModel.startIndex+6]
        # self.learning_rate = genom[NeuralNetModel.startIndex+6]
        # self.weight_decay = genom[NeuralNetModel.startIndex+7]
        
        self.model = keras.Sequential()

        for i in range(self.depth):
            self.model.add(layers.Dense(genom[NeuralNetModel.startIndex+1+i], activation="tanh"))
        self.model.add(layers.Dense(1, activation="sigmoid"))

        self.model.compile(
            optimizer=keras.optimizers.AdamW(),
            loss=keras.losses.binary_crossentropy,
            metrics=[keras.metrics.binary_crossentropy, keras.metrics.F1Score(average='weighted')]
        )

        self.fitted = False

    def evaluate(self, X_test : pa.DataFrame, y_test):
        # return self.model.evaluate(X_test, y_test, 64, verbose=NeuralNetModel.verbose)[2]

        matrix = {"TP" : 0, "FP" : 0, "FN" : 0}

        y_predict = []
        for line in X_test.to_numpy():
            line = line.reshape(1, -1)
            y_predict.append(self.model.predict(line, verbose=NeuralNetModel.verbose)[0][0])

        for i in range(len(y_predict)):
            if y_predict[i] > NeuralNetModel.tolerance:
                if y_test[i] == 1:
                    matrix["TP"] += y_predict[i]
                else:
                    matrix["FP"] += y_predict[i]
            else:
                if y_test[i] == 1:
                    matrix["FN"] += y_predict[i]

        
        score = (2 * matrix["TP"]) / (2 * matrix["TP"] + matrix["FP"] + matrix["FN"])

        if score < 0 or score > 1 or isnan(score):
            print("F1 Score computation error")
            return None

        return score

        

    def fit(self, X_train, y_train, force_fit = False):
        if force_fit == True or (force_fit == False and self.fitted == False):
            self.model.fit(X_train, y_train, 64, epochs=self.epochs, callbacks=[], verbose=NeuralNetModel.verbose)
        self.fitted = True

    def predict(self, X):
        return self.model.predict(X, verbose=NeuralNetModel.verbose)[0][0]

    def save(self):
        pass

    def load(filepath):
        pass

if __name__ == "__main__":
    model = NeuralNetModel([0,0,0,0,1,3,10,10,10,10,10,300])
    model.model.summary()