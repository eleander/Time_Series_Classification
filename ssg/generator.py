import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Number of runs
runs = 10000

# Constants
start_time = 30
end_time = 100
cutoff = 30
power = 100
# Determines whether power should consistently be equal to power
# Or...if the value can vary
is_random = True

## Import Relevant Duty Cycle
from s3 import s3_generator as generator

# For each run, append to lists
# In this case, only s1 was used so that it could be tested
lists = []
for val in range(runs):
    # No randomness = consistent value
    if is_random == False:
        lists.append(generator(power))
    # Allow randomness = vary from 50 to 100
    else:
        rand_power = random.randint(50, power)
        lists.append(generator(rand_power))

# Return a numpy array starting at 0-end_time with 1 as the increment
x = np.arange(0, end_time, 1)

# Convert the list of lists into a numpy array
numpyArray = np.array(lists)

# Create a dataframe where each row is a run
panda_df = pd.DataFrame(
    data=numpyArray,
    columns=x,
)

panda_df.to_csv("../datasets/" + "s3_w_vol.csv", index=False)
