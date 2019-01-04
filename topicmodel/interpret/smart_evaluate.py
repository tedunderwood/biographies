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

print()
print('Reading characters and building doc centroids.')

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

right = 0
wrong = 0
answers = []

def checksame(hypothesis):
    '''
    If two of the characters have the same docid,
    this returns True.
    '''
    c1 = hypothesis['firstsim']
    c2 = hypothesis['secondsim']
    c3 = hypothesis['distractor']

    doc1 = getdoc(c1)
    doc2 = getdoc(c2)
    doc3 = getdoc(c3)

    if doc1 == doc2:
        return True
    elif doc2 == doc3:
        return True
    elif doc3 == doc1:
        return True
    else:
        return False

def smart_cosine(char1, char2, flagsame):
    global charsrelative2docs, meta, rawchars

    #doc1 = getdoc(char1)
    #doc2 = getdoc(char2)

    if flagsame:
        vec1 = charsrelative2docs[char1]
        vec2 = charsrelative2docs[char2]

    else:
        vec1 = rawchars[char1]
        vec2 = rawchars[char2]

    return cosine(vec1, vec2)

def fair_cosine(char1, char2):
    global charsrelative2docs, meta, rawchars

    vec1 = np.append(charsrelative2docs[char1] * 1.2, rawchars[char1])
    vec2 = np.append(charsrelative2docs[char2] * 1.2, rawchars[char2])

    return cosine(vec1, vec2)

for h in hypotheses:

    samedocs = checksame(h)
    pair_cos = smart_cosine(h['firstsim'], h['secondsim'], samedocs)

    # first comparison

    distraction1cos = smart_cosine(h['firstsim'], h['distractor'], samedocs)

    if distraction1cos < pair_cos:
        wrong += 1
        answers.append([h['hypothesisnum'], h['secondsim'], h['firstsim'], h['distractor'], 'wrong'])
    else:
        answers.append([h['hypothesisnum'], h['secondsim'], h['firstsim'], h['distractor'], 'right'])
        right += 1

    # second comparison

    distraction2cos = smart_cosine(h['secondsim'], h['distractor'], samedocs)

    if distraction2cos < pair_cos:
        wrong += 1
        answers.append([h['hypothesisnum'], h['firstsim'], h['secondsim'], h['distractor'], 'wrong'])
    else:
        right += 1
        answers.append([h['hypothesisnum'], h['firstsim'], h['secondsim'], h['distractor'], 'right'])

print('Cosine: ', right / (wrong + right))

user = input('Write to file? ')
if len(user) > 1:
    outpath = 'answers/' + user + '.tsv'
    with open(outpath, mode = 'w', encoding = 'utf-8') as f:
        f.write('index\tcomparand\thinge\tdistractor\tanswer\n')
        for a in answers:
            f.write('\t'.join(a) + '\n')








