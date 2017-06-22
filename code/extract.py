#!/usr/bin/python3

import sys 
import zipfile
import pandas as pd


outdir = sys.argv[1]

bio_df = pd.read_csv('~/biographies/metadata/hathi_ic_biog.tsv', sep='\t')

bioindex = pd.read_csv('/media/secure_volume/index/bioindex.tsv', sep='\t')

merge_bioindex = pd.merge(
    bio_df, bioindex,
    how='inner',
    left_on='docid',
    right_on='htid')

for suffix in merge_bioindex.filesuffix.unique():
    volsplit_file = 'volsplit'+str(suffix)+'.zip'
    volsplit_df = merge_bioindex.loc[merge_bioindex.filesuffix == suffix,:]
    try:
        with zipfile.ZipFile('/media/secure_volume/'+volsplit_file, 'r') as myzip:
            for idx, row in volsplit_df.iterrows():
                filename = row['mainid']+'.zip'
                myzip.extract(filename, outdir)
    except Exception as e:
        print('ERROR:',filname,'not found in',volsplit_file,'!',e)
