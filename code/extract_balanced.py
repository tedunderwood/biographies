#!/usr/bin/python3

import sys
import os
import shutil
import csv
import zipfile
import pandas as pd
import glob

infile = sys.argv[1]
outfile = sys.argv[2]

# remove holding_folder if it exists, and create new folder
# use 'rm -r /holding_folder/* in shell script instead?'
holding_path = '/media/secure_volume/holding_folder'
if os.path.isdir(holding_path):
    shutil.rmtree(holding_path)
os.mkdir(holding_path)        

def extract(infile):
    '''
    Merges bioindex.tsv with the infile (balanced data),
    finds the volsplit.zip location for each bio file and 
    extracts the files into secure_volume/holding_folder.
    '''
    
    bioindex = pd.read_csv('/media/secure_volume/index/bioindex.tsv', sep='\t')
    in_df = pd.read_table(infile)
    
    balanced_bioindex = pd.merge(
        in_df, bioindex,
        how='inner',
        left_on='docid',
        right_on='htid').loc[
        :,['mainid','htid','filesuffix']
        ]

    for idx, row in balanced_bioindex.iterrows():
        filename = row['mainid']+'.zip'
        volsplit_file = 'volsplit'+row['filesuffix']+'.zip'
        print(filename, volsplit_file)

        with zipfile.ZipFile('/media/secure_volume/'+volsplit_file, 'r') as myzip:
            try:
                #print(filename, 'found in:', myzip.filename)
                myzip.extract(filename, '/media/secure_volume/holding_folder')
            except Exception as e:
                print('ERROR:',filename,'not found!', e)


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

extract(infile)
slicer(outfile)
