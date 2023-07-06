# Fit a Gaussian curve to a spectral line found at hits_start to hits_end, plot both, print the width of the Gaussian fit.
# Needs cleanup and generalization

import numpy as np
import matplotlib.pyplot as plt

from astropy.modeling import models
from astropy import units as u

from specutils.spectra import Spectrum1D
from specutils.fitting import fit_lines
from astropy.io import fits
from optical_seti_functions import doppler_broadening_calculator
fits_file = fits.open("C://Users//HAL 9000//.astropy//cache/astroquery//Eso//ADP.2017-07-16T01_01_15.941.fits") #known cosmic ray
# fits_file = fits.open("C:\\Users\\HAL 9000\\.astropy\\cache\\astroquery\\Eso\\ADP.2019-05-11T01_08_36.042.fits") #known stellar emission lines
# fits_file = fits.open("C:\\Users\\HAL 9000\\.astropy\\cache\\astroquery\\Eso\\ADP.2014-09-16T11_04_49.937.fits") #Our signal candidate
spectral_data = fits_file[1].data
wave = spectral_data[0][0]
arr1 = spectral_data[0][1]
arr2 = spectral_data[0][2]
hits_start = 179487  
hits_end = 179493
windowpoint1 = hits_start - 100
windowpoint2 = hits_end + 100
subtracted = arr1 - np.mean(arr1[windowpoint1:windowpoint2])
peak_guess = np.max(subtracted[hits_start:hits_end]) #makes a highly "educated guess" for the fitted curve's peak by taking the actual maximum from the subtracted continuum
mean_guess = np.mean(wave[hits_start:hits_end])
st_deviation_guess_wide = (wave[hits_end] - wave[hits_start]) * 10
st_deviation_guess_narrow = (wave[hits_end] - wave[hits_start]) * 2
spectrum = Spectrum1D(flux=subtracted[windowpoint1:windowpoint2]*u.dimensionless_unscaled, spectral_axis=wave[windowpoint1:windowpoint2]*u.AA)
g_init = models.Gaussian1D(amplitude=peak_guess*u.dimensionless_unscaled, mean=mean_guess*u.AA, stddev=st_deviation_guess_wide*u.AA)
g_fit = fit_lines(spectrum, g_init, window=(wave[windowpoint1]*u.AA, wave[windowpoint2]*u.AA))
standard_deviation = g_fit.stddev.value
if standard_deviation == 1.1754943508222875e-38:
    alternate_guess = models.Gaussian1D(amplitude=peak_guess*u.dimensionless_unscaled, mean=mean_guess*u.AA, stddev=st_deviation_guess_narrow*u.AA)
    alternate_fit = fit_lines(spectrum, alternate_guess, window=(wave[windowpoint1]*u.AA, wave[windowpoint2]*u.AA))
    standard_deviation_2 = alternate_fit.stddev.value
    fwhm = standard_deviation_2 * 2.35
    plt.plot(spectrum.spectral_axis, spectrum.flux) 
    y_fit = alternate_fit(wave[windowpoint1:windowpoint2]*u.AA)
    plt.plot(wave[windowpoint1:windowpoint2], y_fit)
    rest_wavelength = mean_guess
    print(doppler_broadening_calculator(fwhm, rest_wavelength))
else:
    fwhm = standard_deviation * 2.35
    y_fit = g_fit(wave[windowpoint1:windowpoint2]*u.AA)
    plt.plot(spectrum.spectral_axis, spectrum.flux) 
    plt.plot(wave[windowpoint1:windowpoint2], y_fit)
    rest_wavelength = mean_guess
    print(doppler_broadening_calculator(fwhm, rest_wavelength))
print(fwhm) 
#Cosmic ray hits_start: 4082, green auroral emission line: 179487, 179487
#GJ551 HITS_STARTS: 13812, 39670 (something's odd), 43403, 45101, 59377, 64514, 67948, 76729, 80165
