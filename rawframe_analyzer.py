from astropy.io import fits
import numpy
from matplotlib import pyplot as plt
raw_file = "C:/Users/HAL 9000/.astropy/cache/astroquery/Eso/HARPS.2008-10-06T08_58_13.415.fits"
rawfits = fits.open(raw_file)
rawfits.info()
firstimage = rawfits[1]
secondimage = rawfits[2]
firstimage = rawfits[1].data
secondimage = rawfits[2].data
numpy.max(firstimage)
log_firstimage = numpy.log(firstimage)
log_secondimage = numpy.log(secondimage)
bottom_wavelength = [x.split('\t')[6] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\harps_spectralpositioning.txt").readlines()]
top_wavelength = [x.split('\t')[5] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\harps_spectralpositioning.txt").readlines()]
x_spectral_locations = [x.split('\t')[2] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\harps_spectralpositioning.txt").readlines()]
hits_start = 4850
hits_start = int(hits_start * 0.1)
for (lambda1, lambda2, spectral_order) in zip(top_wavelength, bottom_wavelength, x_spectral_locations):
    lambda1_int = int(float(lambda1))
    lambda2_int = int(float(lambda2))
    spectral_order_int = int(spectral_order)
    if hits_start >= 536.97 and hits_start in range(lambda1_int, lambda2_int):                            
        x1 = int(max((spectral_order_int - 100), 0))
        x2 = int(min((spectral_order_int + 100), 2199))
        y2 = int(abs((hits_start - lambda1_int)/(lambda2_int - lambda1_int) * 2200)) + 100
        y1 = int(abs((hits_start - lambda1_int)/(lambda2_int - lambda1_int) * 2200)) - 100
        ccd1_rawframe = plt.imshow(log_secondimage[x1:x2,y1:y2])
        ccd1_rawframe.savefig("rawframe1.svg")
        print(x1)
        print(x2)
        print(y1)
        print(y2)
        print(spectral_order_int)
    if hits_start <  536.97 and hits_start in range(lambda1_int, lambda2_int):
        x1 = int(max((spectral_order_int - 100), 0))
        x2 = int(min((spectral_order_int + 100), 2199))
        y1 = int(abs((hits_start - lambda1_int)/(lambda2_int - lambda1_int)) * 2200) + 100
        y2 = int(abs((hits_start - lambda1_int)/(lambda2_int - lambda1_int)) * 2200) - 100
        ccd2_rawframe = plt.imshow(log_firstimage[:,1300:1600])
        plt.savefig("rawframe2.svg")
        print(x1)
        print(x2)
        print(y1)
        print(y2)
        print(spectral_order_int)
