import sys
from pathlib import Path
cwd = Path(__file__).parent.resolve() 

# Modify these as needed
eso_login="goodmanj"
starlist= cwd/ "OSETI_targets_subset.txt"
results=cwd / "OSETI_results.txt"

optical_seti_dir = cwd.parent.resolve() 
sys.path.append(str(optical_seti_dir))
import big_search
big_search.do_search(withlogin=eso_login,withstarlist=starlist,withresults=results)