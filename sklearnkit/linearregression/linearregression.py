import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

correlex1 = pd.read_csv('correl_ex1.csv')

reg = LinearRegression().fit(np.array(correlex1['comerciais']).reshape(-1,1), correlex1['vendas'])

print(reg.coef_)
print(reg.intercept_)
pred = reg.predict(np.array([1]).reshape(-1,1))
print(pred)