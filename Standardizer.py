import pandas as pa
from collections import Counter
from math import sqrt

class Standardizer:

    def __init__(self, mean = None, deviation = None):
        self.mean = mean
        self.deviation = deviation

    def fit(self, df : pa.DataFrame):
        self.mean = {}
        self.deviation = {}
        for col in df.columns:
            col_values = df[col]
            self.mean[col] = 0
            self.deviation[col] = 0
            for val in col_values:
                if df[col].dtype == 'int64' or df[col].dtype == 'float64':
                    self.mean[col] += val
                    self.deviation[col] += val ** 2

        for col in self.mean:
            self.mean[col] = self.mean[col] / len(df)
            self.deviation[col] = sqrt((self.deviation[col] / len(df)) - (self.mean[col] ** 2))

    def transform(self, df : pa.DataFrame):
        df = df.reset_index(drop=True)
        if self.mean == None or self.deviation == None:
            raise Exception("Standardizer is not fitted")
        for col in df.columns:
            if df[col].dtype == 'int64' or df[col].dtype == 'float64':
                df[col] = df[col].astype('float64')
                for i in range(len(df)):
                    df.loc[i, col] = (df.loc[i, col] - self.mean[col]) / self.deviation[col]
            if df[col].dtype == "bool":
                df[col] = df[col].astype('float64')

        return df
            

        

if __name__ == "__main__":

    df = pa.read_csv("C:/Users/romai/Documents/M1/S1/Python for AI/Hearth disiz/heart.csv")

    print("PreStandard :")
    print(df.head())

    scaler = Standardizer()

    scaler.fit(df)
    df = scaler.transform(df)

    print("PostStandard :")
    print(df.head())