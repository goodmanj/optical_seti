import numpy as np
from matplotlib import pyplot as plt

# Calculate running median of arr1, using window size.
# Output size is arr1 size - window_size
# Use sliding window view for speed, see
# https://numpy.org/devdocs/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html
def running_median(x, window_size):
  return np.median(np.lib.stride_tricks.sliding_window_view(x,window_size),1)

def running_median_old(arr1,window_size):
    fluxes = np.array(arr1)
    median_iterations = len(arr1) - window_size + 1
    running_median = []
    for i in range(0, median_iterations):
        start = i 
        end = i + window_size
        running_median.append(np.median(fluxes[start:end])) 
    return(running_median)

                  
# Calculate running mean of arr1, using window size.
# Output size is arr1 size - window_size
# Use sliding window view for speed, see
# https://numpy.org/devdocs/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html
def running_mean(x, window_size):
  return np.mean(np.lib.stride_tricks.sliding_window_view(x,window_size),1)

def running_mean_old(arr1, window_size):
    fluxes = np.array(arr1)
    mean_iterations = len(fluxes) - window_size + 1
    running_mean = []
    for i in range(0, mean_iterations):
        start = i 
        end = i + window_size
        running_mean.append(np.mean(fluxes[start:end])) 
    return(running_mean)

# Calculate running standard dev of arr1, using window size.
# Output size is arr1 size - window_size
# Use sliding window view for speed, see
# https://numpy.org/devdocs/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html
def running_standarddev(x, stwindow):
   return np.std(np.lib.stride_tricks.sliding_window_view(x,stwindow),1)

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


# JCG: This needs work.  Bad name: what does this function actually do?
# What's with the 500?  Should be a function argument or predefined parameter
# Are we actually using this?  Delete?
def smoothed_spectrum(running_median, arr1):
   normalized_flux = arr1[500:(len(running_median) + 500)]/running_median
   return normalized_flux


# JCG: Are we actually using this?  Delete?
def spike_searcher(normalized_flux):
    count = 0 #we set the count variable
    for i in range(len(normalized_flux)):
            if normalized_flux[i] >= 5:
                 count += 1
            else:
                if count >= 5 and count <= 500:
                    print(i - count, i)
                    count = 0

# Do we need separate functions for these?  Can't we just do one function
#
# spectrum_plot(wave,quantity,index1,index2) and call it with different arguments outside?

def original_spectrum_plot(wave, arr1, index1, index2):
    plt.plot(wave[index1:index2], arr1[index1:index2], '.-')

# Explain what "flat" means.  Are we using this?
def flat_spectrum_plot(wave, normalized_flux, index1, index2):  
    plt.plot(wave[index1:index2], normalized_flux[index1:index2], '.-', label='')

def median_spectrum_plot(wave, runing_median, index1, index2, label):
    plt.plot(wave[index1:index2],running_median[index1:index2], '.-', label='')


# JCG: Are we using this?
def seti_spike_searcher(arr1, min_count = 5, max_count = 500, flux_threshold = 5):
    window_size = 1000
    continuum = running_median(arr1, window_size)
    normalized_flux = arr1[500:(len(continuum) + 500)]/continuum
    count = 0 #we set the count variable
    for i in range(len(normalized_flux)):
            if normalized_flux[i] >= flux_threshold:
                 count += 1
            else:
                if count >= min_count and count <= max_count:
                    print(i - count, i)
                    return(i-count, i)
                    count = 0
#Put stricter upper limit to rule out broader

# JCG: If this extended comment block isn't being used, get rid of it

# def seti_spike_analyzer(arr1, min_count = 5, max_count = 500, threshold_multiplier = 4, stwindow = 100):
#     window_size = 1000
#     continuum = running_median(arr1, window_size)
#     normalized_flux = arr1[500:(len(continuum) + 500)]/continuum
#     count = 0 #we set the count variable
#     flux_threshold = (running_standarddev(arr1, stwindow)) * (threshold_multiplier)
#     for i in range(len(normalized_flux)):
#             if normalized_flux[i] >= flux_threshold[i]:
#                   count += 1
#             else:
#                 if count >= min_count and count <= max_count:
#                     print(i - count, i)
#                     return(i-count, i)
#                     count = 0

