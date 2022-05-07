# Imports
import pandas as pd 
import numpy as np
from numpy.random import default_rng
rng = default_rng()

# Define file names to use for classification
file_names = ["s1_w_vol", "s2_w_vol", "s3_w_vol", "s4_w_vol"]

# Get df from file and store in combined_df and y
# Specify number of rows to use in classifcation
dfs= []
y = []
for file_name in file_names:
    print(f"Reading file {file_name}")
    df = pd.read_csv("../datasets/"+file_name+".csv")
    # Drop Run_1, Run_2, etc
    df.drop(columns=df.columns[:1],axis=1, inplace=True)
    dfs.append(df)

noise_dfs = []

mu, sigma = 1, 0.1
max_noise = 10

count = 1

# Add volatility to each dataframe
for df in dfs: 
    print(f"Currently on df {count} out of {len(dfs)}")
    noise_df = df.copy()
    for run in range(len(noise_df.index)): 
        if run % 100 == 0:
            print(f"On run {run} out of {len(noise_df.index)}") 
        noise = (rng.normal(mu, sigma, len(noise_df.columns)))
        # Noise has max value of 1, noise * max_noise results in max value
        # of max_noise
        noise = (noise * max_noise)
        noise_df.iloc[run] = noise_df.iloc[run] + noise

        num = noise_df._get_numeric_data()

        num[num > 100 ] = 100
        num[num < 0 ] = 0
        
        noise_dfs.append(noise_df)
    print(f"Finished adding noise to {count} out of {len(dfs)} \n")
    count = count + 1

# Save each dataframe
for file_name, noise_df in zip(file_names, noise_dfs):
    print(f"Saving {file_name} to w_vol folder")
    noise_df.to_csv("../datasets/w_vol/"+file_name+".csv")
    print(f"Saved {file_name} to w_vol folder")

