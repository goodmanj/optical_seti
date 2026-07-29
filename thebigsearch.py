# Primary automated search code.

from astropy.io import fits
from optical_seti_functions import seti_spike_analyzer, airglow_elimination
spectral_types = ([x.split(",")[1] for x in open("/Users/blfields/Desktop/LaserInjector/bigsearchstage1.txt").readlines()])
files = ([x.split(",")[2] for x in open("/Users/blfields/Desktop/LaserInjector/bigsearchstage1.txt").readlines()])
stars = ([x.split(",")[0] for x in open("/Users/blfields/Desktop/LaserInjector/bigsearchstage1.txt").readlines()])
distances = ([x.split(",")[3] for x in open("/Users/blfields/Desktop/LaserInjector/bigsearchstage1.txt").readlines()])
output = open("thebigsearch7,5Threshold3rdRun.txt", "w")
airglow_record = open("airglowhits7.5Threshold3rdRun.txt", "w")
nulls = open("blanks7.5threshold3rdRun.txt", "w")
stellar_emission_clusters = open("stellar_emission_clusters7.5Threshold3rdRun.txt", "w")
for star, spectral_type,file,distance in zip(stars,spectral_types,files,distances):
    specfits = fits.open(file)
    wave = specfits[1].data[0][0]
    arr1 = specfits[1].data[0][1]
    print(star)
    hits_start, hits_end, count = seti_spike_analyzer(arr1, min_count = 4, max_count = 500, threshold_multiplier = 7.5, window_size = 1001,percentile=85)
    if (len(hits_start) == 0) and (len(hits_end) == 0):
        nulls.write("{},{},{},{}".format(star,spectral_type,file,distance))
        nulls.flush()
    airglow_hits = airglow_elimination(file,hits_start,hits_end,filter_multiplyer=2.5)
    filtered = [(s, e) for s, e in zip(hits_start, hits_end) if s not in airglow_hits and e not in airglow_hits]
    hits_start, hits_end = (list(x) for x in zip(*filtered)) if filtered else ([], [])
    print(hits_start)
    print(hits_end) 
    print(airglow_hits)
    for start, end in zip(hits_start, hits_end): 
        if len(hits_start) >= 4: 
             stellar_emission_clusters.write("{},{},{},{},{},{},{},{}".format(star,spectral_type,file,start,end,wave[start],wave[end],distance))
             stellar_emission_clusters.flush()
        else:
            output.write("{},{},{},{},{},{},{},{}".format(star,spectral_type,file,start,end,wave[start],wave[end],distance))
            output.flush()
    for glow_air in airglow_hits:
        airglow_record.write("{},{},{},{},{},{}".format(star,spectral_type,file,glow_air,wave[glow_air],distance))

nulls.close()
airglow_record.close()
stellar_emission_clusters.close()
output.close()