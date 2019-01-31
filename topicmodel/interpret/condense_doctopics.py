# condense_doctopics.py

# The doctopics file produced by MALLET can be very
# bulky. This script condenses it by keeping only the
# rows needed to evaluate our preregistered hypotheses.

# At the same time, it produces centroids for authors and
# for particular years. These become useful in smart
# evaluation that compares two characters within the tightest
# available context.

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

args = sys.argv

doctopic_path = args[1]
outpath = doctopic_path.replace('_doctopics.txt', '_vols.tsv')
print(outpath)
centroidpath = doctopic_path.replace('_doctopics.txt', '_centroids.tsv')

if os.path.isfile(outpath):
    print(outpath, ' already exists')
    user = input('Ok to overwrite (y for yes): ')
    if user != 'y':
        sys.exit(0)

# Read metadata in order to create lists of documents linked
# by an author or by a year.

print('Reading metadata and hypotheses.')

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

print()
print('Reading the doctopics file.')

outlines = []
vectorsbydoc = dict()
significant_authors = set()

with open(doctopic_path, encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        charid = fields[1]
        docid = getdoc(charid)
        if docid in significant_vols:
            outlines.append(line)
            author = meta.loc[docid, 'author']
            significant_authors.add(author)

        vector = np.array(fields[2 : ], dtype = 'float32')
        if docid not in vectorsbydoc:
            vectorsbydoc[docid] = []
        vectorsbydoc[docid].append(vector)

veclen = len(vector)

print()
print('Calculating year centroids.')

yearcentroids = dict()

for i in range (1780, 2008):
    floor = i - 20
    ceiling = i + 21
    if floor < 1780:
        floor = 1780
    if ceiling > 2007:
        ceiling = 2007

    charsinwindow = []

    for j in range(floor, ceiling):
        for doc in docsbyyear[j]:
            if doc in vectorsbydoc:
                charsinwindow.extend(vectorsbydoc[doc])

    centroid = np.sum(charsinwindow, axis = 0) / len(charsinwindow)
    assert len(centroid) == veclen
    yearcentroids[i] = centroid

print()
print('Calculating author centroids.')

authcentroids = dict()

for author in significant_authors:
    charsinauthor = []
    for doc in docsbyauthor[author]:
        if doc in vectorsbydoc:
            charsinauthor.extend(vectorsbydoc[doc])

    centroid = np.sum(charsinauthor, axis = 0) / len(charsinauthor)
    assert len(centroid) == veclen
    authcentroids[author] = centroid

print()
print('Writing condensed volumes.')

with open(outpath, mode = 'w', encoding = 'utf-8') as f:
    for line in outlines:
        f.write(line)

print()
print('Writing centroids.')

fieldnames = ['centtype', 'id']
fieldnames.extend([str(x) for x in range(veclen)])

with open(centroidpath, mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, delimiter = '\t', fieldnames = fieldnames)
    writer.writeheader()

    for auth, centroid in authcentroids.items():
        out = dict()
        out['centtype'] = 'author'
        out['id'] = auth
        for i in range(veclen):
            out[str(i)] = centroid[i]
        writer.writerow(out)

    for year, centroid in yearcentroids.items():
        out = dict()
        out['centtype'] = 'year'
        out['id'] = year
        for i in range(veclen):
            out[str(i)] = centroid[i]
        writer.writerow(out)

