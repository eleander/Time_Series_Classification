import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Constants
start_time = 30
end_time = 100
cutoff = 30

from numpy.polynomial import polynomial as P

# time_started: when does motor start?
# root_1 first root of quadratic function
# root_2 second root of quadratic. Note root_2 = root_1 + (value between 15 - 20)
# x0,y0 is coordinates of max height of polynomial
# poly_time_ended is a x value from the (halfway point of x0 and root_2) and (3/4 point of x0 and root_2)
# tc: operation time at constant load
def s4_constants():
    time_started = random.randint(0, start_time)
    root_1 = time_started
    root_2 = random.randint(root_1 + 15, root_1 + 20)

    p = P.Polynomial.fromroots([root_1, root_2])
    flipped_p = -p

    c, b, a = flipped_p.coef
    x0 = -b / (2 * a)
    y0 = flipped_p(x0)

    poly_time_ended = random.randint(
        int(x0 + (root_2 - x0) / 1.5), int(root_2 - (root_2 - x0) / 4)
    )
    y_line = flipped_p(poly_time_ended)

    tc = random.randint(10, 30)
    return time_started, flipped_p, x0, y0, poly_time_ended, y_line, tc


# If x < time_started, motor didn't start yet
# If time_started < x < poly_time_ended, currently in polynomial mode thus return poly(x)
# If poly_time_ended < x < poly_time_ended + tc, currently in line mode at where y = y_line
def s4(x, time_started, flipped_p, x0, y0, poly_time_ended, y_line, tc):
    if x < time_started:
        return 0
    if time_started < x <= poly_time_ended:
        return flipped_p(x)
    if poly_time_ended <= x < poly_time_ended + tc:
        return y_line
    else:
        return 0


lists = []

# Generate a run of S4
def s4_generator():
    # Return a numpy array starting at 0-end_time with 1 as the increment
    x = np.arange(0, end_time, 1)

    # Get the a and b constant for this run
    time_started, flipped_p, x0, y0, poly_time_ended, y_line, tc = s4_constants()

    # Use the s1 function to get the results for each time
    y = []
    for i in range(len(x)):
        y.append(s4(x[i], time_started, flipped_p, x0, y0, poly_time_ended, y_line, tc))
    return y
