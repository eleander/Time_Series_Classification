import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

runs = 3


start_time = 30
end_time = 100
cutoff = 30
power = 100

## S1

# Function to create the a and b constant of S1
# Rule: b - a < cutoff 
def s1_constants(): 
    a = random.randint(0, start_time)
    b = random.randint(a, a + cutoff)
    return a,b

# Given a and b 
# If x < a, return 0 because motor didn't start yet
# If a < x < b, return power since motor is active
# If x > b, return 0 because motor stopped operation
def s1(x,a,b):
 if(x < a): return 0
 if(a<=x<=b): return power 
 else: return 0

lists = []

# Generate a run of S1
def s1_generator():
    # Return a numpy array starting at 0-end_time with 1 as the increment
    x = np.arange(0, end_time, 1)

    # Get the a and b constant for this run
    a, b = s1_constants()

    # Use the s1 function to get the results for each time
    y = []
    for i in range(len(x)):
       y.append(s1(x[i], a, b))
    return y


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