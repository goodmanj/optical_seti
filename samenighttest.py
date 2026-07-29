from astroquery.eso import Eso
eso = Eso()
from pathlib import Path
eso_cache_folder = Path(eso.cache_location)
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
if not eso.authenticated():
    eso.login(username="goodmanj", store_password=True)
def cached_filename(file): 
    file_no_colon = str(file).replace(":","_") 
    return eso_cache_folder/(file_no_colon+".fits")
def doppler(wave,v): 
    c = 2.998e5 # km/s 
    beta = v/c 
    return wave*np.sqrt((1-beta)/(1+beta))


samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2011-09-25T05:25:30.812..2011-09-25T09:25:30.812') 
wavelength = 6688.415 #
#samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2008-07-25T02:50:31.896..2008-07-25T06:50:31.896') 
#wavelength = 5593.86 #
#samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2012-11-20T03:56:02.541..2012-11-20T07:56:02.541') # CoRoT-24
#wavelength = 5983.375 # CoRoT-24
#samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2008-07-25T02:50:31.896..2008-07-25T06:50:31.896') # CoRoT101614469
#wavelength = 5593.895 # CoRoT101614469
#samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2011-12-03T04:43:16.408..2011-12-03T08:43:16.408') # CoRoT221699621
#wavelength = 5446.725 # CoRoT221699621
# samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2013-06-01T03:04:25.906..2013-06-01T05:04:25.906') #HIP59341
# samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2018-02-11T01:10:40.597..2018-02-11T03:10:40.597') # CD-312415
# samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2018-04-10T01:25:08.275..2018-04-10T05:25:08.275') # GJ317
# samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2013-06-01T02:16:19.375..2013-06-01T06:16:19.375') #CoRoT-32
# samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2018-02-01T00:00:30.839..2018-02-01T03:42:30.839') # HD34642
# samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2013-06-01T00:00:53.391..2013-06-01T03:19:53.391') # HD94126
# samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2006-03-25T22:02:33.378..2006-03-26T02:02:33.378') # HD49088
# samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2012-10-22T23:39:09.238..2012-10-22T25:39:09.238') #HIP87607
# samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2013-04-30T09:50:45.212..2013-04-30T11:50:45.212') #HIP87607
# samenight_tbl = eso.query_surveys(surveys='HARPS',date_obs='2005-07-20T04:08:04.468..005-07-20T06:08:04.468') # GJ4291
samenight_tbl.pprint()
specarcfile = samenight_tbl['ARCFILE']
fits_specfile_names = []
for file in specarcfile:
    fits_specfile_name = cached_filename(file)   # underscore version, used for exists() check
    if not fits_specfile_name.exists():
        print(str(fits_specfile_name) + " to be downloaded")
        result = eso.retrieve_data(file)
        # retrieve_data returns the actual saved path (with colons) — use that instead
        actual_path = Path(result[0]) if isinstance(result, list) else Path(result)
        fits_specfile_names.append(actual_path)
    else:
        print(str(fits_specfile_name) + " exists")
        fits_specfile_names.append(fits_specfile_name)
radvel = []
for f in fits_specfile_names: 
    fitsfile = fits.open(f) 
    radvel.append(fitsfile[0].header["HIERARCH ESO TEL TARG RADVEL"]) 
print(radvel)
plt.figure(1)
plt.figure(1).set_size_inches(8,8)

plt.clf()
specfits = [fits.open(f) for f in fits_specfile_names]
radvels = [f[0].header["HIERARCH ESO TEL TARG RADVEL"] for f in specfits]
berv    = [f[0].header["HIERARCH ESO DRS BERV"] for f in specfits]         # Observatory's velocity in barycentric frame

wave = [f[1].data[0][0] for f in specfits]
arr1 = [f[1].data[0][1] for f in specfits]

wave_starframe = [doppler(wave[i],radvels[i]) for i in range(len(radvels))]
wave_obsframe = [doppler(wave[i],berv[i]) for i in range(len(radvels))]


norm_spec = [s/np.median(s) for s in arr1]
wavelim = [wavelength-5,wavelength+5] #CoRoT-32

plt.subplot(3,1,1)
plt.plot([wavelength,wavelength],[0,8],'r--')
for i in range(len(specfits)): 
    plt.plot(wave[i],norm_spec[i],label=fits_specfile_names[i].stem) 
plt.xlim(wavelim) 
plt.ylim([0,8]) 
plt.legend(loc='right') 
plt.title("Barycenter frame") 
plt.ylabel("Normalized Spectrum") 
plt.subplot(3,1,2)
plt.plot([wavelength,wavelength],[0,8],'r--')
for i in range(len(specfits)): 
    plt.plot(wave_starframe[i],norm_spec[i],label=fits_specfile_names[i].stem) 
plt.xlim(wavelim) 
plt.ylim([0,8]) 
plt.legend(loc='right') 
plt.title("Star frame") 
plt.ylabel("Normalized Spectrum") 
plt.subplot(3,1,3)
plt.plot([wavelength,wavelength],[0,8],'r--')
for i in range(len(specfits)): 
    plt.plot(wave_obsframe[i],norm_spec[i],label=fits_specfile_names[i].stem) 
plt.xlim(wavelim) 
plt.ylim([0,8]) 
plt.legend(loc='right') 
plt.title("Terrestrial frame") 
plt.ylabel("Normalized Spectrum") 

# topax = plt.gca() 
# plt.subplot(2,1,2,sharex=topax,sharey=topax)
# for i in range(len(specfits)): 
#     plt.plot(doppler(wave[i],radvels[i]),norm_spec[i],label=fits_specfile_names[i].stem) 
# plt.xlim(wavelim) 
# plt.ylim([0,2.5]) 
# plt.title('Doppler shifted into stellar frame') 
# plt.ylabel("Normalized Spectrum")
plt.show()