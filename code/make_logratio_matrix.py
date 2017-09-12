# Make logratio matrix.

# USAGE:

# python3 make_logratio_matrix.py name_of_outfile pathtodata1 pathtodata2 etc

# this is written to produce
# a matrix of Laplace-smoothed log ratios; i.e.,
# log( (word_uses_for_women + 1 / all_words_for_women) / (word_uses_for_men + 1 / all_words_for_men) )

VOCABLENGTH = 6000

import csv, sys, os
import numpy as np
import pandas as pd
import math
# from random import shuffle
# from random import random as randomprob
from sklearn.linear_model import LinearRegression
from collections import Counter

csv.field_size_limit(sys.maxsize)

arguments = sys.argv

out_filename = arguments[1]
if os.path.isfile(out_filename + '.csv'):
    print(out_filename + ' already exists, and I refuse to overwrite it.')

files_to_use = []
for f in arguments[2:]:
    if os.path.isfile(f):
        files_to_use.append(f)
    else:
        print("Cannot find " + f)

# Let's load some metadata about the publication dates of these works,
# and the inferred genders of their authors.

personalnames = set()
with open("../lexicons/PersonalNames.txt", encoding="utf-8") as f:
    names = f.readlines()

for line in names:
    name = line.rstrip()
    personalnames.add(name)
    personalnames.add('said-' + name)

vocab = Counter()

