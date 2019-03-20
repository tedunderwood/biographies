# autocondense_rolethemes.py

# This script plays the same role for my custom topic model
# that condense_doctopics plays for MALLET:
# we're creating a portable subset of the doct-topic table
# that answers preregistered hypotheses.

# There are differences here because my doctopic file has a
# slightly different format, and especially because I haven't
# normalized the vectors yet. Also, I add authors to the output.

import sys, csv, os
import numpy as np
import pandas as pd

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

def condense_a_file(inpath, outpath, themect):

    # Read metadata in order to create lists of documents linked
    # by an author or by a year.

    meta = pd.read_csv('../../metadata/filtered_fiction_plus_18c.tsv', sep = '\t', index_col = 'docid')
    meta = meta[~meta.index.duplicated(keep = 'first')]

    docsbyauthor = dict()
    groupedbyauthor = meta.groupby('author')
    for auth, group in groupedbyauthor:
        docsbyauthor[auth] = group.index.tolist()

    docsbyyear = dict()
    groupedbyyear = meta.groupby('inferreddate')
    for yr, group in groupedbyyear:
        docsbyyear[yr] = group.index.tolist()

    significant_vols = set()

    with open('../../evaluation/hypotheses.tsv', encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        for row in reader:
            ids = [row['firstsim'], row['secondsim'], row['distractor']]
            for anid in ids:
                docid = getdoc(anid)
                significant_vols.add(docid)

    outlines = []
    vectorsbydoc = dict()
    significant_authors = set()

    with open(inpath, encoding = 'utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            if fields[0] != 'char':
                continue
            charid = fields[1]
            docid = getdoc(charid)
            if docid in significant_vols:
                vector = np.array(fields[3 : ], dtype = 'float32')
                total = np.sum(vector)
                if total < 1:
                    continue
                vector = vector / total
                author = meta.loc[docid, 'author']
                line = [author, charid]
                line.extend([str(x) for x in vector])
                outlines.append(line)

    with open(outpath, mode = 'w', encoding = 'utf-8') as f:
        for line in outlines:
            f.write('\t'.join(line) + '\n')


