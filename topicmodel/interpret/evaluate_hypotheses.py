# evaluate_hypotheses.py

# This script evaluates our preregistered hypotheses using
# the doctopics file produced by MALLET.

import sys, csv
import numpy as np
from scipy.spatial.distance import euclidean, cosine
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

    '''
    We know whether the model got this hypothesis wrong or right.
    Now, using the hypothesis-index (just its number in the list
    of hypotheses), we want to assign credit or blame to the relevant
    class of hypotheses.
    '''

    hypidx = int(hypidx)

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

# MAIN starts here

args = sys.argv

doctopic_path = args[1]

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
cosright = 0
coswrong = 0
answers = []

social = Counter()
structural = Counter()
selfcomp = Counter()

missing = set()

for s in significant_persons:
    if s not in chardict:
        print(s)
        missing.add(s)


for idx, h in enumerate(hypotheses):

    skip = False
    ids = [h['firstsim'], h['secondsim'], h['distractor']]
    hypothesisnum = h['hypothesisnum']

    for anid in ids:
        if anid in missing:
            skip = True
    if skip:
        continue

    first = chardict[h['firstsim']]
    second = chardict[h['secondsim']]
    distract = chardict[h['distractor']]

    pair_euclid = euclidean(first, second)
    pair_cos = cosine(first, second)

    # first comparison

    distraction1 = euclidean(first, distract)
    distraction1cos = cosine(first, distract)

    if distraction1 < pair_euclid:
        wrong += 1
    else:
        right += 1

    if distraction1cos < pair_cos:
        coswrong += 1
        understand_why(selfcomp, social, structural, hypothesisnum, 'wrong')
    elif distraction1cos == pair_cos:
        print('error')
    else:
        understand_why(selfcomp, social, structural, hypothesisnum, 'right')
        cosright += 1

    # second comparison

    distraction2 = euclidean(second, distract)
    distraction2cos = cosine(second, distract)

    if distraction2 < pair_euclid:
        wrong += 1
    else:
        right += 1

    if distraction2cos < pair_cos:
        coswrong += 1
        understand_why(selfcomp, social, structural, hypothesisnum, 'wrong')
    elif distraction2cos == pair_cos:
        print('error')
    else:
        cosright += 1
        understand_why(selfcomp, social, structural, hypothesisnum, 'right')

print('Euclid: ', right / (wrong + right))
print('Cosine: ', cosright / (coswrong + cosright))

selftotal = selfcomp['right'] / (selfcomp['wrong'] + selfcomp['right'])
soctotal = social['right'] / (social['wrong'] + social['right'])
structotal = structural['right'] / (structural['wrong'] + structural['right'])
print()
print('Cosine on self-comparisons: ', selftotal)
print('Cosine on social comparisons: ', soctotal)
print('Cosine on structural comparisons: ', structotal)

# user = input('Write to file? ')
# if len(user) > 1:
#     outpath = 'answers/' + user + '.tsv'
#     with open(outpath, mode = 'w', encoding = 'utf-8') as f:
#         f.write('index\tcomparand\thinge\tdistractor\tanswer\n')
#         for a in answers:
#             f.write('\t'.join(a) + '\n')








