# autosmartevaluate_rolethemes.py

# This is an automatable version of
# smartevaluate_rolethemes.py, that
# can be called as a function from
# measure_variation.py.

import sys, csv, random
import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine
from collections import Counter

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

def understand_why(selfcomp, social, structural, hypidx, whethercorrect):
        if hypidx <= 6:
            selfcomp[whethercorrect] += 1
        if hypidx >= 7 and hypidx <= 46:
            structural[whethercorrect] += 1
        elif hypidx >= 47 and hypidx <= 56:
            social[whethercorrect] += 1
        elif hypidx >= 57 and hypidx <= 73:
            structural[whethercorrect] += 1
        elif hypidx >= 74 and hypidx <= 84:
            social[whethercorrect] += 1
        elif hypidx == 85 or hypidx == 86:
            structural[whethercorrect] += 1
        elif hypidx >= 87 and hypidx <= 92:
            social[whethercorrect] += 1
        elif hypidx >= 93:
            selfcomp[whethercorrect] += 1

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

def smart_cosine(char1, char2, charsrelative2docs, rawchars):

    doc1 = getdoc(char1)
    doc2 = getdoc(char2)

    if doc1 == doc2:
        vec1 = charsrelative2docs[char1]
        vec2 = charsrelative2docs[char2]

    else:
        vec1 = rawchars[char1]
        vec2 = rawchars[char2]

    return cosine(vec1, vec2)

def smarteval_a_model(doctopicpath, numthemes):

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

    # adjust the rawchars for docs

    charsrelative2docs = dict()

    for charid, vector in rawchars.items():
        charsrelative2docs[charid] = vector[numthemes : ]

    right = 0
    wrong = 0
    answers = []

    selfcomp = Counter()
    social = Counter()
    structural = Counter()

    for h in hypotheses:

        pair_cos = smart_cosine(h['firstsim'], h['secondsim'], charsrelative2docs, rawchars)

        # first comparison

        distraction1cos = smart_cosine(h['firstsim'], h['distractor'], charsrelative2docs, rawchars)

        if distraction1cos < pair_cos:
            wrong += 1
            understand_why(selfcomp, social, structural, hypothesisnum, 'wrong')
        else:
            understand_why(selfcomp, social, structural, hypothesisnum, 'right')
            right += 1

        # second comparison

        distraction2cos = smart_cosine(h['secondsim'], h['distractor'], charsrelative2docs, rawchars)

        if distraction2cos < pair_cos:
            wrong += 1
            understand_why(selfcomp, social, structural, hypothesisnum, 'wrong')
        else:
            right += 1
            understand_why(selfcomp, social, structural, hypothesisnum, 'right')

    print('Smart cosine: ', right / (wrong + right))

    return total, selftotal, soctotal, structotal








