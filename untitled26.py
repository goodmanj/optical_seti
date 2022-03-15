from astropy.io import fits
from optical_seti_functions import seti_spike_plotter
file = ("C:\\Users\\HAL 9000\\.astropy\\cache\\astroquery\\Eso\\ADP.2014-09-26T16_52_09.870.fits")
seti_spike_plotter(file, window_size = 101, stwindow = 101, threshold_multiplier = 3.5, spectral_start = 251800, spectral_end = 252000)