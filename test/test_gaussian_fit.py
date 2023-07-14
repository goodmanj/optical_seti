import astropy
import sys

from pathlib import Path
cwd = Path(__file__).parent.resolve() 
optical_seti_dir = cwd.parent.resolve() 
sys.path.append(str(optical_seti_dir))
import optical_seti_functions

eso_cache_path = Path(astropy.config.get_cache_dir()) / "astroquery" / "Eso"

file = eso_cache_path / "ADP.2014-10-06T10_06_38.740.fits"
print(file.exists())
optical_seti_functions.gaussian_curve_fit(file,138185,138189)