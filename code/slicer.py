import csv
import zipfile
import pandas as pd
import glob
import numpy as np
import os
import sys


infile = sys.argv[1]
outfile = sys.argv[2]
nslices = int(sys.argv[3])

def slicer(infile, outfile, slices):
    
    '''
    Takes an output filename (including extension) and number of output files ('slices') as parameters,
    and uses an index file to create slice files of volumes, their IDs, paths and two columns with '0' 
    and '10001' populated. Part of the biography BookNLP workflow.
    '''
    
    balanced_df = pd.read_csv(infile, sep='\t')   
     
    slice_df = pd.DataFrame(balanced_df.loc[:,['htid','mainid']])
    # add path column
    slice_df['mainid'] = '/media/secure_volume/holding_folder/'+slice_df['mainid']+'.zip' 
    slice_df['c'] = 0
    slice_df['d'] = 10001
    
    slice_list = np.array_split(slice_df, slices)
    
    out_num = 0
    
    for slce in slice_list:
        extension = outfile[-4:]
        filename = outfile[:-4]
        file_num = str(out_num)
        outfile_name = (filename+'_'+file_num+extension)
        slce.to_csv(outfile_name, sep='\t', header=False, index=False)
        if out_num != (slices-1):
            out_num += 1
        
        print("Wrote", len(slce), "rows to", outfile_name)

slicer(infile, outfile, nslices)
