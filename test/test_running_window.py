# Test to make sure running medians calculated using np.lib.stride_tricks.sliding_window_view
# gives the same result as using a for loop.

import sys
from pathlib import Path
cwd = Path(__file__).parent.resolve() 
optical_seti_dir = cwd.parent.resolve() 
sys.path.append(str(optical_seti_dir))

import numpy as np
import optical_seti_functions

x = np.random.rand(1000)

x_old_medianfilter = optical_seti_functions.running_median_old(x,100)
x_new_medianfilter = optical_seti_functions.running_median(x,100)

print(np.max(np.abs(x_old_medianfilter - x_new_medianfilter)))

x_old_stdfilter = optical_seti_functions.running_standarddev_old(x,100)
x_new_stdfilter = optical_seti_functions.running_standarddev(x,100)

print(np.max(np.abs(x_old_stdfilter - x_new_stdfilter)))