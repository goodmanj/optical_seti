import numpy as np
from matplotlib import pyplot as plt
from astropy.io import fits

# ##### 1.  STATISTICS FUNCTIONS

# Calculate running median of x, using window size.
# Output size is arr1 size - window_size
# Use sliding window view for speed, see
# https://numpy.org/devdocs/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html
def running_median(x, window_size):
  return np.median(np.lib.stride_tricks.sliding_window_view(x,window_size),1)

# Calculate running median of arr1, using window size.
# Uses a for loop instead of numpy tricks: much slower.  For testing only.
def running_median_old(arr1,window_size):
    fluxes = np.array(arr1)
    median_iterations = len(arr1) - window_size + 1
    running_median = []
    for i in range(0, median_iterations):
        start = i 
        end = i + window_size
        running_median.append(np.median(fluxes[start:end])) 
    return(running_median)

                  
# Calculate running mean of x, using window size.
# Output size is arr1 size - window_size
# Use sliding window view for speed, see
# https://numpy.org/devdocs/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html
def running_mean(x, window_size):
  return np.mean(np.lib.stride_tricks.sliding_window_view(x,window_size),1)

# Calculate running mean of arr1, using window size.
# Uses a for loop instead of numpy tricks: much slower.  For testing only.
def running_mean_old(arr1, window_size):
    fluxes = np.array(arr1)
    mean_iterations = len(fluxes) - window_size + 1
    running_mean = []
    for i in range(0, mean_iterations):
        start = i 
        end = i + window_size
        running_mean.append(np.mean(fluxes[start:end])) 
    return(running_mean)

# Calculate running standard dev of x, using window size.
# Output size is arr1 size - window_size
# Use sliding window view for speed, see
# https://numpy.org/devdocs/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html
def running_standarddev(x, stwindow):
   return np.std(np.lib.stride_tricks.sliding_window_view(x,stwindow),1)

# Calculate running stdev of arr1, using window size.
# Uses a for loop instead of numpy tricks: much slower.  For testing only.
def running_standarddev_old(arr1, stwindow):
    import numpy as np
    fluxes = np.array(arr1)
    standard_iterations = len(arr1) - stwindow + 1
    running_stdeviation = []
    for i in range(0, standard_iterations):
        start = i 
        end = i + stwindow
        running_stdeviation.append(np.std(fluxes[start:end])) 
    return(running_stdeviation)

# ##### 2.  FILE LOADING

# Read a HARPS data file.
# Input arguments:
#   file: filename
# Output arguments:
#   wave: wavelength data (nm)
#   arr1: spectral brightness data

def read_harps_file(file):
    fits_file = fits.open(file)
    spectral_data = fits_file[1].data
    wave = spectral_data[0][0]
    arr1 = spectral_data[0][1]
    return wave, arr1

# ##### 3.  SEARCH ALGORITHM

# The main optical seti search routine.  Identifies spikes that rise more than
# threshold_multiplier times the local standard deviation above the local median.
# Spikes must have at least min_count and no more than max_count pixels in a row
# above the threshold.
# 
# Input arguments:
#   arr1: spectral intensity
#   min_cont: minimum number of bright pixels in a row to count as a spike
#   max_count: maximum number of bright pixels in a row to count as a spike
#   threshold_multiplier: how many standard deviations above median must pixel be to count as a spike
#   cosmic_ray_threshold: unused
#   window_size: running median/stdev window size
# Output arguments: 
#   hits_start: list of indices of start of identified spikes
#   hits_end: list of indices of end of identified spikes
#   count: number of spikes found

def seti_spike_analyzer(arr1, min_count = 4, max_count = 8, threshold_multiplier = 3.5, window_size = 101):
    half_window_size = round((window_size-1)/2)
    continuum = running_median(arr1, window_size)
    count = 0 #reset bright pixel count variable
#    import numpy as np # JCG: Not needed
    flux_threshold = np.array(running_standarddev(arr1, window_size)) * (threshold_multiplier)
#    cosmic_ray_threshold = np.array(running_standarddev(arr1, stwindow)) * (cosmic_ray_threshold) # JCG: Not used
    hits_start = []  # List of starting wavelength indices for spikes
    hits_end = []    # List of ending wavelength indices for spikes
    # List of known airglow lines, this needs to be clearer
    prohibited_wavelengths = list(range(179450, 179650)) + list(range(251750, 251950)) + list(range(210750, 210950)) + list(range(258150, 258350)) + list(range(141550, 141750)) + list(range(141750, 141950)) + list(range(211350, 211550)) # JCG: This is damn ugly
    # Loop over all wavelengths where "continuum" has been calculated.
    for i in range(50,len(continuum) - half_window_size):
            if arr1[i] >= continuum[i - half_window_size] + flux_threshold[i - half_window_size]:  # If pixel is above threshold
                  count += 1                                           # increment count
            else:                                                      # if pixel falls below threshold
                if (count >= min_count) and (count <= max_count):      # if spike isn't too wide or narrow
                    if i not in prohibited_wavelengths:                # if it's not in our list of airglow lines
                        hits_start.append(i-count)                     # Add to the list of spikes found
                        hits_end.append(i)
                count = 0
    print(hits_start, hits_end)
    return hits_start, hits_end, count                                 # Return list of hits found, and number of hits

# ##### 4.  PLOTTING

# Plot spectral data between index1 and index2.
def original_spectrum_plot(wave, arr1, index1, index2):
    plt.plot(wave[index1:index2], arr1[index1:index2], '.-')

# JCG: Plot spectral data with continuum and flux threshold lines.
# Could easily be combined with zoomin_spike_plotter.
# Not used in any other .py
#
# file: HARPS spectrum filename
# window_size: window size for running medians and stdev
# threshold_multiplier: how many standard deviations above median to plot threshold line
# center_index: Index of center of graph
# graph_width: Width of graph (number of data points)

def spike_plotter(file, window_size = 101, threshold_multiplier = 3.5, center_index = 1000): 
    wave, arr1 = read_harps_file(file)
    continuum = running_median(arr1,window_size) 
    start_index = (center_index - 1000)
    end_index = (center_index + 1000)
    threshold = continuum + np.array(running_standarddev(arr1, window_size)) * threshold_multiplier
    x = wave[start_index:end_index]
    plt.plot(x, arr1[start_index:end_index],'.-', x, continuum[(start_index - 50):(end_index - 50)], x, threshold[(start_index - 50):(end_index - 50)])
    plt.savefig(str(file[48:]) + "zoom_out" + ".png")
    start_index = (center_index - 100)
    end_index = (center_index + 100)
    x = wave[start_index:end_index]
    plt.plot(x, arr1[start_index:end_index],'.-', x, continuum[(start_index - 50):(end_index - 50)], x, threshold[(start_index - 50):(end_index - 50)])
    plt.savefig(str(file[48:]) + "zoom_in" + ".png")

