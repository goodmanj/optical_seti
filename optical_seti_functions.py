def running_median(fluxes, window_size):
    import numpy as np
    fluxes = np.array(fluxes)
    median_iterations = len(fluxes) - window_size + 1
    running_median = []
    for i in range(0, median_iterations):
        start = i 
        end = i + window_size
        running_median.append(np.median(fluxes[start:end])) 
    return(running_median)

def running_mean(fluxes, window_size):
    import numpy as np
    fluxes = np.array(fluxes)
    mean_iterations = len(fluxes) - window_size + 1
    running_mean = []
    for i in range(0, mean_iterations):
        start = i 
        end = i + window_size
        running_mean.append(np.mean(fluxes[start:end])) 
    return(running_mean)
