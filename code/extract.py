#!/usr/bin/python3

import sys
import os
import shutil
import csv
import zipfile
import pandas as pd
import glob

start = int(sys.argv[1])
end = int(sys.argv[2])
slice_path= sys.argv[3]

# remove holding_folder if it exists, and create new folder
# use 'rm -r /holding_folder/* in shell script instead?'
holding_path = '/media/secure_volume/holding_folder'
if os.path.isdir(holding_path):
    shutil.rmtree(holding_path)
os.mkdir(holding_path)        

def extract(start,end):
    '''
    Iterates over the specified rows of bioindex.tsv,
    gets the HathiTrust ID, and passes the file names to extract().
    '''
    # skip header
    header = 0
    if start == header:
        start = 1

    with open('/media/secure_volume/index/bioindex.tsv') as bios:
        tsvreader = csv.reader(bios, delimiter='\t')
        count = 0
        for row in tsvreader:
            if (end >= count >= start):
                filename = row[0]+'.zip'
                volsplit_file = 'volsplit'+row[2]+'.zip'
                #print("count:", count, volsplit_file, filename)
            
                with zipfile.ZipFile('/media/secure_volume/'+volsplit_file, 'r') as myzip:
                    try:
                        #print(filename, 'found in:', myzip.filename)
                        myzip.extract(filename, '/media/secure_volume/holding_folder')
                    except Exception as e:
                        print('ERROR:',filename,'not found!', e)

            count += 1


def slicer(outfile):
    idx_file_path = '/media/secure_volume/index/bioindex.tsv'
    holding_folder_path = '/media/secure_volume/holding_folder/'
    bio_idx_df = pd.read_table(idx_file_path)
    bio_idx_df.set_index('mainid', inplace = True)
    mainid_list = [vol for vol in os.listdir(holding_folder_path) if vol.endswith('.zip')]
    # remove '.zip' from file names
    mainid_list_clean = [item[0:-4] for item in mainid_list]

    #subset bioindex on holding_folder IDs
    htid_series = bio_idx_df.htid[mainid_list_clean]
    file_path_list = glob.glob(holding_folder_path+'*.zip')
    # print('file path list has: ',len(file_path_list))
    # print('htid_list has', len(htid_list))
    
    slice_df = pd.DataFrame(htid_series)
    slice_df['path'] = file_path_list
    slice_df['c'] = 0
    slice_df['d'] = 10001

    with open(outfile, 'w') as outf:
        slice_df.to_csv(outfile, sep='\t', header=False)

    print("Wrote", len(slice_df), "rows to", outfile)

extract(start, end)
slicer(slice_path)
