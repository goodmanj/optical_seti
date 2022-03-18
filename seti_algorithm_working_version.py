from astroquery.eso import Eso
from astropy.io import fits
from optical_seti_functions import seti_spike_analyzer
# import csv
eso = Eso()
Eso.login("Spaceboy42")
target_list = [x.split('\t')[0] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\OSETI_targets.txt").readlines()]
spectral_types = [x.split('\t')[3] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\OSETI_targets.txt").readlines()] #Another 
output = open("setitrialoutput2.txt", "a")
output.write("STAR, SPECTRAL TYPE, SPECTRAL INDICES, OBSERVATION FILE") #add wavelength variable.
for (star, spectral_type) in zip(target_list[3], spectral_types[3]):
    print(star)
    tbl = eso.query_surveys('HARPS', target= star)
    data_files = Eso.retrieve_data(tbl['ARCFILE'][:])
    for file in data_files:
        print(str(file))
        fits_file = fits.open(file)
        spectral_data = fits_file[1].data
        wave = spectral_data[0][0]
        arr1 = spectral_data[0][1]
        arr2 = spectral_data[0][2]
        hits_start, hits_end, count  = seti_spike_analyzer(arr1, min_count = 4, max_count = 90, threshold_multiplier = 4, stwindow = 101, window_size = 101)
        wavelength = wave[hits_start]
        if len(hits_start) != 0:
            output.write("{} / {} / {} / {} / {} / {}\n".format(star, spectral_type, hits_start, hits_end, file, wavelength))
    #file.close()
