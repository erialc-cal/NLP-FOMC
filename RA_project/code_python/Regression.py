import pandas as pd
import datetime
import matplotlib.pyplot as plt
import ast
import statsmodels.api as sm
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

project_directory = '/Users/etiennelenaour/Desktop/Stage/'


"""
Load data
"""


df_affirmation = pd.read_csv(project_directory + "csv_files/" + "df_affirmation_finale.csv")
df_chairman = pd.read_csv(project_directory + "csv_files/" + "df_chairman.csv")


df_affirmation_finale = pd.merge(df_chairman, df_affirmation[df_affirmation.columns[2:]])

base1 = df_affirmation_finale[df_affirmation_finale["ChairName"] == "CHAIRMAN GREENSPAN."]
base2 = df_affirmation_finale[df_affirmation_finale["ChairName"] == "CHAIRMAN BERNANKE."]

database = pd.concat([base1, base2], axis=0)


"""
Make Regression
"""

X = database[database.columns[2:]].drop(columns=['ScoreAffiWithoutChair']).drop(columns=['ScorePosti']).drop(columns=['nasdaq_value']) # here we have 2 variables for the multiple linear regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example
y = database['ScoreAffiWithoutChair']


X = sm.add_constant(X) # adding a constant
dummy_chair = X['ChairName'].map({'CHAIRMAN GREENSPAN.':0,'CHAIRMAN BERNANKE.':1})
X = X.drop(columns=['ChairName'])
X['dummy_chair'] = dummy_chair




X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())


"""
reg = RandomForestRegressor(max_depth=2, random_state=0)
reg.fit(X_train, y_train)

score_mae = np.sum(np.abs(reg.predict(X_test) - y_test)) / len(y_test)


importances = reg.feature_importances_
std = np.std([tree.feature_importances_ for tree in reg.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the impurity-based feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(X_train.shape[1]), importances[indices],
        color="r", yerr=std[indices], align="center")
plt.xticks(range(X_train.shape[1]), indices)
plt.xlim([-1, X_train.shape[1]])
plt.show()

print(score_mae)

print(np.std(y_test))
"""






