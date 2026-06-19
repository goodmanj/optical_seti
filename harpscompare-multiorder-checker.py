# harpscompare-multiorder-checker: Parse through a list of optical seti candidates, and use
# "harpscompare" to display the spectra of "UFO" candidate spikes, along with all CCD image regions 
# containing that that spectral region.  User can type in a new verdict for the classification
# of the spike (UFO, CR, SE, etc) based on whether the spike appears in both spectral orders (UFO) or 
# not (CR).  The full table (including the new verdict) is saved to a new file.

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

# Modules and more modules
import sys
sys.path.append("..")
import matplotlib.pyplot as plt
import harpscompare
from matplotlib.widgets import TextBox

# When user hits "enter" in the text box, just close the figure and go on to the next.
def textbox_handler(context):
    plt.close()

# Input Candidate hits text file
infile = Path("CoreInvestigationPartI.txt")
# Output candidate hits text file (with new verdicts).  Add a tag to the end of the input filename.
outfile = Path(infile.stem + "_JCG"+infile.suffix)

# Read in Benji's verdicts, and create a table from them.
from astropy.table import Table

verdict_table = Table.read(infile,format='pandas.csv',
                           names=['star','startype','dist','start_ix','end_ix','spec_fname',
                                  'raw_fname','start_wavel','end_wavel','verdict'])
verdict_table.add_column(verdict_table['verdict'],name='new_verdict')

# Loop over the entire input list of candidate spikes.
for row in verdict_table:
    # Only look at spikes previously classified as UFOs.
    if row['verdict']=='UFO':
        # Replace colons with underscores (needed for Windows)
        if replace_underscores:
            spec_fname = Path(row['spec_fname']).name.replace(":","_")
            raw_fname = Path(row['raw_fname']).name.replace(":","_")
        else:
            spec_fname = Path(row['spec_fname']).name
            raw_fname = Path(row['raw_fname']).name
        # Pull files from user's eso cache folder, not the directory listed in the input txtfile
        spec_path = eso_cache_folder/spec_fname
        raw_path = eso_cache_folder/raw_fname
        print(f"{row['star']}: {spec_fname} - {row['verdict']}")
        # Download spectra and ccd images if necessary
        if not spec_path.exists():
            harpscompare.download_spectrum(spec_path.stem)
        if not raw_path.exists():
            harpscompare.download_associated_raw(spec_path)
        # Central wavelength and range to plot
        mid_lamb = ((float(row['start_wavel'])+float(row['end_wavel']))/2)/10
        lamb_range = [mid_lamb-.5,mid_lamb+.5]
        plt.figure(1,figsize=(8,10))
        plt.clf()
        # Add textbox for user input to graph figure
        axbox = plt.gcf().add_axes((0.8, 0.0, 1.0, 0.05))
        text_box = TextBox(axbox,"Verdict")
        text_box.set_val(row['verdict'])  # Old verdict by default
        text_box.on_submit(textbox_handler)
        # Draw spectrum and CCD file subplots
        harpscompare.compare_spec_to_raw(spec_path,raw_path,lamb=mid_lamb,lamb_range=lamb_range,
                                        multi_order=True,doppler_shift=True)
        # Once figure window has closed, change "new verdict" in table to whatever the user typed in
        row['new_verdict'] = text_box.text
        print(f"{row['star']}: {spec_fname} - {row['verdict']} --> {row['new_verdict']}")
        # Write out new verdict file every time.
        verdict_table.write(outfile,format='csv',overwrite=True)

