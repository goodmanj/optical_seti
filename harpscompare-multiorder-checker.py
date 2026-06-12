# harpscompare-multiorder-checker: Parse through a list of optical seti candidates, and use
# "harpscompare" to display the spectra of "UFO" candidate spikes, along with all CCD image regions 
# containing that that spectral region.  User can type in a new verdict for the classification
# of the spike (UFO, CR, SE, etc) based on whether the spike appears in both spectral orders (UFO) or 
# not (CR).  The full table (including the new verdict) is saved to a new file.

eso_login = "goodmanj"
from astroquery.eso import Eso
eso = Eso()
eso.login(username=eso_login)
from pathlib import Path
eso_cache_folder = Path(eso.cache_location)

import sys
sys.path.append("..")
import optical_seti_functions
import seti_catalog_functions
import csv
import random
import matplotlib.pyplot as plt
import numpy as np
from specutils import Spectrum
from specutils.fitting import fit_lines
from astropy.modeling import models
from astropy import units as u
import harpscompare
from matplotlib.widgets import TextBox

def textbox_handler(context):
    plt.close()

infile = Path("CoreInvestigationPartI.txt")
outfile = Path(infile.stem + "_JCG"+infile.suffix)

# Read in Benji's verdicts, and create a table from them.
from astropy.table import Table

verdict_table = Table.read(infile,format='pandas.csv',
                           names=['star','startype','dist','start_ix','end_ix','spec_fname',
                                  'raw_fname','start_wavel','end_wavel','verdict'])
verdict_table.add_column(verdict_table['verdict'],name='new_verdict')

for row in verdict_table:
    # Only look at spikes previously classified as UFOs.
    if row['verdict']=='UFO':
        spec_fname = Path(row['spec_fname']).name.replace(":","_")
        spec_path = eso_cache_folder/spec_fname
        raw_fname = Path(row['raw_fname']).name.replace(":","_")
        raw_path = eso_cache_folder/raw_fname
        print(f"{row['star']}: {spec_fname} - {row['verdict']}")
        if not spec_path.exists():
            harpscompare.download_spectrum(spec_path.stem)
        if not raw_path.exists():
            harpscompare.download_associated_raw(spec_path)
        mid_lamb = ((float(row['start_wavel'])+float(row['end_wavel']))/2)/10
        lamb_range = [mid_lamb-.5,mid_lamb+.5]
        plt.figure(1,figsize=(8,10))
        plt.clf()
        axbox = plt.gcf().add_axes((0.8, 0.0, 1.0, 0.05))
        text_box = TextBox(axbox,"Verdict")
        text_box.set_val(row['verdict'])
        text_box.on_submit(textbox_handler)
        harpscompare.compare_spec_to_raw(spec_path,raw_path,lamb=mid_lamb,lamb_range=lamb_range,
                                        multi_order=True,doppler_shift=True)
        row['new_verdict'] = text_box.text
        print(f"{row['star']}: {spec_fname} - {row['verdict']} --> {row['new_verdict']}")
        verdict_table.write(outfile,format='csv',overwrite=True)

