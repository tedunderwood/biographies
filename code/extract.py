#!/usr/bin/python3

import sys
import os
import csv
import zipfile
import pandas as pd
import glob

start = int(sys.argv[1])
end = int(sys.argv[2])
slice_path= sys.argv[3]

def get_bios(start,end):
'''
Iterates over the specified rows of bioindex.tsv,
gets the HathiTrust ID, and passes the file names to extract().
'''
    # skip header
    header = 0
    if start == header
        start = 1

    with open('/media/secure_volume/index/bioindex.tsv') as bios:
        tsvreader = csv.reader(bios, delimeter='\t')
        count = 0
        for row in tsvreader:
            if (end >= count >= start):
                filename = row[0]+'.zip'
                # print('bio name=', filename)
                extract(filename)
            count += 1

def extract(filename):
'''
Iterates over each volsplit zipfile, 
searches for the passed filename in the contents, 
extracts it into the holding folder.
'''
    all_vols = [ vol for vol in os.listdir('/media/secure_volume/')
            if vol.startswith('volsplit') ]

    for folder in all_vols:
        with zipfile.ZipFile('/media/secure_volume/'+folder, 'r') as myzip:
            if filename in myzip.namelist():
                # print('file=', name)
                myzip.extract(name, '..holding_folder')

def slicer(outfile):
    idx_file_path = '/media/secure_volume/index/bioindex.tsv'
    holding_folder_path = '/media/secure_volume/holding_folder/'
    bio_idx_df = pd.read_table(idx_file_path)
    bio_idx_df.set_index('mainid')
    mainid_list = [vol for vol in os.listdir(holding_folder_path) if vol.endswith('.zip')]
    # print(mainid_list)
    mainid_list_clean = [item[0:-4] for item in mainid_list]
    htid_list = bio_idx_df.htid[mainid_list_clean]
    htid_list_clean = list(htid_list.index)
    print(type(htid_list_clean))
    file_path_list = glob.glob(holding_folder_path+'*.zip')
    # print('file path list has: ',len(file_path_list))
    # print('htid_list has', len(htid_list))
    # print(htid_list)
    slice_df = pd.DataFrame(htid_list)
    slice_df['path'] = file_path_list
    slice_df['c'] = 0
    slice_df['d'] = 10001
    with open(outfile, 'w') as outf:
        slice_df.to_csv(outfile, sep='\t', header=False)


get_bios(start, end)
slicer(slice_path)
