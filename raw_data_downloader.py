from astropy.io import fits
from astroquery.eso import Eso
import zlib
eso = Eso()
eso.login("Spaceboy42")
raw_download_record = open("raw_download_record.txt", "w")
target_list = [x.split(',')[0] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\category2.txt").readlines()]
start_index = [x.split(',')[2] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\category2.txt").readlines()]
end_index = [x.split(',')[3] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\category2.txt").readlines()]
reduced_files = [x.split(',')[4] for x in open("C:\\Users\\HAL 9000\\OneDrive\\Documents\\GitHub\\optical_seti\\category2.txt").readlines()]
for (reduced_file, start, end) in zip(reduced_files[1:], start_index[1:], end_index[1:]):
    fits_file = fits.open(reduced_file)
    file_header = fits_file[0].header
    header = file_header["PROV1"]
    observation_name = header[:-5]
    tbl = eso.query_main(column_filters={'instrument': 'HARPS', 'dp_id': observation_name})
    raw_file = eso.retrieve_data(tbl['Dataset ID'], unzip=False)[0][:-2]
    print("{},{},{},{}\n".format(reduced_file,raw_file,start,end))
    raw_download_record.write("{},{},{},{}\n".format(reduced_file,raw_file,start,end))
    raw_download_record.flush()
# close file here