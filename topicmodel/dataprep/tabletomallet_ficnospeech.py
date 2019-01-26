#!/usr/bin/env python3

# tabletomallet_ficnospeech.py

# This script selects & prepares data for use by MALLET. It starts from the
# tabular data produced by jsontotable5.py, and slightly changes format.
# More importantly, it selects volumes distributed as evenly as possible across
# time, and ensures that the volumes for all our preregistered hypotheses
# will be present.

# This particular variant of tabletomallet has been edited to remove
# dialogue from the data.

import csv, random, sys

# Our general strategy is to take 1000 books from each decade between the 1780s
# and the 2000s (where 1000 books are available, which they aren't until the 1850s).
# So we start by organizing books by decade:

decades = dict()
for floor in range(1780, 2010, 10):
    decades[floor] = set()

with open('../../metadata/filtered_fiction_plus_18c.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        # there are two different forms of id volumes can have,
        # because 19c stories are often multi-volume
        # and so I assigned them new docids

        inferreddate = int(row['inferreddate'])
        decfloor = 10 * (inferreddate // 10)
        docid = row['docid']

        if decfloor in decades:
            decades[decfloor].add(docid)

# Then sample 1000 from each decade.

randomsample = set()

for floor, available in decades.items():
    if len(available) < 1000:
        k = len(available)
        print(floor, k)
    else:
        k = 1000
    selected = random.sample(available, k)
    randomsample = randomsample.union(selected)

# We also want to ensure that we have all the books needed to test preregistered hypotheses.
# So let's add those too.

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

specialids = set()

with open('../../evaluation/hypotheses.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        ids = [row['firstsim'], row['secondsim'], row['distractor']]
        for anid in ids:
            docid = getdoc(anid)
            specialids.add(docid)

# In addition, there are a few characters who are known to be split across a couple
# different names. We're going to unify these in data prep.

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

print('Translator for ', len(char_translator))

sources = ['/Users/tunder/data/character_table_18c19c.tsv',
    '/Users/tunder/data/character_table_post1900.tsv']

malletout = '/Users/tunder/data/malletficnospeech.txt'

errors = 0
errorset = {}

lines = []
special_lines = []

wordholding = dict()
labelholding = dict()

linecount = 0

for s in sources:
    with open(s, encoding = 'utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            docid = fields[0]
            if docid in randomsample or docid in specialids:
                charid = fields[2]
                date = fields[4]
                gender = fields[3]
                words = [x for x in fields[5].split() if not x.startswith('said-')]
                label = 'fic' + date + gender

                if charid in char_translator or charid in to_supplement:

                    if charid in char_translator:
                        hold_id = char_translator[charid]
                    else:
                        hold_id = charid

                    if hold_id not in wordholding:
                        wordholding[hold_id] = []
                    wordholding[hold_id].extend(words)
                    labelholding[hold_id] = label

                else:
                    outline = ' '.join([charid, label, ' '.join(words)]) + '\n'
                    if docid in specialids:
                        special_lines.append(outline)
                    else:
                        lines.append(outline)

            if len(lines) > 1000:
                with open(malletout, mode = 'a', encoding = 'utf-8') as f:
                    for l in lines:
                        f.write(l)
                        linecount += 1
                lines = []

for anid in to_supplement:
    outline = ' '.join([anid, labelholding[anid], ' '.join(wordholding[anid])]) + '\n'
    special_lines.append(outline)

with open(malletout, mode = 'a', encoding = 'utf-8') as f:
    for l in special_lines:
        f.write(l)
        linecount += 1

print("Total volumes: ", len(randomsample) + len(specialids))
print("Total chars: ", linecount)





