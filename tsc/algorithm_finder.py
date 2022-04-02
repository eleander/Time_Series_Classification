# Imports
import pandas as pd 
import numpy as np 
from sklearn.metrics import accuracy_score

from sktime.datatypes._panel._convert import (
    from_2d_array_to_nested,
    from_nested_to_2d_array,
    is_nested_dataframe,
)

# Helper function to get classifier name
def get_clf_name(estimator):
    return(estimator.__class__.__name__)

def get_clf_class(estimator):
    return clf.__class__.__module__.split(".")[2]

# Define file names to use for classification
file_names = ["s1_no_vol", "s2_no_vol"]

# Get df from file and store in combined_df and y
# Specify number of rows to use in classifcation
dfs= []
y = []
for file_name in file_names:
    df = pd.read_csv ("../datasets/"+file_name+".csv", nrows=10)
    df.drop(columns=df.columns[:1],axis=1, inplace=True)
    nested_df = from_2d_array_to_nested(df)
    y.extend([file_name[1]] * df.shape[0])
    dfs.append(nested_df)

y = np.asarray(y)
combined_df = pd.concat(dfs)

# Train / test split of data
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(combined_df, y)

# Define classifiers that will be used in algorithm finder
from sktime.classification.dictionary_based import IndividualBOSS
from sktime.classification.dictionary_based import ContractableBOSS


# Come back
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

clfs.append(ContractableBOSS(n_parameter_samples=25, max_ensemble_size=5))
clfs.append(IndividualBOSS())
clfs.append(BOSSEnsemble(max_ensemble_size=5))
clfs.append(KNeighborsTimeSeriesClassifier())
clfs.append(ElasticEnsemble(
    proportion_of_param_options=0.1,
    proportion_train_for_test=0.1,
))
clfs.append(ProximityForest(n_estimators=5))
clfs.append(HIVECOTEV2(
    stc_params={
        "estimator": RotationForest(n_estimators=3),
        "n_shapelet_samples": 500,
        "max_shapelets": 20,
        "batch_size": 100,
    },
    drcif_params={"n_estimators": 10},
    arsenal_params={"num_kernels": 100, "n_estimators": 5},
    tde_params={
        "n_parameter_samples": 25,
        "max_ensemble_size": 5,
        "randomly_selected_params": 10,
    },
))
clfs.append(TimeSeriesForestClassifier(n_estimators=10))
clfs.append(RandomIntervalSpectralEnsemble(n_estimators=10))
clfs.append(ShapeletTransformClassifier(
    estimator=RotationForest(n_estimators=3),
    n_shapelet_samples=500,
    max_shapelets=20,
    batch_size=100,
))


# Append type of algorithm (eg. dictionary_based)
types = []

for clf in clfs: 
    types.append(get_clf_class(type))

# Classify the dataset
acc_scores = []

import time

times = []
for count, clf in enumerate(clfs): 
    start = time.time()
    print(f"Training {count+1} out of {len(clfs)}")
    print(f"Currently on: {get_clf_name(clf)}")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc_score = accuracy_score(y_test, y_pred)
    acc_scores.append(acc_score)
    end = time.time()
    time_elapsed_ms = (end - start)*1000
    times.append(time_elapsed_ms)
    print(f"The time elapsed was: {time_elapsed_ms} ms")


# Sort according to type
types, acc_scores, clfs = zip(*sorted(zip(types, acc_scores, clfs), key=lambda pair: pair[0]))

# Print Results 
print()
print(f"{'Type' : <20}{'Name' : <40}{'Accuracy' : <15}{'Time in ms' : <15}")
for type, clf, acc_score, time_ms in zip(types, clfs, acc_scores, times):
    acc_score_perc = '{:0.0f}'.format(acc_score*100)
    print(f"{get_clf_class(clf): <20}{get_clf_name(clf) : <40}{(acc_score_perc)+'%':<15}{time_ms : <15}")
