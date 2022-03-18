from astropy.io import fits
from optical_seti_functions import wormhunter, zoomin_spike_plotter
file = ("C:\\Users\\HAL 9000\\.astropy\\cache\\astroquery\\Eso\\ADP.2014-09-24T09_42_14.633.fits")
fits_file = fits.open(file)
spectral_data = fits_file[1].data
wave = spectral_data[0][0]
arr1 = spectral_data[0][1]
arr2 = spectral_data[0][2]

zoomin_spike_plotter(file, window_size = 101, stwindow = 101, threshold_multiplier = 3.5, spectral_start = 308249, spectral_end = 308253)