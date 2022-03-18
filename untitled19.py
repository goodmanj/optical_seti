# from astroquery.eso import Eso
# from astropy.io import fits
# from optical_seti_functions import seti_spike_analyzer
# # import csv
# eso = Eso()
# eso.login("Spaceboy42")
# target_list = ["TOI 700"]
# spectral_types = ["G"]
# # target_list = [x.split('\t')[0] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\OSETI_targets.txt").readlines()]
# # spectral_types = [x.split('\t')[3] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\OSETI_targets.txt").readlines()] #Another 
# # output = open("TESST1.txt", "a")
# # output.write("STAR / SPECTRAL TYPE / HIT START / HIT END / START WAVELENGTH / END WAVELENGTH / PIXEL COUNT / FLUX / OBSERVATION FILE") #add wavelength variable.
# for (star, spectral_type) in zip(target_list, spectral_types):
#     print(star)
#     tbl = eso.query_surveys('HARPS', cache=False, target= star)
#     data_files = eso.retrieve_data(tbl['ARCFILE'][:])
#     objects = tbl['Object'][:]
#     print(objects)

#SIMBAD QUERRY:
from astroquery.simbad import Simbad
result_table = Simbad.query_objectids("Polaris")
result_list = result_table["ID"][:]
random_stars = ["GJ699","PROXIMA CENTAURI", "AAVSO 0122+88", "Polaris"]
star_ID = [i for i in range(len(random_stars)) if random_stars[i] not in result_list] 
print(star_ID)
        