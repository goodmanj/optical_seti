from astroquery.eso import Eso
from astropy.io import fits
from optical_seti_functions import seti_spike_analyzer
# import csv
eso = Eso()
eso.login("Spaceboy42")
target_list = [x.split('\t')[0] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\OSETI_targets.txt").readlines()]
spectral_types = [x.split('\t')[3] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\OSETI_targets.txt").readlines()] #Another 
output = open("setitrialoutput2.txt", "a")
output.write("STAR, SPECTRAL TYPE, SPECTRAL INDICES, OBSERVATION FILE") #add wavelength variable.
for (star, spectral_type) in zip(target_list, spectral_types):
    print(star)
    tbl = eso.query_surveys('HARPS', target= star)
    data_files = eso.retrieve_data(tbl['ARCFILE'][:])
    for file in data_files:
        print(str(file))
        fits_file = fits.open(file)
        spectral_data = fits_file[1].data
        wave = spectral_data[0][0]
        arr1 = spectral_data[0][1]
        arr2 = spectral_data[0][2]
        hits_start, hits_end, count  = seti_spike_analyzer(arr1, min_count = 4, max_count = 90, threshold_multiplier = 4, stwindow = 101, window_size = 101)
        wavelength = wave[hits_start]
        if len(hits_start) != 0:
            output.write("{} / {} / {} / {} / {}\n".format(star, spectral_type, hits_start, file, wavelength))
    #file.close()


# if len(hits_start) != 0 and len(hits_end) !=0:
    # with open('TOI-7001.csv', 'w', newline='') as csvfile:
        #     fieldnames =['STAR','OBSERVATION/FILE', 'SPECTRAL INDICES']
        #     thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     thewriter.writeheader()  
        #     thewriter.writerow({ 'STAR':str(star), 'OBSERVATION/FILE':str(file), 'SPECTRAL INDICES':(hits_start, hits_end)}) #add in: "WAVELENGTH: wave[hits_start], WIDTH: pixel_count, SPECTRAL_TYPE
#NOTES: seems to be doing a weird thing--it only outputs the last file  from the last star...why can't the CSV file output all of them?
    #thewriter.writeheader()
    #thewriter.writerow({'OBSERVATION/FILE':str(file), 'SPECTRAL INDICES':z})

    
#, 'WAVELENGTHS':wave[z]    
# tbl = eso.query_surveys('HARPS', target= x)
# data_files = eso.retrieve_data(tbl['ARCFILE'][:])
# from astropy.io import fits
# from optical_seti_functions import seti_spike_analyzer
# for file in data_files:
#     print(str(file))
#     fits_file = fits.open(file)
#     spectral_data = fits_file[1].data
#     wave = spectral_data[0][0]
#     arr1 = spectral_data[0][1]
#     arr2 = spectral_data[0][2]
#     seti_spike_analyzer(arr1, min_count = 4, max_count = 8, threshold_multiplier = 5, stwindow = 101, window_size = 101)
#     print('''
          
          
#           ''')
# import csv
# with open('time_domain_seti.csv', 'w', newline='') as csvfile:
#     fieldnames =['OBSERVATION/FILE', 'SPECTRAL INDICES']
#     thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
#     thewriter.writeheader()
#for file in data_files:
#thewriter.writerow({'OBSERVATION/FILE':str(file), 'SPECTRAL INDICES':seti_spike_analyzer(arr1, min_count = 4, max_count = 8, threshold_multiplier = 4, stwindow = 100)})

