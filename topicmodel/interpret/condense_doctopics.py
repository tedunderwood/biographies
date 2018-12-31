# condense_doctopics.py

# The doctopics file produced by MALLET can be very
# bulky. This script condenses it by keeping only the
# rows needed to evaluate our preregistered hypotheses.

import sys, csv, os

def getdoc(anid):
    '''
    Gets the docid part of a character id
    '''

    if '|' in anid:
        thedoc = anid.split('|')[0]
    else:
        print('error', anid)
        thedoc = anid

    return thedoc

# MAIN starts here

args = sys.argv

doctopic_path = args[1]
outpath = doctopic_path.replace('_doctopics.txt', '_vols.tsv')
print(outpath)

if os.path.isfile(outpath):
    print(outpath, ' already exists')
    user = input('Ok to overwrite (y for yes): ')
    if user != 'y':
        sys.exit(0)

significant_vols = set()

with open('../../evaluation/hypotheses.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        ids = [row['firstsim'], row['secondsim'], row['distractor']]
        for anid in ids:
            docid = getdoc(anid)
            significant_vols.add(docid)

outlines = []

with open(doctopic_path, encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        charid = fields[1]
        docid = getdoc(charid)
        if docid not in significant_vols:
            continue
        else:
            outlines.append(line)

with open(outpath, mode = 'w', encoding = 'utf-8') as f:
    for line in outlines:
        f.write(line)
