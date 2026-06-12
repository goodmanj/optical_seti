from optical_seti_functions_github_edition import read_harps_file, seti_spike_analyzer
from astroquery.eso import Eso
import random
import scipy.constants
from matplotlib import pyplot as plt
import numpy as np
from Gaussian_Injector import add_gaussian_to_array, plot_gaussian_comparison
from astropy.io import fits
from optical_seti_functions import seti_spike_analyzer
import html5lib
file = "C:\\Users\\bnfie\\.astropy\\cache\\astroquery\\Eso\\ADP.2017-09-22T01_01_40.589.fits"
wave, arr1 = read_harps_file(file)
data = arr1
e = 0.057 #instrumental efficiency
LP = 100000 #Laser Transmitter Power (Watts)
h = 6.626 * 10 ** -34 #plancks constant 
c = 2.99 * 10 ** 8 #speed of light
T = 900 #exposure_time
D_t = 10 #assumed diameter of transmitter
D_R = 3.6 #Diameter of recieving telescope.
parsecs = 15
D = parsecs * (10 * 10 ** 16)
#center = random.choice(arr1)
lamb = 5000 * 10 ** -10
wavelength = 5800.00
array_length = len(arr1)
center = np.where(wave == wavelength)[0]
area = (e * LP * (D_t ** 2) * (D_R ** 2) * T) // ((1.22 ** 2) * lamb * h * c * (D ** 2))
modded_spectrum = add_gaussian_to_array(data, fwhm = 10, amplitude=None, center=center, array_length=array_length, axis=-1, area=area)
seti_spike_analyzer(modded_spectrum, min_count = 4, max_count = 60, threshold_multiplier = 3.5, window_size = 101)
plt.plot(wave, modded_spectrum)
plt.show()

