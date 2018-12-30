# evaluate_hypotheses_docadjusted.py

# This script evaluates our preregistered hypotheses using
# the doctopics file produced by MALLET.

import sys, csv
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean, cosine

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

# MAIN starts

args = sys.argv

doctopic_path = args[1]

meta = pd.read_csv('../../metadata/filtered_fiction_plus_18c.tsv', sep = '\t', index_col = 'docid')
meta = meta[~meta.index.duplicated(keep = 'first')]

docsbyauthor = dict()

groupedbyauthor = meta.groupby('author')
for auth, group in groupedbyauthor:
    docsbyauthor[auth] = group.index.tolist()

hypotheses = []
significant_persons = set()

with open('../../evaluation/hypotheses.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        ids = [row['firstsim'], row['secondsim'], row['distractor']]
        for anid in ids:
            if '_' in anid:
                anid = anid.replace('_', '|')
            significant_persons.add(anid)
        hypotheses.append(row)

numtopics = 0
chardict = dict()
vectorsbydoc = dict()

with open(doctopic_path, encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        charid = fields[1]
        vector = np.array(fields[2 : ], dtype = 'float32')
        docid = charid.split('|')[0]
        if docid not in vectorsbydoc:
            vectorsbydoc[docid] = []
        vectorsbydoc[docid].append(vector)

        if charid in significant_persons:
            chardict[charid] = vector

# Make doc centroids

doc_centroids = dict()

for doc, group in vectorsbydoc.items():

    centroid = np.sum(group, axis = 0) / len(group)
    doc_centroids[doc] = centroid

right = 0
wrong = 0
cosright = 0
coswrong = 0
answers = []

def adjusted_vector(charid):
    global chardict, doc_centroids

    raw_vector = chardict[charid]

    docid = getdoc(charid)
    normal_vector = doc_centroids[docid]

    divergence = raw_vector - normal_vector

    if np.isnan(np.sum(divergence)):
        print('error', charid)

    return divergence


for h in hypotheses:

    first = adjusted_vector(h['firstsim'])
    second = adjusted_vector(h['secondsim'])
    distract = adjusted_vector(h['distractor'])

    pair_euclid = euclidean(first, second)
    pair_cos = cosine(first, second)

    # first comparison

    distraction1 = euclidean(first, distract)
    distraction1cos = cosine(first, distract)

    if distraction1 < pair_euclid:
        wrong += 1
        answers.append([h['firstsim'], h['distractor'], 'wrong'])
    else:
        right += 1
        answers.append([h['firstsim'], h['distractor'], 'right'])

    if distraction1cos < pair_cos:
        coswrong += 1
    else:
        cosright += 1

    # second comparison

    distraction2 = euclidean(second, distract)
    distraction2cos = cosine(second, distract)

    if distraction2 < pair_euclid:
        wrong += 1
        answers.append([h['hypothesisnum'], h['secondsim'], h['distractor'], 'wrong'])
    else:
        right += 1
        answers.append([h['hypothesisnum'], h['secondsim'], h['distractor'], 'right'])

    if distraction2cos < pair_cos:
        coswrong += 1
    else:
        cosright += 1

print('Euclid: ', right / (wrong + right))
print('Cosine: ', cosright / (coswrong + cosright))








