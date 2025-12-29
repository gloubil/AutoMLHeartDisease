from genomeUtils import *
import pandas as pa
import numpy as np
from sklearn.model_selection import train_test_split
from Standardizer import Standardizer

class Preprocessor:

    len_strat = 4
    test_size = 0.3

    def __init__(self, stratSegment = None):
        if stratSegment == None:
            self.strat = Preprocessor.getStrategies([0 for i in range(Preprocessor.len_strat)])
        else:
            self.strat = Preprocessor.getStrategies(stratSegment)
        self.scaler = None


    def transform(self, filepath):
        df = pa.read_csv(filepath)

        for col in df.columns:
            if df[col].dtype == 'int64':
                    df[col] = df[col].astype('float64')



        objColumns = []
        for c in df.columns:
            if isinstance(df[c].to_numpy()[0], str):
                objColumns.append(c)

        df = pa.get_dummies(df, columns=objColumns)

        for s in self.strat:
            df = s(df)
            df.reset_index(drop=True)

        df_train, df_test = train_test_split(df, test_size=Preprocessor.test_size)

        df = df.reset_index(drop=True)
        df_train = df_train.reset_index(drop=True)
        df_test = df_test.reset_index(drop=True)

        y = df["HeartDisease"]
        X = df.drop("HeartDisease", axis=1)
        y_train = df_train["HeartDisease"]
        X_train = df_train.drop("HeartDisease", axis=1)
        y_test = df_test["HeartDisease"]
        X_test = df_test.drop("HeartDisease", axis=1)

        scaler = Standardizer()
        scaler.fit(X)

        X = scaler.transform(X)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        return X_train, y_train, X_test, y_test

    def getDataFrame(self):
        return self.df

    @staticmethod
    def normalToPreprocessed(df, scaler : Standardizer = None, separateY : bool = False):
        objColumns = []
        for c in df.columns:
            if isinstance(df[c].to_numpy()[0], str):
                objColumns.append(c)

        if separateY:
            df = pa.get_dummies(df, columns=objColumns+['HeartDisease'])
        else:
            df = pa.get_dummies(df, columns=objColumns)



        y = df.filter(like="HeartDisease")
        
        X = df.drop(columns=y.columns, axis=1)
        
        if scaler is None:
            scaler = Standardizer()
            scaler.fit(X)

        X = scaler.transform(X)
        
        return X, y.to_numpy(), scaler    

    def getScaler(self):
        return self.scaler

    @staticmethod
    def chooseFunction(i_param, strat):
        restingBP = [doNothingRestingBP, removeZerosRestingBP, zerosByMeanCholesterol, zeroByMedianRestingBP, knnInferRestingBP]
        cholesterol = [doNothingCholesterol, zerosByMeanCholesterol, zerosByMedianCholesterol, knnInferCholesterol]
        oldpeak = [doNothingOldpeak, perRangeOldpeak, rmAberrantOldpeak, aberrantByMeanOldpeak, aberrantByMedianOldpeak]
        maxHR = [doNothingMaxHR, categorizeMaxHR]
        strategies = [restingBP, cholesterol, oldpeak, maxHR]

        return strategies[i_param][strat]

    @staticmethod
    def getStrategies(ind):
        strat = []
        for i in range(Preprocessor.len_strat):
            strat.append(Preprocessor.chooseFunction(i, ind[i]))
        return strat
    
if __name__ == "__main__":

    filepath = "C:/Users/romai/Documents/M1/S1/Python for AI/Hearth disiz/heart.csv"

    preprocessor = Preprocessor()

    X_train, y_train, X_test, y_test = preprocessor.transform(filepath)

    print(X_test)
    print(y_test)