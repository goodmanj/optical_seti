from astropy.io import fits #Import fits handler from astropy.io
fits.info('ADP.2014-09-16T11 03 32.357.fits') 
file_name = 'ADP.2014-09-16T11 03 32.357.fits' #name the path so you don't have to open again.
fits_file = fits.open(file_name)
spectral_data = fits_file[1].data #Rename it to a variable, then use that to index it so you get the first file out of the condensed FITS.
wave = spectral_data[0][0]
arr1 = spectral_data[0][1] #Pulling out the arrays from within the master array...nested arrays!
arr2 = spectral_data[0][2]
from optical_seti_functions import running_median
window_size = 1000
running_median = running_median(arr1,window_size)
from matplotlib import pyplot as plt
plt.plot(wave[0:20000],running_median[0:20000],'.-')  
plt.show() #Use matplotlib to show it.
#Questions:
    #1.I indexed both the wavelengths and the running median flux to the length of the median flux array, even though it's around 1000 characters shorter. Is this a problem?
    #2. How do we make a graph that more clearly shows the "pixels above background"?
    #3. How did Tellis and Marcy decide on which median window to use? why every thousand angstroms? Why not every 10,000 angstroms, or every 800, etc.?