#compare_answers.py

import sys, csv
from collections import Counter

firstfile = input('First file? ')
firstfile = 'answers/' + firstfile + '.tsv'
secondfile = input('Second file? ')
secondfile = 'answers/' + secondfile + '.tsv'

def getchar(astring):
    return astring.split('|')[1]

def getdoc(astring):
    return astring.split('|')[0]

def readfile(filepath):
    comparisons = []
    with open(filepath, encoding = 'utf-8') as f:
        for line in f:
            docctr = Counter()
            fields = line.strip().split('\t')
            if fields[0] == 'index':
                continue
            comp = dict()
            comp['idx'] = int(fields[0])
            comp['comparand'] = getchar(fields[1])
            comp['hinge'] = getchar(fields[2])
            comp['distractor'] = getchar(fields[3])
            if fields[4] == 'right':
                comp['ans'] = 1
            else:
                comp['ans'] = 0

            for i in range(2, 4):
                docid = getdoc(fields[i])
                docctr[docid] += 1
            docmax = docctr.most_common(1)[0][1]
            comp['docmax'] = docmax

            comparisons.append(comp)
    return comparisons

first = readfile(firstfile)
second = readfile(secondfile)

bothright = 0
bothwrong = 0
differ = 0
firstwrong = []
secondwrong = []

assert len(first) == len(second)

for i in range(0, len(first)):
    fa = first[i]['ans']
    sa = second[i]['ans']

    if fa == 1 and sa == 1:
        bothright += 1
    elif fa == 0 and sa == 0:
        bothwrong += 1
    elif fa == 1 and sa == 0:
        differ += 1
        secondwrong.append(second[i])
    else:
        differ += 1
        firstwrong.append(first[i])

def outdict(dictionary):
    print('idx\tcomparand\thinge\tdistractor\tdocmax\tanswer')
    for d in dictionary:
        print(str(d['idx']) + '\t' + d['comparand'] + '\t' +
            d['hinge'] + '\t' + d['distractor'] + '\t' +
            str(d['docmax']) + '\t' + str(d['ans']))


print('Both right: ', bothright)
print('Both wrong: ', bothwrong)
print("Differ: ", differ)
print()
print('FIRST WRONG')
outdict(firstwrong)
print()
print('SECOND WRONG')
outdict(secondwrong)


