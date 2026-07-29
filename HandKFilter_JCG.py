# HandKFilter_JCG.py: Parse through a list of optical seti candidates, and use Benji's code from HandKFilter.property
# to remove hits corresponding to the wavelengths of H and K spectral lines.
# This version does auto-downloading of files and astropy tables to streamline the code.

# ESO archive login info (replace with your userid)
eso_login = "goodmanj"

# On Windows, need to replace all colons in filenames with underscores.  Set to True for Windows, False for Mac/Linux.
replace_underscores=True

# Set up ESO archive queries, identify cache directory
from astroquery.eso import Eso
eso = Eso()
eso.login(username=eso_login)
from pathlib import Path
eso_cache_folder = Path(eso.cache_location)
from astropy.io import fits
from harpscompare import doppler

# Modules and more modules
import sys
sys.path.append("..")
import harpscompare
from astropy.table import Table
import pandas

# Input Candidate hits text file
#infile = Path("results-tables/thebigsearch7,5Threshold3rdRun.txt") # Main run
infile = Path("results-tables/repeater_analysispart1.txt") # Repeater analysis, main run
# Output candidate hits text file (with new verdicts).  Add a tag to the end of the input filename.
filtered_file = Path("results-tables/repeater-main-filtered_hits_nohk.txt")
handk_file = Path("results-tables/repeater-main-handklines.txt")

stars = [x.split(',')[0] for x in open(infile).readlines()]
spectral_types = [x.split(',')[1] for x in open(infile).readlines()]
specfiles = [x.split(',')[2] for x in open(infile).readlines()]
hits_start = [x.split(',')[3] for x in open(infile).readlines()]
hits_end = [x.split(',')[4] for x in open(infile).readlines()]
waves1 = [x.split(',')[5] for x in open(infile).readlines()]
waves2 = [x.split(',')[6] for x in open(infile).readlines()]
waves_orig = [x.split(',')[7] for x in open(infile).readlines()]

spike_table = Table()
spike_table['stars'] = stars
spike_table['spectral_types'] = spectral_types
spike_table['specfiles'] = specfiles
spike_table['hits_start'] = hits_start
spike_table['hits_end'] = hits_end
spike_table['waves1'] = waves1
spike_table['waves2'] = waves2
spike_table['waves_orig'] = waves_orig
spike_table.add_column(spike_table['stars'],name='HorK')
spike_table.pprint()
spike_table['HorK'][:] = ' '


# Loop over the entire input list of candidate spikes.
for row in spike_table:
    # Replace colons with underscores (needed for Windows)
    if replace_underscores:
        spec_fname = Path(row['specfiles']).name.replace(":","_")
    else:
        spec_fname = Path(row['specfiles']).name
    # Pull files from user's eso cache folder, not the directory listed in the input txtfile
    spec_path = eso_cache_folder/spec_fname
    print(f"{row['stars']}: {spec_fname}")
    # Download spectra and ccd images if necessary
    if not spec_path.exists():
        harpscompare.download_spectrum(spec_path.stem)
    # Central wavelength
    central_wavelength = (float(row['waves1'])+float(row['waves2']))/2
    fitsfile = fits.open(spec_path)
    v = fitsfile[0].header["HIERARCH ESO TEL TARG RADVEL"]

    if abs(v) > 0 and abs(v) < 99999.0:
        dopplershifted = doppler(central_wavelength,v)
        if int((dopplershifted)) == 3933 or int(dopplershifted) == 3968:
            row['HorK'] = 'T'
        else:
            row['HorK'] = 'F'
    else:
        row['HorK'] = 'F'

# Alternate method: Positive or negative V is okay
 
# Write hits containing H or K lines to one file...
spike_table[spike_table['HorK']=='T'].write(handk_file,format='csv',overwrite=True)
# And hits that aren't H or K lines to another.
spike_table[spike_table['HorK']=='F'].write(filtered_file,format='csv',overwrite=True)
spike_table.write('tmp.txt',format='csv',overwrite=True)