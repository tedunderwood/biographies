#!/usr/bin/env python3

# basic_character_eda.py

# Adapted from jsontotable5.py, which actually unpacks the
# data in book jsons produced by BookNLP.

# This variant instead produces a table that reveals
# the number of characters per book, and the distribution
# of characters across possible sizes.

import ujson, csv, sys, os

def add_dicts_to_list(alistofdicts, alist, prefix):

    for word in alistofdicts:
        if type(word) == str:
            wordval = word.lower()
        else:
            wordval = word["w"].lower()

        if len(prefix) > 1:
            wordval = prefix + '-' + wordval

        alist.append(wordval)

    return alist

outlist = list()
counter = 0

usedalready = set()

stopwords = set()    # GLOBAL list of stopwords only used to filter dialogue
stoppath = '../lexicons/stopwords.txt'
with open(stoppath, encoding = 'utf-8') as f:
    for line in f:
        stopwords.add(line.lower().strip())

morestops = {'just', 'right', 'mr', 'mr.', "n't", "ca"}
for stop in morestops:
    stopwords.add(stop)

def charlengths(jsonstring):
    ''' Given a single json string produced by BookNLP, this extracts the
    characters, and records their lengths and genders.

    jsonstring: what we will parse'''

    global id2date, unknowndate, stopwords, thingsunknown

    jsonobject = ujson.loads(jsonstring)

    charsizes = []
    dialsizes = []
    chargenders = []

    storyid = jsonobject["id"]

    characterlist = jsonobject["characters"]

    for character in characterlist:

        gender = character["g"]
        if gender == 1:
            genderstring = "f"
        elif gender == 2:
            genderstring = "m"
        else:
            genderstring = 'u'

        chargenders.append(genderstring)

        thesewords = []       # gathering all non-dialogue for this character

        thesewords = add_dicts_to_list(character["agent"], thesewords, '')
        thesewords = add_dicts_to_list(character["poss"], thesewords, '')
        thesewords = add_dicts_to_list(character["mod"], thesewords, '')
        thesewords = add_dicts_to_list(character["patient"], thesewords, 'was')

        nondial = len(thesewords)
        dialogue = []

        for spoken in character["speaking"]:
            if type(spoken) == str:
                wlist = spoken.lower().split()
            else:
                wlist = spoken['w'].lower().split()

            for w in wlist:
                if w in stopwords:
                    continue
                if len(w) > 0 and w[0].isalpha():
                    word = 'said-' + w
                    dialogue.append(word)

        dial = len(dialogue)

        charsizes.append(dial + nondial)
        dialsizes.append(dial)

    return storyid, charsizes, dialsizes, chargenders


def getfolder(folder, outlines):

    sourcefiles = [x for x in os.listdir(folder) if x.endswith('.book')]
    # the data files produced by BookNLP all end with '.book'
    for sf in sourcefiles:
        path = os.path.join(folder, sf)
        with open(path, encoding = 'utf-8') as f:
            jsonstring = f.read()

        expectedid = sf.replace('.book', '')
        storyid, charsizes, dialsizes, chargenders = charlengths(jsonstring)

        for size, dial, g in zip(charsizes, dialsizes, chargenders):
            outline = '\t'.join([storyid, str(size), str(dial), g]) + '\n'
            outlines.append(outline)
    return outlines

## MAIN EXECUTION BEGINS HERE

arguments = sys.argv
datasource = arguments[1]
outfile = arguments[2]

if datasource == 'bio':
    datafolders = ['/projects/ischoolichass/ichass/usesofscale/chardata/post1923bio',
    '/projects/ischoolichass/ichass/usesofscale/chardata/pre1923bio']

    outlines = []

    for folder in datafolders:
        print(folder)
        outlines = getfolder(folder, outlines)

elif datasource == 'fic':

    datafolders = ['/projects/ischoolichass/ichass/usesofscale/chardata/post1923fic']

    outlines = []

    datafiles = ['/projects/ischoolichass/ichass/usesofscale/chardata/pre1923fic/20thc_characters1.json',
    '/projects/ischoolichass/ichass/usesofscale/chardata/pre1923fic/20thc_characters2.json',
    '/projects/ischoolichass/ichass/usesofscale/chardata/pre1923fic/20thc_characters3.json',
    '/projects/ischoolichass/ichass/usesofscale/chardata/pre1923fic/pre1900chars.json']

    for dfile in datafiles:
        assert os.path.isfile(dfile)
        # otherwise we have an error
        print(dfile)

        with open(dfile, encoding = 'utf-8') as f:
            for jsonstring in f:
                storyid, charsizes, dialsizes, chargenders = charlengths(jsonstring)

                for size, dial, g in zip(charsizes, dialsizes, chargenders):
                    outline = '\t'.join([storyid, str(size), str(dial), g]) + '\n'
                    outlines.append(outline)
                    
    for folder in datafolders:
        print(folder)
        outlines = getfolder(folder, outlines)

else:
    print("Usage for basic_character_eda is either:")
    print("python basic_character_eda.py fic outfile")
    print("or")
    print("python basic_character_eda.py bio outfile")

## DONE.

with open(outfile, mode = 'w', encoding = 'utf-8') as f:
    f.write('story\ttotalsize\tdialsize\tgender\n')
    for line in outlines:
        f.write(line)
