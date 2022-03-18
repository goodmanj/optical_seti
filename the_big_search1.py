from astroquery.eso import Eso
from astropy.io import fits
from optical_seti_functions import seti_spike_analyzer
# import csv
eso = Eso()
eso.login("Spaceboy42")
target_list = [x.split('\t')[0] for x in open("C:\\Users\\HAL 9000\\Downloads\\OSETI_survey1.txt").readlines()]
spectral_types = [x.split('\t')[3] for x in open("C:\\Users\\HAL 9000\\Downloads\\OSETI_survey1.txt").readlines()] 
temperatures = [x.split('\t')[4] for x in open("C:\\Users\\HAL 9000\\Downloads\\OSETI_survey1.txt").readlines()] 
#Another 
output = open("onelineperhit.txt", "a")
output.write("STAR,SPECTRAL TYPE,START INDEX,END INDEX,OBSERVATION FILE,START WAVELENGTH,END WAVELENGTH,HARPS OBJECT,TEMPERATURE") #add wavelength variable.
for (star, spectral_type, temperature) in zip(target_list[2:3], spectral_types[2:3], temperatures[2:3]):
    print(star)
    # eso.login("Spaceboy42")
    Eso.ROW_LIMIT = -1
    tbl = eso.query_surveys('HARPS', target= star,box=0.1)
    star_objects = tbl['Object'][:]
    data_files = eso.retrieve_data(tbl['ARCFILE'][1:2])
    for (file, star_object) in zip(data_files, star_objects):
        print(str(file))
        fits_file = fits.open(file)
        spectral_data = fits_file[1].data
        wave = spectral_data[0][0]
        arr1 = spectral_data[0][1]
        arr2 = spectral_data[0][2]
        hits_start, hits_end, count  = seti_spike_analyzer(arr1, min_count = 4, max_count = 60, threshold_multiplier = 3.5, cosmic_ray_threshold = 1.5, stwindow = 101, window_size = 101)
        for (start, end) in zip(hits_start, hits_end):
            wavelength_start = wave[start]
            wavelength_end = wave[end]
            if len(hits_start) != 0:
                output.write("{},{},{},{},{},{},{},{},{}\n".format(star, spectral_type, start, end, file, wavelength_start, wavelength_end, star_object, temperature))
    #file.close()
