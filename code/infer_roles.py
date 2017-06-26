# infer_roles.py

# Character role inference based on the assumption that
# a single work is unlikely to include multiple characters
# occupying the same role.

# we implement that very simply by postulating that the chance
# a word in type w, character c, book b belongs to role r is proportional to

# (fraction of r that is w + alpha) * (number of role r in c + beta) 
#          divided by
#  (fraction of other words in b that belong to r + gamma)

# where alpha, beta, gamma are blurriness constants,
# and we expect gamma to be pretty high, like 0.05

import gzip, json, random, bisect

import pandas as pd 
import numpy as np 
from collections import Counter

stopwords = set()
stoppath = '/Users/tunder/Documents/TextAnalysisWithR/tedstopwords.txt'
with open(stoppath, encoding = 'utf-8') as f:
    for line in f:
        stopwords.add(line.lower().strip())

morestops = {'just', 'right', 'mr', 'mr.'}
for stop in morestops:
    stopwords.add(stop)

def get_vocab(tarpath, stopwords, v):
    vocab = Counter()

    characters = dict()
    charctr = 0

    books = dict()
    bookctr = 0

    specialstopwords = {'said', 'had', 'was', 'is', 'says'}

    with gzip.open(tarpath, mode = 'rt') as f:
        ctr = 0
        for line in f:
            ctr += 1
            jobj = json.loads(line)
            theid = jobj['id']
            if theid in books:
                print('duplicate book')
            else:
                books[theid] = bookctr
                thisbook = bookctr
                bookctr += 1

            if bookctr > 300:
                break

            for c in jobj['characters']:
                if 'g' not in c:
                    continue

                gender = c['g']
                if gender not in {0, 1, 2}:
                    continue
                else:
                    pass

                names = c['names']
                maxname = ''
                maxlen = 0
                for n in names:
                    thisname = n['n']
                    thislen = len(thisname)
                    if thislen > maxlen:
                        maxname = thisname.replace(' ', '_')

                thischarwords = 0

                for role in ['agent', 'mod', 'patient', 'poss']:
                    if role in c:
                        for w in c[role]:
                            word = w['w'].lower()

                            if word in specialstopwords or word.startswith("'"):
                                continue
                            if len(word) < 1:
                                continue
                            if not word[0].isalpha():
                                continue

                            if role == 'patient':
                                word = 'was ' + word
                            vocab[word] += 1
                            thischarwords += 1

                for spoken in c['speaking']:
                    wstring = spoken['w'].lower().split()
                    for w in wstring:
                        if w in stopwords or w == "n't" or w == 'ca':
                            continue
                        if len(w) > 0 and w[0].isalpha():
                            word = 'said ' + w
                            vocab[word] += 1
                            thischarwords += 1

                if thischarwords < 11:
                    continue
                else:
                    charactername = theid + '_' + maxname
                    if charactername in characters:
                        print('charactererror ' + charactername)
                    else:
                        newfound = True
                        characters[charactername] = charctr
                        charctr += 1

    selected_vocab = vocab.most_common(v)
    with open('selectedvocab.txt', mode = 'w', encoding = 'utf-8') as f:
        for a, b in selected_vocab:
            f.write(str(a) + "\t" + str(b) + '\n')

    vocabulary_list = [x[0] for x in selected_vocab]
    lexicon = dict()
    for idx, val in enumerate(vocabulary_list):
        lexicon[val] = idx

    return vocabulary_list, lexicon, characters, books

def get_characters(tarpath, lexicon, characters, books, k):

    wtypecol = []
    charcol = []
    bookcol = []
    topiccol = []

    wordtopics = dict()
    chartopics = dict()
    booktopics = dict()

    chargenders = dict()

    for w, idx in lexicon.items():
        wordtopics[idx] = np.zeros(k)

    topicroulette = [x for x in range(k)]
    charctr = 0
    with gzip.open(tarpath, mode = 'rt') as f:
        ctr = 0
        for line in f:
            if ctr % 100 == 0:
                print(ctr)
            ctr += 1
            if ctr > 50:
                break
            jobj = json.loads(line)
            theid = jobj['id']
            if theid in books:
                bookid = books[theid]
                bookdist = np.zeros(k)
            else:
                print('bookerror')

            for c in jobj['characters']:

                names = c['names']
                maxname = ''
                maxlen = 0
                for n in names:
                    thisname = n['n']
                    thislen = len(thisname)
                    if thislen > maxlen:
                        maxname = thisname.replace(' ', '_')

                charactername = theid + '_' + maxname

                if charactername not in characters:
                    continue
                else:
                    charctr += 1
                    if charctr % 100 == 2:
                        print(charctr)

                charid = characters[charactername]
                chardist = np.zeros(k)    

                for role in ['agent', 'mod', 'patient', 'poss']:
                    if role in c:
                        for w in c[role]:
                            word = w['w'].lower()
                            if role == 'patient':
                                word = 'was ' + word
                            if word not in lexicon:
                                continue
                            else:
                                wordid = lexicon[word]
                                randomtopic = random.sample(topicroulette, 1)[0]

                                wtypecol.append(wordid)
                                charcol.append(charid)
                                bookcol.append(bookid)
                                topiccol.append(randomtopic)

                                bookdist[randomtopic] += 1
                                chardist[randomtopic] += 1
                                wordtopics[wordid][randomtopic] += 1
                

                for spoken in c['speaking']:
                    wstring = spoken['w'].lower().split()
                    for w in wstring:
                        if len(w) > 0 and w[0].isalpha():
                            word = 'said ' + w
                            if word not in lexicon:
                                continue
                            else:
                                wordid = lexicon[word]

                                randomtopic = random.sample(topicroulette, 1)[0]

                                wtypecol.append(wordid)
                                charcol.append(charid)
                                bookcol.append(bookid)
                                topiccol.append(randomtopic)

                                bookdist[randomtopic] += 1
                                chardist[randomtopic] += 1
                                wordtopics[wordid][randomtopic] += 1

                chartopics[charid] = chardist

            booktopics[bookid] = bookdist


    td = dict()

    td['wordtype'] = wtypecol
    td['chartype'] = charcol
    td['booktype'] = bookcol
    td['topic'] = topiccol

    tokens = pd.DataFrame(td)
    wordtopics = pd.DataFrame(wordtopics)

    return tokens, wordtopics, chartopics, booktopics, chargenders

