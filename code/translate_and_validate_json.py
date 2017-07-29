#!/usr/bin/env python3

# translate_and_validate_json.py

# This script translates jsons produced by BookNLP into a
# form that is more securely and completely nonconsumptive.

# USAGE of this module:

# python3 translate_and_validate.py -command infolder outfolder

# where -command is either -translate or -validate
# and the last two arguments are the folder to get jsons from
# and the one to write them to.
#
# Translate converts raw jsons into a clearly nonconsumptive form;
# validate just copies them while confirming that they don't contain
# any strings longer than 200 chars.

import ujson, os, sys, csv
from collections import Counter

def translate_json(inpath, outpath):
    '''
    Takes a json file produced by David Bamman's BookNLP
    code, and translates it into a form that lacks
    references to word position. It also turns dialogue
    into word counts.
    '''

    # we confirm that the outfile doesn't yet exist

    if os.path.exists(outpath):
        return 'file already exists'

    roles = ['agent', 'patient', 'mod', 'poss']

    with open(inpath, encoding = 'utf-8') as f:
        jsonstring = f.read()

    old = ujson.loads(jsonstring)
    new = dict()

    storyid = old["id"]
    new["id"] = storyid

    new["characters"] = []
    for c in old["characters"]:
        newchar = dict()
        newchar['names'] = c['names']
        newchar['g'] = c['g']
        newchar['NNPcount'] = c['NNPcount']
        newchar['id'] = c['id']

        for role in roles:
            oldrole = c[role]
            newrole = []
            for word in oldrole:
                newrole.append(word['w'])
                # we are dumping the old attribute 'i' which pointed to the actual
                # location of the word in the book. Instead the new grammatical role
                # will be a straightforward list of words


            newchar[role] = newrole

        speaking = c['speaking']
        wordcounts = Counter()
        for speech in speaking:
            wlist = speech['w'].lower().split()
            for w in wlist:
                wordcounts[w] += 1
        newchar['speaking'] = wordcounts


        new['characters'].append(newchar)

    outstring = ujson.dumps(new)
    with open(outpath, mode = 'w', encoding = 'utf-8') as f:
        f.write(outstring)

    return 'written'

def truncate_200(astring, errors, errorcategory):
    '''
    Truncates a string so it has no more than 200 characters.
    '''

    if len(astring) > 200:
        astring = astring[0 : 200]
        errors[errorcategory] += 1
        return astring
    else:
        return astring


def validate_json(inpath, outpath):
    # let's confirm that this is valid and none of the strings in it are too big
    # to be non-consumptive, while copying it to a new location

    # this will guarantee that the file in the new location does not contain
    # any string larger than 200 characters

    roles = ['agent', 'patient', 'mod', 'poss']

    with open(inpath, encoding = 'utf-8') as f:
        jsonstring = f.read()

    old = ujson.loads(jsonstring)
    new = dict()

    errors = Counter()
    errorcats = ['names', 'word', 'dialogue']
    for cat in errorcats:
        errors[cat] = 0

    if os.path.exists(outpath):
        return errors, 'file already exists'

    storyid = old["id"]

    new["id"] = storyid

    new["characters"] = []
    for c in old["characters"]:
        newchar = dict()
        newchar['names'] = c['names']
        for name in newchar['names']:
            name['n'] = truncate_200(name['n'], errors, 'names')

        newchar['g'] = c['g']

        newchar['NNPcount'] = c['NNPcount']
        newchar['id'] = c['id']

        for role in roles:
            oldrole = c[role]
            newrole = []
            for word in oldrole:
                word = truncate_200(word, errors, 'word')
                newrole.append(word)
            newchar[role] = newrole

        newchar['speaking'] = Counter()
        for word, count in c['speaking'].items():
            word = truncate_200(word, errors, 'dialogue')
            newchar['speaking'][word] = count

        new['characters'].append(newchar)

    outstring = ujson.dumps(new)
    with open(outpath, mode = 'w', encoding = 'utf-8') as f:
        f.write(outstring)

    return errors, 'written'

### MAIN CODE

args = sys.argv

if len(args) < 4:
    print('USAGE of this module:')
    print('python3 translate_and_validate.py -command infolder outfolder')
    print()
    print('where -command is either -translate or -validate')
    print('and the last two arguments are the folder to get jsons from')
    print('and the one to write them to.')
    print()
    print('Translate converts raw jsons into a clearly nonconsumptive form;')
    print("validate just copies them while confirming that they don't contain")
    print('any strings longer than 200 chars.')

command = args[1]
indirectory = args[2]
outdirectory = args[3]

if command == '-translate':
    files = os.listdir(indirectory)
    jsons = [x for x in files if x.endswith('.book')]
    for j in jsons:
        inpath = os.path.join(indirectory, j)
        outpath = os.path.join(outdirectory, j)
        if not os.path.exists(inpath):
            print('Missing file.')
        elif os.path.exists(outpath):
            print('Attempt to overwrite ' + outpath + " , skipping.")
        else:
            result = translate_json(inpath, outpath)

if command == '-validate':
    errorfields = ['fileid', 'names', 'word', 'dialogue']
    files = os.listdir(indirectory)
    jsons = [x for x in files if x.endswith('.book')]
    sumerrors = dict()

    for j in jsons:
        inpath = os.path.join(indirectory, j)
        outpath = os.path.join(outdirectory, j)
        if not os.path.exists(inpath):
            print('Missing file.')
        elif os.path.exists(outpath):
            print('Attempt to overwrite ' + outpath + " , skipping.")
        else:
            errors, result = validate_json(inpath, outpath)
            sumerrors[j] = errors

    with open('errorlog.tsv', mode = 'w', encoding = 'utf-8') as f:
        scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = errorfields)
        scribe.writeheader()

        for anid, errordict in sumerrors.items():
            out = dict(errordict)
            out['fileid'] = anid
            scribe.writerow(out)
















