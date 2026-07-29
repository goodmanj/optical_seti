from astropy.io import fits
from harpscompare import doppler
import numpy as np

# ESO file access stuff
from astroquery.eso import Eso
eso = Eso()
from pathlib import Path
eso_cache_folder = Path(eso.cache_location)
if not eso.authenticated():
    eso.login(username="goodmanj", store_password=True)
def cached_filename(file): 
    file_no_colon = str(file).replace(":","_") 
    return eso_cache_folder/(file_no_colon)

def download_if_needed(file):
    fits_specfile_name = cached_filename(file)   # underscore version, used for exists() check
    print(fits_specfile_name)
    if not fits_specfile_name.exists():
        print(str(fits_specfile_name) + " to be downloaded")
        result = eso.retrieve_data(file)
        # retrieve_data returns the actual saved path (with colons) — use that instead
        actual_path = Path(result[0]) if isinstance(result, list) else Path(result)
        return actual_path
    else:
        print(str(fits_specfile_name) + " exists")
        return fits_specfile_name

#infile = "results-tables/thebigsearch7,5Threshold3rdRun.txt"
infile = "results-tables/repeater_analysispart1.txt"
stars = [x.split(',')[0] for x in open(infile).readlines()]
spectral_types = [x.split(',')[1] for x in open(infile).readlines()]
specfiles = [x.split(',')[2] for x in open(infile).readlines()]
hits_start = [x.split(',')[3] for x in open(infile).readlines()]
hits_end = [x.split(',')[4] for x in open(infile).readlines()]
waves1 = [x.split(',')[5] for x in open(infile).readlines()]
waves2 = [x.split(',')[6] for x in open(infile).readlines()]
#distances = [x.split(',')[7] for x in open(infile).readlines()]
orig_wave = [x.split(',')[7] for x in open(infile).readlines()]

filtered  = open("results-tables/repeater-filtered_hits_nohk.txt", "w")
handk  = open("results-tables/repeater-handklines.txt", "w")
#filtered  = open("results-tables/core-filtered_hits_nohk.txt", "w")
#handk  = open("results-tables/core-handklines.txt", "w")
#for star,sptypes,d,start,end,spec,lamb,lamb2 in zip(stars,spectral_types,distances,hits_start,hits_end,specfiles,waves1,waves2):
for star,sptypes,d,start,end,spec,lamb,lamb2 in zip(stars,spectral_types,orig_wave,hits_start,hits_end,specfiles,waves1,waves2):
    central_wavelength = ((float(lamb) + float(lamb2)) / 2)
    spec_fname = Path(spec).name
    spec_actual_fname = download_if_needed(spec_fname)
    fitsfile = fits.open(spec_actual_fname)
    v = fitsfile[0].header["HIERARCH ESO TEL TARG RADVEL"]
    if abs(v) > 0 and abs(v) < 99999.0:
        dopplershifted = doppler(central_wavelength,v)
        if int((dopplershifted)) == 3933 or int(dopplershifted) == 3968:
            handk.write("{},{},{},{},{},{},{},{},{}\n".format(star,sptypes,d,start,end,spec,lamb,lamb2))
            handk.flush()
    if abs(v) == 0 or abs(v) == 99999.0 or int(dopplershifted) != 3933 or int(dopplershifted) != 3968:
        filtered.write("{},{},{},{},{},{},{},{}\n".format(star,sptypes,d,start,end,spec,lamb,lamb2))
        filtered.flush()
handk.close()
filtered.close()
            