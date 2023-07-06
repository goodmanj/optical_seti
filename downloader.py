# Download one spectrum from each of the targets listed in OSETI_survey1.txt, store in cache.
# Should be integrated in with big_search.py

from astroquery.eso import Eso
from astropy.io import fits
from optical_seti_functions import seti_spike_analyzer
# import csv
eso = Eso()
eso.login("Spaceboy42")
target_list = [x.split('\t')[0] for x in open("C:\\Users\\HAL 9000\\Downloads\\OSETI_survey1.txt").readlines()]
spectral_types = [x.split('\t')[3] for x in open("C:\\Users\\HAL 9000\\Downloads\\OSETI_survey1.txt").readlines()] 
temperatures = [x.split('\t')[4] for x in open("C:\\Users\\HAL 9000\\Downloads\\OSETI_survey1.txt").readlines()] 
distances = [x.split('\t')[8] for x in open("C:\\Users\\HAL 9000\\Downloads\\OSETI_survey1.txt").readlines()] 
output = open("multistarwidefield.txt", "a")
output.write("STAR,SPECTRAL TYPE,OBSERVATION FILE,HARPS OBJECT,TEMPERATURE,DISTANCES\n") #add wavelength variable.
for (star, spectral_type, temperature, distance) in zip(target_list[1:(len(target_list))], spectral_types[1:(len(target_list))], temperatures[1:(len(target_list))], distances[1:(len(target_list))]):
    print(star)
    # eso.login("Spaceboy42")
    Eso.ROW_LIMIT = -1
    tbl = eso.query_surveys('HARPS', target= star,box=0.1)
    star_objects = tbl['Object'][:]
    data_files = eso.retrieve_data(tbl['ARCFILE'][1:2]) 
    for (file, star_object) in zip(data_files, star_objects):
        output.write("{},{},{},{},{},{}\n".format(star,spectral_type,file,star_object,temperature, distance))
