import csv
import zipfile
import pandas as pd
import glob
import numpy as np
import os

def slicer(outfile, slices):
    
    '''
    Takes an output filename (including extension) and number of output files ('slices') as parameters,
    and uses an index file to create slice files of volumes, their IDs, paths and two columns with '0' 
    and '10001' populated. Part of the biography BookNLP workflow.
    '''
    
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
    
    slice_list = np.array_split(slice_df, slices)
    
    out_num = 0
    
    for slce in slice_list:
        extension = outfile[-4:]
        filename = outfile[:-4]
        file_num = str(out_num)
        outfile_name = (filename+'_'+file_num+extension)
        with open (outfile_name, 'w') as outf:
            slce.to_csv(outf, sep='\t', header=False)
        if out_num != (slices-1):
            out_num += 1
        
        print("Wrote", len(slce), "rows to", outfile_name)
