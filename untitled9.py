from astropy.io import fits
from optical_seti_functions import wormhunter, zoomin_spike_plotter
file = ("C:\\Users\\HAL 9000\\.astropy\\cache\\astroquery\\Eso\\ADP.2014-09-26T16_51_30.057.fits")
fits_file = fits.open(file)
spectral_data = fits_file[1].data
wave = spectral_data[0][0]
arr1 = spectral_data[0][1]
arr2 = spectral_data[0][2]
hits_start, hits_end, count  = wormhunter(arr1, min_count = 4, max_count = 60, threshold_multiplier = 3.5, stwindow = 101, window_size = 101)
