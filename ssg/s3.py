# time_started: when does motor start?
# tc: operation time at constant load
# to: time deenergized and at rest
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Constants
start_time = 30
end_time = 100
cutoff = 30


def s3_constants():
    time_started = random.randint(0, start_time)
    tc = random.randint(10, 30)
    to = random.randint(10, 30)
    return time_started, tc, to


# Given a and b
# If x < time_started, return 0 because motor didn't start yet
# If time_started < x < time_started + tc, return power since motor is active
# If time_started + tc < x < time_started + tc + to, return 0 since cycle 1 finished and cycle 2 not started yet
# If time_started + tc + to < x < time_started + tc + to + tc, return power since in cycle 2
# Else, return 0 since since both cycles complete
def s3(x, time_started, tc, to, power):
    if x < time_started:
        return 0
    if time_started < x < time_started + tc:
        return power
    if time_started + tc < x < time_started + tc + to:
        return 0
    if time_started + tc + to < x < time_started + tc + to + tc:
        return power
    else:
        return 0


lists = []

# Generate a run of S3
def s3_generator(power):
    # Return a numpy array starting at 0-end_time with 1 as the increment
    x = np.arange(0, end_time, 1)

    # Get the a and b constant for this run
    time_started, tc, to = s3_constants()

    # Use the s1 function to get the results for each time
    y = []
    for i in range(len(x)):
        y.append(s3(x[i], time_started, tc, to, power))
    return y
