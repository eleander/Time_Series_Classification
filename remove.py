# Imports
from random import random
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

from sktime.datatypes._panel._convert import (
    from_2d_array_to_nested,
)

# Helper function to get classifier name
def get_clf_name(estimator):
    return estimator.__class__.__name__


def get_clf_class(estimator):
    return clf.__class__.__module__.split(".")[2]


# Define file names to use for classification
file_names = ["s1_w_vol", "s2_w_vol", "s3_w_vol", "s4_w_vol"]

for file_name in file_names:
    df = pd.read_csv("./datasets/" + file_name + ".csv")
    # df.drop(columns=df.columns[:1], axis=1, inplace=True)
    # df.to_csv("./datasets/" + file_name + "_drop" + ".csv")
    # df.drop("y", axis=1, inplace=True)
    print(df["y"])