def onesample(tokens, wordtopics, chartopics, booktopics, booktotals, constants):
    k, alpha, beta, gamma = constants

    topictotals = dict()
    for r in range(k):
        topictotals[r] = sum(wordtopics.loc[r, :])

    for i in tokens.index:
        if i % 1000 == 1:
            print(i)
        w = tokens.loc[i, 'wordtype']
        c = tokens.loc[i, 'chartype']
        b = tokens.loc[i, 'booktype']
        z = tokens.loc[i, 'topic']

        # pop token off counts, so its current assignment doesn't
        # affect its own probability of assignment to different
        # topics

        wordtopics.loc[z, w] = wordtopics.loc[z, w] - 1
        chartopics[c][z] = chartopics[c][z] - 1
        booktopics[b][z] = booktopics[b][z] - 1
        topictotals[z] = topictotals[z] - 1

        # create a continuum with spaces proportional
        # to topic probabilities
        cutpoints = []
        lastcut = 0

        for r in range(k):
            totalwordsinr = topictotals[r]
            thiswordinr = wordtopics.loc[r, w]
            wfractionofr = thiswordinr / (totalwordsinr + 0.1)
            rinc = chartopics[c][r]
            rinb = booktopics[b][r]
            relsewhereinb = (rinb - rinc) / booktotals[b]

            probability = ((wfractionofr + alpha) * (rinc + beta)) / (relsewhereinb + gamma)
            if probability <= 0:
                print('subzeroerror')
                probability = 0.000000001
                if totalwordsinr < 0:
                    print('totalwordsinr')
                elif rinc < 0:
                    print('rinc')
                elif thiswordinr < 0:
                    print('thiswordinr')
            lastcut = lastcut + probability
            cutpoints.append(lastcut)

        random_real = random.uniform(0, lastcut)
        # the new topic is the insertion point for this random real in the sequence
        newtopic = bisect.bisect_left(cutpoints, random_real)

        if newtopic < 0:
            print('Undershot error')
            newtopic = 0
        if newtopic >= k:
            print('Overshot error')
            newtopic = k - 1

        tokens.loc[i, 'topic'] = newtopic

        # add this token back to the counters
        wordtopics.loc[newtopic, w] = wordtopics.loc[newtopic, w] + 1
        chartopics[c][newtopic] = chartopics[c][newtopic] + 1
        booktopics[b][newtopic] = booktopics[b][newtopic] + 1
        topictotals[newtopic] = topictotals[newtopic] + 1

def print_topicwords(wordtopics, r, vocabulary_list):
    alltopiccounts = list(wordtopics.loc[r, : ])
    decorated = [x for x in zip(alltopiccounts, vocabulary_list)]
    decorated.sort(reverse = True)
    top5 = [x[1] for x in decorated[0: 10]]
    line = str(r) + ': '
    for word in top5:
        line = line + word + ' | '
    print(line)

if __name__ == '__main__':
    k = 20
    v = 20000
    # k is the number of topics; v the vocab size
    alpha = 1/v 
    beta = 0.06
    gamma = 0.2
    constants = (k, alpha, beta, gamma)
    tarpath = '/Users/tunder/Dropbox/genderdata/rawjsons/chicago.json.gz'

    vocabulary_list, lexicon, characters, books = get_vocab(tarpath, stopwords, v)
    tokens, wordtopics, chartopics, booktopics, chargenders = get_characters(tarpath, lexicon, characters, books, k)

    for character, topicdist in chartopics.items():
        for r in range(k):
            topicdist[r] = tokens[(tokens['chartype'] == character) & (tokens['topic'] == r)].count()[0]
    
    booktotals = dict()
    for bookid, bookidx in books.items():
        booktotals[bookidx] = tokens[tokens['booktype'] == bookidx].count()[0]

    for iteration in range(40):
        print("ITERATION: " + str(iteration))
        for r in range(k):
            print_topicwords(wordtopics, r, vocabulary_list)
        print()
        onesample(tokens, wordtopics, chartopics, booktopics, booktotals, constants)





