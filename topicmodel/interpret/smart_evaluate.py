# smart_evaluation.py

# This script evaluates our preregistered hypotheses using
# the doctopics file produced by MALLET.

import sys, csv, random
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

doctopicpath = args[1]

meta = pd.read_csv('../../metadata/filtered_fiction_plus_18c.tsv', sep = '\t', index_col = 'docid')
meta = meta[~meta.index.duplicated(keep = 'first')]

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

vectorsbydoc = dict()
rawchars = dict()

with open(doctopicpath, encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        charid = fields[1]
        vector = np.array(fields[2 : ], dtype = 'float32')
        docid = charid.split('|')[0]
        if docid not in vectorsbydoc:
            vectorsbydoc[docid] = []
        vectorsbydoc[docid].append(vector)

        if charid in significant_persons:
            rawchars[charid] = vector

# Make doc centroids

doc_centroids = dict()

for doc, group in vectorsbydoc.items():

    centroid = np.sum(group, axis = 0) / len(group)
    doc_centroids[doc] = centroid

# adjust the rawchars for docs

charsrelative2docs = dict()

for charid, vector in rawchars.items():
    docid = getdoc(charid)
    centroid = doc_centroids[docid]
    charsrelative2docs[charid] = vector - centroid

# also adjust them for world mean

charsrelative2world = dict()

allvec = []
for k, v in rawchars.items():
    allvec.append(v)
meanvec = np.mean(allvec, axis = 0)

for p in significant_persons:
    charsrelative2world[p] = rawchars[p] - meanvec

docdistances = []
worlddistances = []
for i in range(100):
    id1 = random.sample(significant_persons, 1)[0]
    id2 = random.sample(significant_persons, 1)[0]
    docdistances.append(cosine(charsrelative2docs[id1], charsrelative2docs[id2]))
    worlddistances.append(cosine(charsrelative2world[id1], charsrelative2world[id2]))

adjmean = np.mean(docdistances)
normmean = np.mean(worlddistances)
print(10000 * adjmean, 10000 * normmean, normmean/adjmean)

right = 0
wrong = 0
cosright = 0
coswrong = 0
answers = []

def smart_cosine(char1, char2):
    global charsrelative2world, charsrelative2docs, meta

    doc1 = getdoc(char1)
    doc2 = getdoc(char2)

    auth1 = meta.loc[doc1, 'author']
    auth2 = meta.loc[doc2, 'author']

    if doc1 != doc2 and auth1 != auth2:
        norm1 = charsrelative2world[char1]
        norm2 = charsrelative2world[char2]
        comparison = cosine(norm1, norm2)
    else:
        adj1 = charsrelative2docs[char1]
        adj2 = charsrelative2docs[char2]
        comparison = cosine(adj1, adj2)

    return comparison

for h in hypotheses:

    first = charsrelative2world[h['firstsim']]
    second = charsrelative2world[h['secondsim']]
    distract = charsrelative2world[h['distractor']]

    pair_euclid = euclidean(first, second)
    pair_cos = smart_cosine(h['firstsim'], h['secondsim'])

    # first comparison

    distraction1 = euclidean(first, distract)
    distraction1cos = smart_cosine(h['firstsim'], h['distractor'])

    if distraction1 < pair_euclid:
        wrong += 1
    else:
        right += 1

    if distraction1cos < pair_cos:
        coswrong += 1
        answers.append([h['hypothesisnum'], h['secondsim'], h['firstsim'], h['distractor'], 'wrong'])
    else:
        answers.append([h['hypothesisnum'], h['secondsim'], h['firstsim'], h['distractor'], 'right'])
        cosright += 1

    # second comparison

    distraction2 = euclidean(second, distract)
    distraction2cos = smart_cosine(h['secondsim'], h['distractor'])

    if distraction2 < pair_euclid:
        wrong += 1
    else:
        right += 1

    if distraction1cos < pair_cos:
        coswrong += 1
        answers.append([h['hypothesisnum'], h['firstsim'], h['secondsim'], h['distractor'], 'wrong'])
    else:
        cosright += 1
        answers.append([h['hypothesisnum'], h['firstsim'], h['secondsim'], h['distractor'], 'right'])

print('Euclid: ', right / (wrong + right))
print('Cosine: ', cosright / (coswrong + cosright))

user = input('Write to file? ')
if len(user) > 1:
    outpath = 'answers/' + user + '.tsv'
    with open(outpath, mode = 'w', encoding = 'utf-8') as f:
        f.write('index\tcomparand\thinge\tdistractor\tanswer\n')
        for a in answers:
            f.write('\t'.join(a) + '\n')








