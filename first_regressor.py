import math

import numpy as np
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor

from load_dataset import get_featureDataframe, get_labels
from utils import RMSe, computeMSF

feature_df = get_featureDataframe()
labels_df = get_labels()

alcoholFreeTime = labels_df.loc[labels_df.Alcohol == 0].Time.apply(lambda x: x.to_pydatetime().replace(minute=0))
Test_time_without_sec = feature_df.Test_time.apply(lambda x: x.replace(minute=0, second=0))

y = computeMSF(feature_df, labels_df)

feature_df['Test_time'] = Test_time_without_sec
feature_df = feature_df.loc[feature_df.Test_time.isin(alcoholFreeTime.values)]

# feature_df['Test_time'] = Test_time_without_sec
# feature_df = feature_df.loc[feature_df.Test_time.isin(alcoholFreeTime.values)]
#
# alarmFreeTime = labels_df.loc[labels_df.Alarmclock == 0].Time.apply(lambda x: x.to_pydatetime().replace(minute=0))
# Test_time_without_sec = feature_df.Test_time.apply(lambda x: x.replace(minute=0, second=0))
#
# feature_df['Test_time'] = Test_time_without_sec
# feature_df = feature_df.loc[feature_df.Test_time.isin(alarmFreeTime.values)]
#
# caffeineFreeTime = labels_df.loc[labels_df.Caffeine == 0].Time.apply(lambda x: x.to_pydatetime().replace(minute=0))
# Test_time_without_sec = feature_df.Test_time.apply(lambda x: x.replace(minute=0, second=0))
#
# feature_df['Test_time'] = Test_time_without_sec
# feature_df = feature_df.loc[feature_df.Test_time.isin(caffeineFreeTime.values)]



# X = [[y] for y in feature_df.groupby(feature_df.Subject).positive_mean.mean().values]
# X = [[y] for y in feature_df.groupby(feature_df.Subject).positive_median.mean().values]
X = [[y] for y in feature_df.groupby(feature_df.Subject).q50_mean.mean().values]  # 0.34
# X = [[y] for y in feature_df.groupby(feature_df.Subject).q95_mean.mean().values]#0.096
# X = [[y] for y in feature_df.groupby(feature_df.Subject).q75_mean.mean().values]#0.63

X_train_set = X[:-2]
X_test_set = X[-2:]

y_train_set = y[:-2]
y_test_set = y[-2:]
# print(X_train_set)
# print(y_train_set)
#
model = LinearRegression()
model.fit(X_train_set, y_train_set)
predicted_set = model.predict(X_test_set)

error2 = RMSe(predicted_set, y_test_set)

print("Linear Regressor ", model.score(X_test_set, y_test_set))
print(error2)

clf = Ridge()
clf.fit(X_train_set, y_train_set)
predicted = clf.predict(X_test_set)
error3 = RMSe(predicted, y_test_set)
print("Ridge Score ", clf.score(X_test_set, y_test_set))
print(error3)

clf = Lasso()
clf.fit(X_train_set, y_train_set)
predicted = clf.predict(X_test_set)
error3 = RMSe(predicted, y_test_set)
print("Lasso Score ", clf.score(X_test_set, y_test_set))
print(error3)

clf = ElasticNet()
clf.fit(X_train_set, y_train_set)
predicted = clf.predict(X_test_set)
error3 = RMSe(predicted, y_test_set)
print("ElasticNet Score ", clf.score(X_test_set, y_test_set))
print(error3)

clf = GradientBoostingRegressor()
clf.fit(X_train_set, y_train_set)
predicted = clf.predict(X_test_set)
error3 = RMSe(predicted, y_test_set)
print("GradientBoostingRegressor Score ", clf.score(X_test_set, y_test_set))
print(error3)

clf = RandomForestRegressor()
clf.fit(X_train_set, y_train_set)
predicted = clf.predict(X_test_set)
error3 = RMSe(predicted, y_test_set)
print("RandomForestRegressor Score ", clf.score(X_test_set, y_test_set))
print(error3)

dtrModel = DecisionTreeRegressor()
dtrModel.fit(X_train_set, y_train_set)

rng = np.random.RandomState(1)
adaModel = AdaBoostRegressor(DecisionTreeRegressor(), n_estimators=300, random_state=rng)
adaModel.fit(X_train_set, y_train_set)

adaPredicted = adaModel.predict(X_test_set)
print("AdaBoostRegressor Score ", clf.score(X_test_set, y_test_set))
error3 = RMSe(adaPredicted, y_test_set)
print(error3)
