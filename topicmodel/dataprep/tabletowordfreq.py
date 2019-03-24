#!/usr/bin/env python3

# tabletowordfreq.py

# This script translates character-text into a table of word frequencies
# that can be used by evaluate_hypotheses.

import csv, random, sys, os
from collections import Counter
import numpy as np

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

# First we create a list of the characters we're going to need--
# the ones about which hypotheses have been formulated.

specialids = set()
charstowrite = set()

with open('../../evaluation/hypotheses.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        ids = [row['firstsim'], row['secondsim'], row['distractor']]
        for anid in ids:
            docid = getdoc(anid)
            specialids.add(docid)
            charstowrite.add(anid)

# In addition, there are a few characters who are known to be split across a couple
# different names. We're going to unify these aliases in data prep.

# Our strategy is to create a dictionary that translates the supplemental character
# ids into main character ids. This is only necessary in 15 cases.

char_translator = dict()
to_supplement = set()

with open('../../evaluation/newcharacters.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        supp = row['supplementalcharid']
        if len(supp) > 1:
            char_translator[supp] = row['charid']
            to_supplement.add(row['charid'])

outfile = '../rawwordfreq/wordfreq_vols.tsv'

characters = dict()

with open('/Users/tunder/data/bestfic.txt', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split()
        charid = fields[0]
        thisdoc = getdoc(charid)
        if thisdoc in specialids:
            words = fields[2: ]

            if charid in char_translator or charid in to_supplement:

                if charid in char_translator:
                    hold_id = char_translator[charid]
                else:
                    hold_id = charid

                if hold_id not in characters:
                    characters[hold_id] = []
                characters[hold_id].extend(words)

            else:
                characters[charid] = words

lex = Counter()

for char, words in characters.items():
    for w in set(words):
        lex[w] += 1

vocab = [x[0] for x in lex.most_common(10000)]

vocorder = dict()
for idx, w in enumerate(vocab):
    vocorder[w] = idx

vocablen = len(vocab)
print('Vocabulary of ', vocablen)

charvectors = dict()
for char, words in characters.items():
    vector = np.zeros(vocablen)
    for w in words:
        if w in vocab:
            idx = vocorder[w]
            vector[idx] = vector[idx] + 1
    if np.sum(vector) > 0:
        vector = vector / np.sum(vector)
    charvectors[char] = vector

idx = 0
with open(outfile,mode = 'w', encoding = 'utf-8') as f:
    for char in charstowrite:
        vector = charvectors[char]
        f.write(str(idx) + '\t' + char + '\t' + '\t'.join([str(x) for x in vector]) + '\n')