# def seti_spike_analyzer(arr1, min_count = 4, max_count = 8, threshold_multiplier = 4, stwindow = 101, window_size = 101):
#     continuum = running_median(arr1, window_size)
#     count = 0 #we set the count variable
#     import numpy as np
#     flux_threshold = np.array(running_standarddev(arr1, stwindow)) * (threshold_multiplier)
#     hits_start = []
#     hits_end = []
#     for i in range(50,len(continuum) - 50):
#             if arr1[i] >= continuum[i - 50] + flux_threshold[i - 50]:
#                   count += 1
#             else:
#                 if (count >= min_count) and (count <= max_count):
#                     print("Hit found.\n")
#                     print("arr1: ")
#                     print(arr1[i-count:i])
#                     print("\n threshhold: ")
#                     print(continuum[(i-50):(i-50+count)]+flux_threshold[(i-50):(i-50+count)])
#                     print("\n")
#                     hits_start.append(i-count)
#                     hits_end.append(i)
#                 count = 0
#     print(hits_start, hits_end)
#     return(hits_start, hits_end) 

# The main SETI search routine.
# 
# Input arguments:
#   arr1: spectral intensity
#   min_cont: minimum number of bright pixels in a row to count as a spike
#   max_count: maximum number of bright pixels in a row to count as a spike
#   threshold_multiplier: how many standard deviations above median must pixel be to count as a spike
#   cosmic_ray_threshold: unused
#   stwindow: window size for standard deviation (must equal window_size)
#   window_size: window size for median (must equal stwindow)
def seti_spike_analyzer(arr1, min_count = 4, max_count = 8, threshold_multiplier = 3, cosmic_ray_threshold = 1.5, stwindow = 101, window_size = 101):
    half_window_size = (window_size-1)/2
    continuum = running_median(arr1, window_size)
    count = 0 #reset bright pixel count variable
#    import numpy as np # JCG: Not needed
    flux_threshold = np.array(running_standarddev(arr1, stwindow)) * (threshold_multiplier)
#    cosmic_ray_threshold = np.array(running_standarddev(arr1, stwindow)) * (cosmic_ray_threshold) # JCG: Not used
    hits_start = []  # List of starting wavelength indices for spikes
    hits_end = []    # List of ending wavelength indices for spikes
    # List of known airglow lines, this needs to be clearer
    prohibited_wavelengths = list(range(179450, 179650)) + list(range(251750, 251950)) + list(range(210750, 210950)) + list(range(258150, 258350)) + list(range(141550, 141750)) + list(range(141750, 141950)) + list(range(211350, 211550)) # JCG: This is damn ugly
    # Loop over all wavelengths where "continuum" has been calculated.
    for i in range(50,len(continuum) - 50):
            if arr1[i] >= continuum[i - 50] + flux_threshold[i - 50]:  # If pixel is above threshold
                  count += 1                                           # increment count
            else:                                                      # if pixel falls below threshold
                if (count >= min_count) and (count <= max_count):      # if spike isn't too wide or narrow
                    # JCG: Get rid of this
                    # print("Hit found.\n")
                    # print("arr1: ")
                    # print(arr1[i-count:i])
                    # print("\n threshhold: ")
                    # print(continuum[(i-50):(i-50+count)]+flux_threshold[(i-50):(i-50+count)])
                    # print("\n")
                    if i not in prohibited_wavelengths:                # if it's not in our list of airglow lines
                        hits_start.append(i-count)                     # Add to the list of spikes found
                        hits_end.append(i)
                count = 0
    print(hits_start, hits_end)
    return hits_start, hits_end, count                                 # Return list of hits found, and number of hits

# JCG: Is this being used? Appears only in "decision_tree.py"
# This is a variant on seti_spike_analyzer that rules out spikes with sharp edges, calling them "cosmic rays".

