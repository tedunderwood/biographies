# evaluate_hypotheses.py

# This script evaluates our preregistered hypotheses using
# the doctopics file produced by MALLET.

# This version of evaluate_hypotheses is redesigned to permit
# being called repeatedly as a function from measure_variation.

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
        thedoc = anid.split('|')[0]
    else:
        print('error', anid)
        thedoc = anid

    return thedoc

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

    for idx, h in enumerate(hypotheses):

        skip = False
        ids = [h['firstsim'], h['secondsim'], h['distractor']]

        first = chardict[h['firstsim']]
        second = chardict[h['secondsim']]
        distract = chardict[h['distractor']]

        pair_cos = cosine(first, second)

        # first comparison

        distraction1cos = cosine(first, distract)

        if distraction1cos < pair_cos:
            wrong += 1
            answers.append([h['hypothesisnum'], h['secondsim'], h['firstsim'], h['distractor'], 'wrong'])
        elif distraction1cos == pair_cos:
            print('error')
            answers.append([h['hypothesisnum'], h['secondsim'], h['firstsim'], h['distractor'], 'error'])
        else:
            answers.append([h['hypothesisnum'], h['secondsim'], h['firstsim'], h['distractor'], 'right'])
            right += 1

        # second comparison

        distraction2cos = cosine(second, distract)

        if distraction2cos < pair_cos:
            wrong += 1
            answers.append([h['hypothesisnum'], h['firstsim'], h['secondsim'], h['distractor'], 'wrong'])
        elif distraction2cos == pair_cos:
            print('error')
            answers.append([h['hypothesisnum'], h['firstsim'], h['secondsim'], h['distractor'], 'error'])
        else:
            right += 1
            answers.append([h['hypothesisnum'], h['firstsim'], h['secondsim'], h['distractor'], 'right'])

    print('Cosine: ', right / (wrong + right))

    # user = input('Write to file? ')
    # if len(user) > 1:
    #     outpath = 'answers/' + user + '.tsv'
    #     with open(outpath, mode = 'w', encoding = 'utf-8') as f:
    #         f.write('index\tcomparand\thinge\tdistractor\tanswer\n')
    #         for a in answers:
    #             f.write('\t'.join(a) + '\n')








