from astroquery.eso import Eso
from astropy.io import fits
from optical_seti_functions import seti_spike_analyzer
import csv
target_list = ["BD-07436B"]
spectral_types = ["M"]
# target_list = [x.split('\t')[0] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\OSETI_targets.txt").readlines()]
# spectral_types = [x.split('\t')[3] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\OSETI_targets.txt").readlines()] #Another 
header = ["STAR","SPECTRAL TYPE","HIT START","HIT END","START WAVELENGTH","END WAVELENGTH","OBSERVATION FILE"] #add wavelength variable.
with open('TOI700Dfinaltest.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
for (star, spectral_type) in zip(target_list, spectral_types):
    print(star)
    Eso.ROW_LIMIT = -1
    tbl = Eso.query_surveys('HARPS', target= star, box=1)
    data_files = Eso.retrieve_data(tbl['ARCFILE'][:])
    star_objects = tbl['Object'][:]
    for (file, star_object) in zip(data_files, star_objects):
        print(str(file))
        fits_file = fits.open(file)
        spectral_data = fits_file[1].data
        wave = spectral_data[0][0]
        arr1 = spectral_data[0][1]
        arr2 = spectral_data[0][2]
        hits_start, hits_end, count  = seti_spike_analyzer(arr1, min_count = 4, max_count = 90, threshold_multiplier = 4, stwindow = 101, window_size = 101)
        start_wavelength = wave[hits_start]
        end_wavelength = wave[hits_end]
        hit_details = str(star,spectral_type,hits_start,hits_end,start_wavelength,end_wavelength,file,star_object)
        if len(hits_start) != 0:
            writer.writerows(hit_details)

