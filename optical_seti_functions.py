import numpy as np
def running_median(arr1, window_size):
    fluxes = np.array(arr1)
    median_iterations = len(arr1) - window_size + 1
    running_median = []
    for i in range(0, median_iterations):
        start = i 
        end = i + window_size
        running_median.append(np.median(fluxes[start:end])) 
    return(running_median)

def running_mean(arr1, window_size):
    fluxes = np.array(arr1)
    mean_iterations = len(fluxes) - window_size + 1
    running_mean = []
    for i in range(0, mean_iterations):
        start = i 
        end = i + window_size
        running_mean.append(np.mean(fluxes[start:end])) 
    return(running_mean)

def smoothed_spectrum(running_median, arr1):
   normalized_flux = arr1[500:(len(running_median) + 500)]/running_median
   return normalized_flux



def spike_searcher(normalized_flux):
    count = 0 #we set the count variable
    for i in range(len(normalized_flux)):
            if normalized_flux[i] >= 5:
                 count += 1
            else:
                if count >= 5 and count <= 500:
                    print(i - count, i)
                    count = 0

def original_spectrum_plot(wave, arr1, index1, index2):
    from matplotlib import pyplot as plt
    plt.plot(wave[index1:index2], arr1[index1:index2], '.-')

def flat_spectrum_plot(wave, normalized_flux, index1, index2):  
    from matplotlib import pyplot as plt
    plt.plot(wave[index1:index2], normalized_flux[index1:index2], '.-', label='')

def median_spectrum_plot(wave, runing_median, index1, index2, label):
    from matplotlib import pyplot as plt
    plt.plot(wave[index1:index2],running_median[index1:index2], '.-', label='')

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

def running_standarddev(arr1, stwindow):
    import numpy as np
    fluxes = np.array(arr1)
    standard_iterations = len(arr1) - stwindow + 1
    running_stdeviation = []
    for i in range(0, standard_iterations):
        start = i 
        end = i + stwindow
        running_stdeviation.append(np.std(fluxes[start:end])) 
    return(running_stdeviation)


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

def seti_spike_analyzer(arr1, min_count = 4, max_count = 8, threshold_multiplier = 4, stwindow = 101, window_size = 101):
    continuum = running_median(arr1, window_size)
    count = 0 #we set the count variable
    import numpy as np
    flux_threshold = np.array(running_standarddev(arr1, stwindow)) * (threshold_multiplier)
    hits_start = []
    hits_end = []
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
                    hits_start.append(i-count)
                    hits_end.append(i)
                count = 0            
    print(hits_start, hits_end)
    return hits_start, hits_end, count

def seti_spike_plotter(arr1, wave, window_size = 101, stwindow = 101, threshold_multiplier = 5, spectral_start = 1000, spectral_end = 2000): #Where "spectral window" is 
    from matplotlib import pyplot as plt
    continuum = running_median(arr1,window_size) 
    threshold = continuum + np.array(running_standarddev(arr1, stwindow)) * threshold_multiplier
    plt.plot(wave[spectral_start:spectral_end], arr1[spectral_start:spectral_end],'.-', wave[spectral_start:spectral_end], continuum[(spectral_start - 50):(spectral_end - 50)], wave[spectral_start:spectral_end], threshold[(spectral_start - 50):(spectral_end - 50)])

# def specific_spectral_type_search
    
#def seti_spike_plotter():
    # plt.plot(range(103300,103400), arr1[103300:103400],'.-',range(103300,103400), continuum[103250:103350], range(103300,103400), threshold[103250:103350])