def add2vocab(vocab, filepath):
    with open(filepath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        for row in reader:
            if 'chargender' in row:
                gender = row['chargender']
            else:
                gender = row['gender']

            if gender.startswith('u'):
                continue
            words = row['words'].split()
            for w in words:
                if not w.startswith('said-') and w not in personalnames:
                    vocab[w] += 1

# Let's create the vocabulary.

for f in files_to_use:
    add2vocab(vocab, f)

vocabcount = len(vocab)
print("The data includes " + str(vocabcount) + " words")

wordsinorder = [x[0] for x in vocab.most_common(VOCABLENGTH)]

vocabulary = dict()
vocabset = set()

for idx, word in enumerate(wordsinorder):
    vocabulary[word] = idx
    vocabset.add(word)
print("Vocabulary sorted, top " + str(VOCABLENGTH) + " kept.")


vecbyyear = dict()
vecbyyear['m'] = dict()
vecbyyear['f'] = dict()
datevector = list(range(1780, 2008))

for g in ['f', 'm']:
    for i in range(1780, 2008):
        vecbyyear[g][i] = np.zeros((VOCABLENGTH))

def add2counts(vecbyyear, path):
    with open(path, encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        for row in reader:
            if 'chargender' in row:
                gender = row['chargender']
            else:
                gender = row['gender']

            if gender.startswith('u'):
                continue

            date = int(row['pubdate'])
            if date < 1780 or date > 2008:
                continue

            words = row['words'].split()
            for w in words:
                if w in vocabset:
                    idx = vocabulary[w]
                    np.add.at(vecbyyear[gender][date], idx, 1)

# Let's actually count words.

for f in files_to_use:
    add2counts(vecbyyear, f)

def dunnings(vectora, vectorb):
    assert len(vectora) == len(vectorb)
    veclen = len(vectora)
    totala = np.sum(vectora)
    totalb = np.sum(vectorb)
    totalboth = totala + totalb

    dunningvector = np.zeros(veclen)

    for i in range(veclen):
        if vectora[i] == 0 or vectorb[i] == 0:
            continue
            # Cause you know you're going to get div0 errors.

        try:
            probI = (vectora[i] + vectorb[i]) / totalboth
            probnotI = 1 - probI
            expectedIA = totala * probI
            expectedIB = totalb * probI
            expectedNotIA = totala * probnotI
            expectedNotIB = totalb * probnotI
            expected_table = np.array([[expectedIA, expectedNotIA],
                [expectedIB, expectedNotIB]])
            actual_table = np.array([[vectora[i], (totala - vectora[i])],
                [vectorb[i], (totalb - vectorb[i])]])
            G = np.sum(actual_table * np.log(actual_table / expected_table))

            # We're going to use a signed version of Dunnings, so features where
            # B is higher than expected will be negative.

            if expectedIB > vectorb[i]:
                G = -G

            dunningvector[i] = G

        except:
            pass
            # There are a million ways to get a div-by-zero or log-zero error
            # in that calculation. I could check them all, or just do this.
            # The vector was initialized with zeroes, which are the default
            # value I want for failed calculations anyhow.

    return dunningvector

def pure_rank_matrix(femalevectorsbyyear, malevectorsbyyear, datevector):
    rankmatrix = []
    magnitudematrix = []

    for i in datevector:
        d = dunnings(femalevectorsbyyear[i], malevectorsbyyear[i])

        # transform this into a nonparametric ranking
        decorated = [x for x in zip(d, [x for x in range(len(d))])]
        decorated.sort()

        negativeidx = -sum(d < 0)
        positiveidx = 1

        numzeros = sum(d == 0)

        ranking = np.zeros(len(d))
        for dvalue, index in decorated:
            # to understand what follows, it's crucial to remember that
            # we're iterating through decorated in dvalue order

            if dvalue < 0:
                ranking[index] = negativeidx
                negativeidx += 1
            elif dvalue > 0:
                ranking[index] = positiveidx
                positiveidx += 1
            else:
                # dvalue is zero
                pass

        checkzeros = sum(ranking == 0)
        if numzeros != checkzeros:
            print('error in number of zeros')


        rawmagnitude = femalevectorsbyyear[i] + malevectorsbyyear[i]
        normalizedmagnitude = rawmagnitude / np.sum(rawmagnitude)
        assert len(ranking) == len(normalizedmagnitude)
        rank_adjusted_by_magnitude = ranking * normalizedmagnitude

        rankmatrix.append(ranking)
        magnitudematrix.append(rank_adjusted_by_magnitude)

    return np.array(magnitudematrix), np.array(rankmatrix)

def diff_proportion(vecbyyear, datevector):
    diffmatrix = []

    for yr in datevector:
        if np.sum(vecbyyear['m'][yr]) == 0:
            mvec = np.full(len(vecbyyear['m'][yr]), 0)
        else:
            mvec = (vecbyyear['m'][yr] * 5000) / np.sum(vecbyyear['m'][yr])

        if np.sum(vecbyyear['f'][yr]) == 0:
            fvec = np.full(len(vecbyyear['f'][yr]), 0)
        else:
            fvec = (vecbyyear['f'][yr] * 5000) / np.sum(vecbyyear['f'][yr])

        dvec = fvec - mvec
        diffmatrix.append(dvec)

    return np.array(diffmatrix)

def log_ratios(vecbyyear, datevector):

    diffmatrix = []

    for yr in datevector:

        # We add one to all the word counts;
        # let's call that Laplacian smoothing.
        # It has the effect of getting rid of
        # nan values, in a way that I think is relatively
        # principled: it will tend to move
        # infrequent words toward the origin.

        vecbyyear['m'][yr] = vecbyyear['m'][yr] + 1
        mvec = vecbyyear['m'][yr] / np.sum(vecbyyear['m'][yr])


        vecbyyear['f'][yr] = vecbyyear['f'][yr] + 1
        fvec = vecbyyear['f'][yr] / np.sum(vecbyyear['f'][yr])

        ratios = fvec / mvec

        log_ratios = np.log(ratios)

        diffmatrix.append(log_ratios)

    return np.array(diffmatrix)

diffmatrix = log_ratios(vecbyyear, datevector)

def writematrix(amatrix, outpath):
    global wordsinorder, datevector

    with open(outpath, mode = 'w', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['thedate'] + wordsinorder)
        for i, date in enumerate(datevector):
            writer.writerow(np.insert(amatrix[i, : ], 0, date))

writematrix(diffmatrix, '../data/' + out_filename + '.csv')

print('Linear regression to infer slopes.')
datevector = np.array(datevector)
outrows = []
for i in range(VOCABLENGTH):
    thiscolumn = diffmatrix[ : , [i]]
    # note: the brackets around i extract it as a *column* rather than row

    notmissing = thiscolumn != 0
    # still a column

    y = thiscolumn[notmissing].transpose()

    # that's a cheap hack to create an array w/ more than one column,
    # which the linear regression seems to want

    x = datevector[notmissing.transpose()[0]]
    # We have to transpose the column "notmissing" to index a row.

    x = x[ : , np.newaxis]
    # Then we have to make x a row of an array with two
    # dimensions (even though it only has one row).

    vectorlen = len(x)

    word = wordsinorder[i]

    model = LinearRegression()

    model.fit(x, y)
    slope = model.coef_[0]
    intercept = model.intercept_
    standard_deviation = np.std(y)

    nineteenth = np.mean(thiscolumn[0:120])
    twentieth =np.mean(thiscolumn[120:])
    change = twentieth - nineteenth

    approachmid = abs(np.nanmean(thiscolumn[0:60])) - abs(np.nanmean(thiscolumn[150:210]))
    approachstd = approachmid / standard_deviation

    # note that it's important we use thiscolumn rather than y here, because y has been reduced
    # in length

    out = dict()
    out['word'] = word
    out['slope'] = slope
    out['mean'] = np.mean(thiscolumn)
    out['intercept'] = intercept
    out['change'] = change
    out['approachmid'] = approachmid
    out['approachstd'] = approachstd
    outrows.append(out)

with open('../data/' + out_filename + '.slopes.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = ['word', 'slope', 'mean', 'intercept', 'change', 'approachmid', 'approachstd'])
    writer.writeheader()
    for row in outrows:
        writer.writerow(row)







