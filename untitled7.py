from optical_seti_functions import zoomin_spike_plotter
data_files = [x.split(',')[0] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\seti_threethresholdsampling.txt").readlines()] 
spectral_starts = [x.split(',')[0] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\seti_3.5thresholdsampling.txt").readlines()]
spectral_ends = [x.split(',')[0] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\seti_3.5thresholdsampling.txt").readlines()]
for (file, spectral_start, spectral_end) in zip(data_files[1:], spectral_starts[1:], spectral_ends[1:]):
    zoomin_spike_plotter(file, window_size = 101, stwindow = 101, threshold_multiplier = 3.5, spectral_start = spectral_start, spectral_end = spectral_end)
    