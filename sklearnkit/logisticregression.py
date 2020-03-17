import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

titanic = pd.read_csv('titanic.csv', ';')
titanic = pd.get_dummies(titanic, drop_first=True)

print(titanic.drop('Sobrevivente', axis=1))

X_train, y_train, X_test, y_test = train_test_split(
    titanic.drop('Sobrevivente', axis=1), titanic['Sobrevivente'])

reg = LogisticRegression(solver='lbfgs').fit(X_train, y_train)