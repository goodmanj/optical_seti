import sys
from pathlib import Path
cwd = Path(__file__).parent.resolve() 

# Modify these as needed
eso_login="goodmanj"
starlist= cwd/ "OSETI_targets_subset.txt"
downloadlist = cwd / "multistarwidefield.txt"
results=cwd / "OSETI_results.txt"

optical_seti_dir = cwd.parent.resolve() 
sys.path.append(str(optical_seti_dir))

import seti_catalog_functions
seti_catalog_functions.predownloader(withlogin=eso_login,withstarlist=starlist,withresults=downloadlist)
seti_catalog_functions.do_search(withlogin=eso_login,withstarlist=downloadlist,withresults=results,predownloader_format=True)