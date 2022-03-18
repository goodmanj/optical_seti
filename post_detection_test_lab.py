from astroquery.eso import Eso
from astropy.io import fits
from optical_seti_functions import seti_spike_analyzer
from astroquery.simbad import Simbad
# # # import csv
Eso.ROW_LIMIT = -1
# # eso.login("Spaceboy42")
# # target_list = ["TOI 700"]
# # spectral_types = ["G"]
# target_list = [x.split('\t')[0] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\OSETI_targets.txt").readlines()]
# spectral_types = [x.split('\t')[3] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\OSETI_targets.txt").readlines()] #Another 
# # output = open("TESST1.txt", "a")
# # output.write("STAR / SPECTRAL TYPE / HIT START / HIT END / START WAVELENGTH / END WAVELENGTH / PIXEL COUNT / FLUX / OBSERVATION FILE") #add wavelength variable.
# for (star, spectral_type) in zip(target_list[:4], spectral_types):
#     print(star)
#     tbl = eso.query_surveys('HARPS', cache=False, target= star)
#     # data_files = eso.retrieve_data(tbl['ARCFILE'][:])
#     objects = tbl['Object'][:]
#     print(objects)
tbl = Eso.query_surveys('HARPS',target="BD+053829",box=1)
tbl.pprint_all()
objects = tbl['Object'][:]
print(objects)
tbl.pprint_all()
print(len(tbl))
result_table = Simbad.query_objectids("BD+053829")
result_list = result_table["ID"][:]
for star in objects:
    if star in result_table:
        print(star)
# print(objects)
    # star_IDs = [i for i in range(len(objects)) if objects[i] not in result_list] 
        