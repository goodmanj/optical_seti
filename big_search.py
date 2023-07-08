eso_login = "Spaceboy42"
star_list = "OSETI_targets.txt"
results = "onelineperhit.txt"

from astroquery.eso import Eso
from astropy.io import fits
import astropy.config
import optical_seti_functions
from pathlib import Path
eso_cache_path = Path(astropy.config.get_cache_dir()) / "astroquery" / "Eso"

def do_search(withlogin=eso_login,withstarlist=star_list,withresults=results):
    eso = Eso()
    eso.login(withlogin)

    target_list = [x.split('\t')[0] for x in open(withstarlist).readlines()]
    spectral_types = [x.split('\t')[3] for x in open(withstarlist).readlines()] 
    temperatures = [x.split('\t')[4] for x in open(withstarlist).readlines()] 

    output = open(withresults, "w")
    output.write("STAR,SPECTRAL TYPE,START INDEX,END INDEX,OBSERVATION FILE,START WAVELENGTH,END WAVELENGTH,HARPS OBJECT,TEMPERATURE\n") #add wavelength variable.
    for (star, spectral_type, temperature) in zip(target_list[1:], spectral_types[1:], temperatures[1:]):
        print(star)
        Eso.ROW_LIMIT = -1
        tbl = eso.query_surveys('HARPS', target= star,box=0.1)
        star_objects = tbl['Object'][:]
        arcfile = tbl['ARCFILE'][1:2]
        cached_file = eso_cache_path /  (arcfile[0].replace(":","_")+".fits")
        if (cached_file.exists()):
            print("Big_search using cached file " + str(cached_file))
            data_files = [cached_file]
        else:
            print("Big_search downloading " + str(arcfile[0]))
            data_files = eso.retrieve_data(arcfile) 
        for (file, star_object) in zip(data_files, star_objects):
            print(str(file))
            fits_file = fits.open(file)
            spectral_data = fits_file[1].data
            wave = spectral_data[0][0]
            arr1 = spectral_data[0][1]
            arr2 = spectral_data[0][2]
            hits_start, hits_end, count  = optical_seti_functions.seti_spike_analyzer(arr1, min_count = 4, max_count = 60, threshold_multiplier = 3.5, window_size = 101)
            for (start, end) in zip(hits_start, hits_end):
                wavelength_start = wave[start]
                wavelength_end = wave[end]
                if len(hits_start) != 0:
                    output.write("{},{},{},{},{},{},{},{},{}\n".format(star, spectral_type, start, end, file, wavelength_start, wavelength_end, star_object, temperature))
        #file.close()
