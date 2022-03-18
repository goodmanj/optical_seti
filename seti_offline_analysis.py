from astropy.io import fits
from optical_seti_functions import wormsearcher
# import csv
output = open("singleobservationallstarsearch.txt", "a")
output.write("STAR,SPECTRAL TYPE,START INDEX,END INDEX,FILE,START WAVELENGTH,END WAVELENGTH,HARPS OBJECT,TEMPERATURE") #add wavelength variable.
target_list = [x.split(',')[0] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\multistarwidefield.txt").readlines()]
data_files = [x.split(',')[2] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\multistarwidefield.txt").readlines()] 
harps_objects = [x.split(',')[3] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\multistarwidefield.txt").readlines()]
spectral_types = [x.split(',')[1] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\multistarwidefield.txt").readlines()]
temperatures = [x.split(',')[4] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\multistarwidefield.txt").readlines()]
distances = [x.split(',')[5] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\multistarwidefield.txt").readlines()]
for (star, harps_object, spectral_type, temperature, file, distance) in zip(target_list[1:], harps_objects[1:], spectral_types[1:], temperatures[1:], data_files[1:], distances[1:]): 
    print(str(file))
    fits_file = fits.open(file)
    spectral_data = fits_file[1].data
    wave = spectral_data[0][0]
    arr1 = spectral_data[0][1]
    arr2 = spectral_data[0][2]
    hits_start, hits_end, count, intermediate_count = wormsearcher(arr1, min_count = 4, max_count = 60, threshold_multiplier = 3, stwindow = 101, window_size = 101)
    wavelength_start = wave[hits_start]
    wavelength_end = wave[hits_end]
    for (start, end) in zip(hits_start, hits_end):
            wavelength_start = wave[start]
            wavelength_end = wave[end]
            if len(hits_start) != 0:
                output.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(star, spectral_type, start, end, file, wavelength_start, wavelength_end, harps_object, temperature, distance, intermediate_count))
                 