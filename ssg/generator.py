import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

runs = 3

# Constants
start_time = 30
end_time = 100
cutoff = 30
power = 100

## S1

from s1 import s1_generator
from constants import runs, end_time

# For each run, append to lists
# In this case, only s1 was used so that it could be tested
lists = []
for val in range(runs): 
    lists.append(s1_generator())

# Return a numpy array starting at 0-end_time with 1 as the increment
x = np.arange(0, end_time, 1)

# Convert the list of lists into a numpy array
numpyArray = np.array(lists)

# Create a dataframe where each row is a run
panda_df = pd.DataFrame(data = numpyArray,
                        index = ['Run_' + str(i + 1) 
                        for i in range(numpyArray.shape[0])],
                        columns = x)


duty_cycle = np.full(runs, 1)

panda_df["y"] = duty_cycle

print(panda_df.shape)

panda_df.to_csv("../datasets/"+"s1.csv")