def wormhunter(arr1, min_count = 4, max_count = 60, threshold_multiplier = 3.5, stwindow = 101, window_size = 101):
    continuum = running_median(arr1, window_size)
    count = 0 #we set the count variable
    import numpy as np
    flux_threshold = np.array(running_standarddev(arr1, stwindow)) * (threshold_multiplier)
    hits_start = []
    hits_end = []
    intermediate_counts = []
    prohibited_wavelengths = list(range(179450, 179650)) + list(range(251750, 251950)) + list(range(210750, 210950)) + list(range(258150, 258350)) + list(range(141550, 141750)) + list(range(141750, 141950)) + list(range(211350, 211550))
    for i in range(50,len(continuum) - 50):
            if arr1[i] >= continuum[i - 50] + flux_threshold[i - 50]:
                  count += 1
            else:
                if (count >= min_count) and (count <= max_count):
                    # print("Hit found.\n")
                    # print("arr1: ")
                    # print(arr1[i-count:i])
                    # print("\n threshhold: ")
                    # print(continuum[(i-50):(i-50+count)]+flux_threshold[(i-50):(i-50+count)])
                    # print("\n")
                    if i not in prohibited_wavelengths:
                        cosmic_ray_start = (i-count) - 5 #The algorithm is trained to search it's immediate 'neighborhood' of pixels, hence why we expand the
                        cosmic_ray_end = i + 5
                        peaky = arr1[cosmic_ray_start:cosmic_ray_end] - continuum[(cosmic_ray_start - 50):(cosmic_ray_end - 50)]
                        intermediate_count = 0
                        top_threshold = (np.amax(peaky) * (0.7)) 
                        bottom_threshold = (np.amax(peaky) * (0.2)) 
                        for j in range(0, len(peaky)):
                            if peaky[j] <= top_threshold  and peaky[j] >= bottom_threshold:
                                intermediate_count += 1 
                        if intermediate_count != 0:
                              hits_start.append(i-count)
                              hits_end.append(i)
                              intermediate_counts.append(intermediate_count)
                count = 0             
    print(hits_start, hits_end, intermediate_counts)
    return hits_start, hits_end, intermediate_counts

# JCG: Is this being used? Appears only in "offline_analysis.py".  Appears broken.
# This is a variant on seti_spike_analyzer and wormhunter that doesn't actually store hit locations.

def wormsearcher(arr1, wave, min_count = 4, max_count = 60, threshold_multiplier = 3, stwindow = 101, window_size = 101):
    continuum = running_median(arr1, window_size)
    count = 0 #we set the count variable
    import numpy as np
    flux_threshold = np.array(running_standarddev(arr1, stwindow)) * (threshold_multiplier)
    hits_start = []
    hits_end = []
    intermediate_count = 0
    prohibited_wavelengths = list(range(179500, 179610)) + list(range(251810, 251910)) + list(range(210810, 210910)) + list(range(258200, 258312)) + list(range(141600, 141712)) + list(range(141800, 141912)) + list(range(211400, 211512))  
    for i in range(50,len(continuum) - 50):
            if arr1[i] >= continuum[i - 50] + flux_threshold[i - 50]:
                  count += 1
            else:
                if (count >= min_count) and (count <= max_count):
                    # print("Hit found.\n")
                    # print("arr1: ")
                    # print(arr1[i-count:i])
                    # print("\n threshhold: ")
                    # print(continuum[(i-50):(i-50+count)]+flux_threshold[(i-50):(i-50+count)])
                    # print("\n")
                    if int(wave[i]) not in prohibited_wavelengths:
                        hits_start.append(i-count)
                        hits_end.append(i)
                        cosmic_ray_start = (i-count) - 5 #The algorithm is trained to search it's immediate 'neighborhood' of pixels, hence why we expand the
                        cosmic_ray_end = i + 5
                        peaky = arr1[cosmic_ray_start:cosmic_ray_end] - continuum[(cosmic_ray_start - 50):(cosmic_ray_end - 50)]
                        intermediate_count = 0
                        top_threshold = (np.amax(peaky) * (0.7)) 
                        bottom_threshold = (np.amax(peaky) * (0.25)) 
                        for j in range(0, len(peaky)):
                            if peaky[j] <= top_threshold  and peaky[j] >= bottom_threshold:
                                intermediate_count += 1 
                count = 0             
    print(hits_start, hits_end)
    return hits_start, hits_end, count, intermediate_count

