# Imports
from random import random
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

seed = 2022

from sktime.datatypes._panel._convert import (
    from_2d_array_to_nested,
)

# Helper function to get classifier name
def get_clf_name(estimator):
    return estimator.__class__.__name__


def get_clf_class(clf):
    return clf.__class__.__module__.split(".")[2]


# Define file names to use for classification
file_names = ["s1_w_vol", "s2_w_vol", "s3_w_vol", "s4_w_vol"]

# Get df from file and store in combined_df and y
# Specify number of rows to use in classifcation
dfs = []
y = []
for file_name in file_names:
    df = pd.read_csv("../datasets/w_vol_and_rand/" + file_name + ".csv", nrows=1000)
    nested_df = from_2d_array_to_nested(df)
    y.extend([file_name[1]] * df.shape[0])
    dfs.append(nested_df)

y = np.asarray(y)
combined_df = pd.concat(dfs)

print(f"\nThe number of rows received are {len(combined_df.index)}")
print(f"The number of y values received are {len(y)}")

# Train / test split of data
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(combined_df, y, random_state=seed)
print(f"Length of X_train is {len(X_train)} and y_train is {len(y_train)}")
print(f"Length of X_test is {len(X_test)} and y_test is {len(y_test)}\n")


# Define classifiers that will be used in algorithm finder
from sktime.classification.dictionary_based import IndividualBOSS
from sktime.classification.dictionary_based import ContractableBOSS
from sktime.classification.dictionary_based import BOSSEnsemble
from sktime.classification.distance_based import KNeighborsTimeSeriesClassifier
from sktime.classification.distance_based import ElasticEnsemble
from sktime.classification.distance_based import ProximityForest
from sktime.classification.hybrid import HIVECOTEV2
from sktime.contrib.vector_classifiers._rotation_forest import RotationForest
from sktime.classification.interval_based import TimeSeriesForestClassifier
from sktime.classification.interval_based import RandomIntervalSpectralEnsemble
from sktime.classification.shapelet_based import ShapeletTransformClassifier
from sktime.contrib.vector_classifiers._rotation_forest import RotationForest

clfs = []

clfs.append(
    ContractableBOSS(n_parameter_samples=25, max_ensemble_size=5, random_state=seed)
)
clfs.append(IndividualBOSS(random_state=seed))
# clfs.append(BOSSEnsemble(max_ensemble_size=5, random_state=seed))
clfs.append(KNeighborsTimeSeriesClassifier())
# # Refer to s1_s2_no_vol_10_runs.txt
# # Time to train these algorithms are too long 30,000 ms for only 10 runs for s1 and s2

# clfs.append(
#     ElasticEnsemble(
#         proportion_of_param_options=0.1,
#         proportion_train_for_test=0.1,
#         random_state=seed,
#     )
# )
# clfs.append(ProximityForest(n_estimators=5, random_state=seed))
# clfs.append(
#     HIVECOTEV2(
#         stc_params={
#             "estimator": RotationForest(n_estimators=3, random_state=seed),
#             "n_shapelet_samples": 500,
#             "max_shapelets": 20,
#             "batch_size": 100,
#         },
#         drcif_params={"n_estimators": 10},
#         arsenal_params={"num_kernels": 100, "n_estimators": 5},
#         tde_params={
#             "n_parameter_samples": 25,
#             "max_ensemble_size": 5,
#             "randomly_selected_params": 10,
#         },
#         random_state=seed,
#     )
# )
clfs.append(TimeSeriesForestClassifier(n_estimators=10, random_state=seed))
# clfs.append(RandomIntervalSpectralEnsemble(n_estimators=10, random_state=seed))
clfs.append(
    ShapeletTransformClassifier(
        estimator=RotationForest(n_estimators=3, random_state=seed),
        n_shapelet_samples=500,
        max_shapelets=20,
        batch_size=100,
        random_state=seed,
    )
)


# Append type of algorithm (eg. dictionary_based)
types = []

for clf in clfs:
    types.append(get_clf_class(clf))

# Classify the dataset
acc_scores = []
f1_scores = []

import time

times = []
for count, clf in enumerate(clfs):
    print(f"Training {count+1} out of {len(clfs)}")
    print(f"Currently on: {get_clf_name(clf)}")
    start = time.time()
    clf.fit(X_train, y_train)
    end = time.time()
    y_pred = clf.predict(X_test)
    acc_score = accuracy_score(y_test, y_pred)
    f1_score_val = f1_score(y_test, y_pred, average="weighted")
    f1_scores.append(f1_score_val)
    acc_scores.append(acc_score)
    time_elapsed_ms = (end - start) * 1000
    times.append(time_elapsed_ms)
    print(f"The accuracy was {acc_score}")
    print(f"The f1 score was {f1_score_val}")
    print(f"The time elapsed was: {time_elapsed_ms} ms")


# Sort according to type
types, acc_scores, f1_scores, clfs = zip(
    *sorted(zip(types, acc_scores, f1_scores, clfs), key=lambda pair: pair[0])
)

# Print Results
print()
print(
    f"{'Type' : <20}{'Name' : <40}{'Accuracy' : <15}{'F1 Score' : <15}{'Time in ms' : <15}"
)
for type, clf, acc_score, f1_score_val, time_ms in zip(
    types, clfs, acc_scores, f1_scores, times
):
    acc_score_perc = f"{acc_score*100:.2f}"
    f1_score_perc = f"{f1_score_val*100:.2f}"
    time_ms_redu = f"{time_ms:.2f}"

    print(
        f"{get_clf_class(clf): <20}{get_clf_name(clf) : <40}{(acc_score_perc)+'%':<15}{(f1_score_perc)+'%':<15}{time_ms_redu : <15}"
    )
