import pandas as pa
from sklearn.neighbors import KNeighborsClassifier

# RestingBP
# Do nothing
# Remove Line == 0
# Replace by mean
# Replace by median
# Infer with knn

def doNothingRestingBP(df : pa.DataFrame):
    return df

def removeZerosRestingBP(df : pa.DataFrame):
    df = df.loc[df['RestingBP'] != 0]
    return df

def zerosByMeanRestingBP(df : pa.DataFrame):
    mean = float(int(df['RestingBP'].mean()))
    df.loc[df['RestingBP'] == 0] = mean
    return df

def zeroByMedianRestingBP(df : pa.DataFrame):
    median = float(int(df['RestingBP'].median()))
    df.loc[df['RestingBP'] == 0] = median
    return df

def knnInferRestingBP(df : pa.DataFrame):
    withoutMissing = df.loc[df['RestingBP'] != 0]
    y_w = withoutMissing['RestingBP']
    X_w = withoutMissing.drop('RestingBP', axis=1)

    # Fit KNN with good values
    knn = KNeighborsClassifier()
    knn.fit(X_w, y_w)

    # Getting missing values
    missing = df.loc[df['RestingBP'] == 0]
    X_m = missing.drop('RestingBP', axis=1)
    y_m = knn.predict(X_m)

    X_m.loc[X_m.index, 'RestingBP'] = y_m

    infered = X_m

    df.loc[infered.index] = infered

    return df




# Cholesterol
# Do nothing
# Replace by mean
# Replace by median
# Infer with knn

def doNothingCholesterol(df : pa.DataFrame):
    return df

def zerosByMeanCholesterol(df : pa.DataFrame):
    mean = float(int(df['Cholesterol'].mean()))
    df.loc[df['Cholesterol'] == 0] = mean
    return df

def zerosByMedianCholesterol(df : pa.DataFrame):
    median = float(int(df['Cholesterol'].median()))
    df.loc[df['Cholesterol'] == 0] = median
    return df

def knnInferCholesterol(df : pa.DataFrame):
    withoutMissing = df.loc[df['Cholesterol'] != 0]
    y_w = withoutMissing['Cholesterol']
    X_w = withoutMissing.drop('Cholesterol', axis=1)

    # Fit KNN with good values
    knn = KNeighborsClassifier()
    knn.fit(X_w, y_w)

    # Getting missing values
    missing = df.loc[df['Cholesterol'] == 0]
    X_m = missing.drop('Cholesterol', axis=1)
    y_m = knn.predict(X_m)

    X_m.loc[X_m.index, 'Cholesterol'] = y_m

    infered = X_m

    df.loc[infered.index] = infered

    return df


# Oldpeak
# Do nothing           
# Categorize per range (0-1, 1-2, etc.) One column per range and bool
# Remove aberrant
# Replace aberrant by mean
# Replace aberrant by median

def doNothingOldpeak(df : pa.DataFrame):
    return df

def perRangeOldpeak(df : pa.DataFrame):
    df_dummies = pa.get_dummies(
        pa.cut(df['Oldpeak'], bins=[-float('inf'), 0, 4, float('inf')], 
            labels=['below0', 'between', 'greater4']),
        prefix='Oldpeak'
    )

    df = pa.concat([df, df_dummies], axis=1)

    df = df.drop('Oldpeak', axis=1)

    return df

def rmAberrantOldpeak(df : pa.DataFrame):
    lb = 0
    ub = 4
    df = df.loc[df['Oldpeak'] >= lb]
    df = df.loc[df['Oldpeak'] <= ub]

    return df


def aberrantByMeanOldpeak(df : pa.DataFrame):
    lb = 0
    ub = 4
    mean = df['Oldpeak'].mean()
    df.loc[df['Oldpeak'] < lb] = mean
    df.loc[df['Oldpeak'] > ub] = mean

    return df

def aberrantByMedianOldpeak(df : pa.DataFrame):
    lb = 0
    ub = 4
    median = df['Oldpeak'].median()
    df.loc[df['Oldpeak'] < lb] = median
    df.loc[df['Oldpeak'] > ub] = median

    return df


# MaxHR
# Do nothing
# Categorize by low normal high, one column per category

def doNothingMaxHR(df : pa.DataFrame):
    return df

def categorizeMaxHR(df : pa.DataFrame):
    df_dummies = pa.get_dummies(
        pa.cut(df['MaxHR'], bins=[-float('inf'), 70, 180, float('inf')], 
            labels=['low', 'medium', 'high']),
        prefix='MaxHR'
    )

    df = pa.concat([df, df_dummies], axis=1)

    # df = df.drop('MaxHR', axis=1)

    return df


if __name__ == "__main__":
    df = pa.read_csv("C:/Users/romai/Documents/M1/S1/Python for AI/Hearth disiz/heart.csv")
    df = pa.get_dummies(df, columns=None)
    print(df)
    df = aberrantByMedianOldpeak(df)
    print(df)