# JCG: Plot spectral data with continuum and flux threshold lines.
# Could easily be combined with zoomin_spike_plotter.
# Not used in any other .py

def zoomout_spike_plotter(file, window_size = 101, stwindow = 101, threshold_multiplier = 5, spectral_start = 1000, spectral_end = 2000): #Where "spectral window" is 
    from matplotlib import pyplot as plt
    from astropy.io import fits
    fits_file = fits.open(file)
    spectral_data = fits_file[1].data
    wave = spectral_data[0][0]
    arr1 = spectral_data[0][1]
    arr2 = spectral_data[0][2]
    continuum = running_median(arr1,window_size) 
    zoomoutstart_index = (spectral_start - 1000)
    zoomoutend_index = (spectral_end + 1000)
    threshold = continuum + np.array(running_standarddev(arr1, stwindow)) * threshold_multiplier
    plt.plot(wave[zoomoutstart_index:zoomoutend_index], arr1[zoomoutstart_index:zoomoutend_index],'.-', wave[zoomoutstart_index:zoomoutend_index], continuum[(zoomoutstart_index - 50):(zoomoutend_index - 50)], wave[zoomoutstart_index:zoomoutend_index], threshold[(zoomoutstart_index - 50):(zoomoutend_index - 50)])
    plt.savefig(str(file[48:]) + "zoom_out" + ".png")
    zoominstart_index = (spectral_start - 100)
    zoominend_index = (spectral_end + 100)
    plt.plot(wave[zoominstart_index:zoominend_index], arr1[zoominstart_index:zoominend_index],'.-', wave[zoominstart_index:zoominend_index], continuum[(zoominstart_index - 50):(zoominend_index - 50)], wave[zoominstart_index:zoominend_index], threshold[(zoominstart_index - 50):(zoominend_index - 50)])
    plt.savefig(str(file[48:]) + "zoom_in" + ".png")

# JCG: Plot spectral data with continuum and flux threshold lines.
# Could easily be combined with zoomin_spike_plotter.
# Not used in any other .py

def zoomin_spike_plotter(file, window_size = 101, stwindow = 101, threshold_multiplier = 5, spectral_start = 1000, spectral_end = 2000, cosmic_ray_multiplier = 0.5): #Where "spectral window" is 
    from matplotlib import pyplot as plt
    from astropy.io import fits
    fits_file = fits.open(file)
    spectral_data = fits_file[1].data
    wave = spectral_data[0][0]
    arr1 = spectral_data[0][1]
    arr2 = spectral_data[0][2]
    continuum = running_median(arr1,window_size) 
    threshold = continuum + np.array(running_standarddev(arr1, stwindow)) * threshold_multiplier
    zoominstart_index = (spectral_start - 100)
    zoominend_index = (spectral_end + 100)
    plt.plot(wave[zoominstart_index:zoominend_index], arr1[zoominstart_index:zoominend_index],'.-', wave[zoominstart_index:zoominend_index], continuum[(zoominstart_index - 50):(zoominend_index - 50)], wave[zoominstart_index:zoominend_index], threshold[(zoominstart_index - 50):(zoominend_index - 50)])
    plt.savefig(str(file[48:]) + "zoom_in" + ".png")

# Calculate relative velocity of doppler shifted wavelengths.
# Not used in any .py
def doppler_detective(wavelength1, wavelength2):
    if wavelength2 > wavelength1:
        doppler_velocity = ((wavelength2-wavelength1)/(wavelength1))*(2.99 * 10 ** 18) #Angstroms per second.
        radial_velocity = doppler_velocity * (10 ** -10)
        return(radial_velocity)
        print(str(radial_velocity) + "m/s")

# Calculate themperature of thermal doppler broadened hydrogen line.
# Used by gaussian_curve_fitting_algorithm.py
# Remove or make general-purpose?
def doppler_broadening_calculator(fwhm, rest_wavelength):
    import numpy as np
    c = 2.99E8 #speed of light
    k = 1.38E-23 #Boltzmann's constant
    m = 1.67E-27 #mass of a hydrogen atom
    T = (((c**2) * m)/(k)) * ((fwhm)**2)/(8*np.log(2)*(rest_wavelength ** 2)) 
    return T
    print(str(T) + "K")
