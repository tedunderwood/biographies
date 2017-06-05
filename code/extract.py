#!/usr/bin/python3

import sys
import os
import csv
import zipfile

start = int(sys.argv[1])
end = int(sys.argv[2])

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


get_bios(start, end)
