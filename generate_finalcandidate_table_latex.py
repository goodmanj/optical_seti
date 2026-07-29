from pathlib import Path
import astropy.table

t = astropy.table.Table.read('results-tables/OSETI HARPS Final Candidates.csv',
                names=['star','type','hits_start','specfile','ccdfile','wavel','verdict','source','empty'],
                format='pandas.csv',skiprows=1)

for row in t:
    row['ccdfile'] = Path(row['ccdfile']).stem
    row['ccdfile'] = row['ccdfile'][6:]
    row['ccdfile'] = row['ccdfile'].replace("T"," ")

repeater_mask = t['source']=='Repeaters'
t_repeaters_only = t[repeater_mask]
t_core = t[~repeater_mask]

t_core['star','type','wavel','ccdfile'].write('results-tables/tier4table.txt',
        format='ascii.latex',overwrite=True,formats={"wavel":"%12.3f"})
t_repeaters_only['star','type','wavel','ccdfile'].write('results-tables/tier4table_repeaters.txt',
        format='ascii.latex',overwrite=True,formats={"wavel":"%12.3f"})
