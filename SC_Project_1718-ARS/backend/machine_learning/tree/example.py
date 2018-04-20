import time
start_time = time.time()
import numpy as np
from sklearn.preprocessing import RobustScaler
from decision_tree import RegressionTree, ClassificationTree
from utils.functions import mean_squared_error, accuracy_score
from utils.data_manipulations import standardize, train_test_split, k_fold_cross_validation_sets
import csv
import pickle
X = np.array([0,0,0,0,0,0,0])
y = np.array([0])

with open('movie_metadata.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        try:
            column = np.array([])
            column = np.hstack((column, float(row['duration'])))
            column = np.hstack((column, float(row['director_facebook_likes'])))
            column = np.hstack((column, float(row['actor_1_facebook_likes'])))
            column = np.hstack((column, float(row['actor_2_facebook_likes'])))
            column = np.hstack((column, float(row['actor_3_facebook_likes'])))
            column = np.hstack((column, float(row['budget'])))
            column = np.hstack((column, float(row['facenumber_in_poster'])))
            target = float(row['imdb_score'])
            target = int(target)
            if target >= 4 and target <= 8:
                y = np.vstack((y, [target]))#scores
                X = np.vstack((X, column))
            # dataset.append(Instance( [ncfr, dur, dfl, a3fl, a1fl, gr], [target] ))
        except Exception as e:
            pass

model = ClassificationTree()
X = standardize(X)
# X = RobustScaler(quantile_range=(25, 75)).fit_transform(X)
# X = MinMaxScaler().fit_transform(X)
# # # print y
datasets = k_fold_cross_validation_sets(X, y, 3)

for data in datasets:
    X_train, X_test, y_train, y_test = data
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(accuracy_score(y_test, y_pred))
    # print accuracy_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)
    # print (model.predict(np.array([[178, 0, 1000, 936]])))
    print(model.predict(np.array([[178, 0, 1000, 936, 855, 237000000, 0]])))

# model.print_tree()

filename = 'finalized_model.pikle'
pickle.dump(model, open(filename, 'wb'))

model_a = pickle.load(open(filename, 'rb'))

# print (model_a.predict(np.array([[178, 0, 1000, 936, 855, 237000000, 0]])))
print (model_a.predict(np.array([[178, 0, 1000, 936, 855, 237000000, 0]])))