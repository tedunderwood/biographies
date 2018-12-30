# evaluate_hypotheses.py

# This script evaluates our preregistered hypotheses using
# the doctopics file produced by MALLET.

import sys, csv
import numpy as np
from scipy.spatial.distance import euclidean, cosine

def getdoc(anid):
    '''
    Gets the docid part of a character id
    '''

    if '|' in anid:
        thedoc = anid.split('|')[0]
    elif '_' in anid:
        thedoc = anid.split('_')[0]
    else:
        print('error', anid)
        thedoc = anid

    return thedoc

# MAIN starts

args = sys.argv

doctopic_path = args[1]

datedict = dict()
docdates = dict()

with open('../../metadata/filtered_fiction_plus_18c.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:

        inferreddate = int(row['inferreddate'])
        docid = row['docid']

        if inferreddate not in datedict:
            datedict[inferreddate] = []
        datedict[inferreddate].append(docid)
        docdates[docid] = inferreddate

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
docdict = dict()

with open(doctopic_path, encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        charid = fields[1]
        vector = np.array(fields[2 : ], dtype = 'float32')
        docid = charid.split('|')[0]
        if docid not in docdict:
            docdict[docid] = []
        docdict[docid].append(vector)

        if charid in significant_persons:
            chardict[charid] = vector

centroids = dict()

for k, v in docdict.items():
    centroid = np.sum(v, axis = 0) / len(v)
    centroids[k] = centroid

yr_centroids = dict()

for yr in range (1780, 2009):
    doc_centroids = []
    for yr2 in range(yr - 5, yr + 6):
        if yr2 not in datedict:
            continue
        for doc in datedict[yr2]:
            if doc in centroids:
                doc_centroids.append(centroids[doc])
    centroid = np.sum(doc_centroids, axis = 0) / len(doc_centroids)
    yr_centroids[yr] = centroid

right = 0
wrong = 0
cosright = 0
coswrong = 0
answers = []

missing = set()

for s in significant_persons:
    if s not in chardict:
        print(s)
        missing.add(s)


for idx, h in enumerate(hypotheses):

    skip = False
    ids = [h['firstsim'], h['secondsim'], h['distractor']]
    for anid in ids:
        if anid in missing:
            skip = True
    if skip:
        continue

    first = chardict[h['firstsim']] - yr_centroids[docdates[getdoc(h['firstsim'])]]
    second = chardict[h['secondsim']] - yr_centroids[docdates[getdoc(h['secondsim'])]]
    distract = chardict[h['distractor']] - yr_centroids[docdates[getdoc(h['distractor'])]]

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
        answers.append([idx, h['secondsim'], h['distractor'], 'wrong'])
    else:
        right += 1
        answers.append([idx, h['secondsim'], h['distractor'], 'right'])

    if distraction2cos < pair_cos:
        coswrong += 1
    else:
        cosright += 1

print('Euclid: ', right / (wrong + right))
print('Cosine: ', cosright / (coswrong + cosright))








