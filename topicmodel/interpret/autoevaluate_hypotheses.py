# evaluate_hypotheses.py

# This script evaluates our preregistered hypotheses using
# the doctopics file produced by MALLET.

# This version of evaluate_hypotheses is redesigned to permit
# being called repeatedly as a function from measure_variation.

import sys, csv
import numpy as np
from scipy.spatial.distance import cosine
from collections import Counter

def getdoc(anid):
    '''
    Gets the docid part of a character id
    '''

    if '|' in anid:
        thedoc = anid.split('|')[0]
    elif '_' in anid:
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


def evaluate_a_model(doctopic_path):

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

    with open(doctopic_path, encoding = 'utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            charid = fields[1]
            if charid not in significant_persons:
                continue
            else:
                vector = np.array(fields[2 : ], dtype = 'float32')
                veclen = len(vector)
                if numtopics == 0:
                    numtopics = veclen
                elif numtopics != veclen:
                    print('error: should not change once set')
                chardict[charid] = vector

    right = 0
    wrong = 0
    answers = []
    social = Counter()
    structural = Counter()
    selfcomp = Counter()

    for idx, h in enumerate(hypotheses):

        skip = False
        ids = [h['firstsim'], h['secondsim'], h['distractor']]

        first = chardict[h['firstsim']]
        second = chardict[h['secondsim']]
        distract = chardict[h['distractor']]
        hypothesisnum = h['hypothesisnum']

        pair_cos = cosine(first, second)

        # first comparison

        distraction1cos = cosine(first, distract)

        if distraction1cos < pair_cos:
            wrong += 1
            understand_why(selfcomp, social, structural, hypothesisnum, 'wrong')

        elif distraction1cos == pair_cos:
            print('error')

        else:
            right += 1
            understand_why(selfcomp, social, structural, hypothesisnum, 'right')

        # second comparison

        distraction2cos = cosine(second, distract)

        if distraction2cos < pair_cos:
            wrong += 1
            understand_why(selfcomp, social, structural, hypothesisnum, 'wrong')

        elif distraction2cos == pair_cos:
            print('error')

        else:
            right += 1
            understand_why(selfcomp, social, structural, hypothesisnum, 'right')


    print('Cosine: ', right / (wrong + right))

    total = right / (wrong + right)
    selftotal = selfcomp['right'] / (selfcomp['wrong'] + selfcomp['right'])
    soctotal = social['right'] / (social['wrong'] + social['right'])
    structotal = structural['right'] / (structural['wrong'] + structural['right'])

    return total, selftotal, soctotal, structotal








