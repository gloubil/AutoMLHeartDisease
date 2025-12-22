from genomeUtils import *
import pandas as pa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class Preprocessor:

    len_strat = 4
    test_size = 0.3

    def __init__(self, stratSegment = None):
        if stratSegment == None:
            self.strat = Preprocessor.getStrategies([0 for i in range(Preprocessor.len_strat)])
        else:
            self.strat = Preprocessor.getStrategies(stratSegment)
        self.scaler = StandardScaler()

    def transform(self, filepath):
        df = pa.read_csv(filepath)
        for s in self.strat:
            df = s(df)

        df = self.scaler.fit_transform(df)
        
        df_train, df_test = train_test_split(df, test_size=Preprocessor.test_size, random_state=53)

        y_train = df_train.filter(like="HeartDisease")
    
        X_train = df_train.drop(columns=y_train.columns, axis=1)

        y_test = df_test.filter(like="HeartDisease")
    
        X_test = df_test.drop(columns=y_test.columns, axis=1)

        return X_train, y_train, X_test, y_test

        
        

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