import sys
from pathlib import Path
cwd = Path(__file__).parent.resolve() # The directory this file is in

# Modify these as needed
eso_login="goodmanj"
starlist= cwd/ "OSETI_targets_subset.txt"
downloadlist = cwd / "multistarwidefield_bulk.txt"

optical_seti_dir = cwd.parent.resolve()  # Location of optical SETI scripts
sys.path.append(str(optical_seti_dir))   # Add to path

import seti_catalog_functions
# Download
seti_catalog_functions.bulk_predownload(withlogin=eso_login,withstarlist=starlist,withresults=downloadlist,obs_per_star=20)
