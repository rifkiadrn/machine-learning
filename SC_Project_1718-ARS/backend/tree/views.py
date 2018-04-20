from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .utils import data_manipulations, functions
from .decision_tree import RegressionTree, ClassificationTree
from .utils.functions import mean_squared_error, accuracy_score
from .utils.data_manipulations import standardize, train_test_split, k_fold_cross_validation_sets
from sklearn.preprocessing import RobustScaler
from ars_backend.settings import PROJECT_ROOT
import time
import numpy as np
import csv
import pickle
import os

CSV_PATH = os.path.join(PROJECT_ROOT, '../tree/movie_metadata.csv')

def main() -> object:
    X = np.array([0,0,0,0,0,0,0])
    y = np.array([0])

    with open(CSV_PATH) as f:
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
                    y = np.vstack((y, [target])) #scores
                    X = np.vstack((X, column))
            except Exception as e:
                pass

    model = ClassificationTree()
    y = y[:, 0]
    X = standardize(X)
    datasets = k_fold_cross_validation_sets(X, y, 3)

    for data in datasets:
        X_train, X_test, y_train, y_test = data
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(accuracy_score(y_test, y_pred))
        mse = mean_squared_error(y_test, y_pred)
        print("Mean Squared Error:", mse)
    filename = os.path.join(PROJECT_ROOT, 'finalized_model.pikle')
    pickle.dump(model, open(filename, 'wb'))
    model_a = pickle.load(open(filename, 'rb'))


class TrainingModel(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        try:
            main()
            return Response({"status": "success"}, status= status.HTTP_200_OK)
        except Exception as e:
            return  Response({"status" : "failed", "data" : e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





