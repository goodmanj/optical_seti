from pathlib import Path
import astropy.table
from matplotlib import pyplot as plt

t = astropy.table.Table.read('results-tables/OSETI HARPS Final Candidates.csv',
                names=['star','type','hits_start','specfile','ccdfile','wavel','verdict','source','empty'],
                format='pandas.csv',skiprows=1)

repeater_mask = t['source']=='Repeaters'
t_repeaters_only = t[repeater_mask]
t_core = t[~repeater_mask]

starlist = sorted(list(set(t_core['star']))) # Get alphabetically sorted list of unique names
# Build a list containing the list of candidate wavelengths for each star.
wavel_list = [list(t[t['star']==starname]['wavel']) for starname in starlist] 

plt.figure(1)
plt.figure(1).set_size_inches(w=6,h=4)
plt.eventplot(wavel_list)
plt.yticks(range(len(starlist)),labels=[str(star) for star in starlist])
plt.gca().yaxis.set_inverted(True)
plt.xlabel('Wavelength (angstroms)')
plt.grid()
plt.tight_layout()
plt.savefig('manuscript-figures/candidate_wavelengths.pdf',format='pdf')