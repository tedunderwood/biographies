#!/usr/bin/env python3

# jsontotable5.py

# Written December, 2015. Rewritten June 2017.
# Ted Underwood.

# This translates the jsons produced by
# David Bamman's BookNLP pipeline into a simpler text file.

# As the telltale 5 implies, this is the last in a series
# of versions. This version is designed to work only with
# HathiTrust data. Earlier versions also used Chicago.

# It unpacks each json into a string of words
# separated by spaces, folding grammatical roles together except
# that passive verbs get prefixed by "was-" and dialogue
# gets prefixed by "said-". My observation is that in practice
# mod and poss are pretty legible from the part of speech.

# usage python jsontotable5.py -folder infolder outfile
# or
#       python jsontotable5.py -jsonl infile outfile
#
# the first expects separate volume jsons in a folder
# the second expects a JSON-lines file with one volume
# json per line

import pandas as pd
import ujson, csv, sys, os


# date functions taken from https://github.com/tedunderwood/library/blob/master/SonicScrewdriver.py
def infer_date(datetype, firstdate, seconddate, textdate):
    '''Receives a date type and three dates, as strings, with no guarantee that any
    of the dates will be numeric. The logic of the data here is defined by
    MARC standards for controlfield 008:
    http://www.loc.gov/marc/bibliographic/concise/bd008a.html
    Returns a date that represents either a shaky consensus
    about the earliest attested date for this item, or 0, indicating no
    consensus.
    '''
    try:
        intdate = int(firstdate)
    except:
        # No readable date
        if firstdate.endswith('uu'):
            # Two missing places is too many.
            intdate = 0
        elif firstdate.endswith('u'):
            # but one is okay
            try:
                decade = int(firstdate[0:3])
                intdate = decade * 10
            except:
                # something's weird. fail.
                intdate = 0
        else:
            intdate = 0

    if intdate == 0:
        try:
            intdate = int(textdate)
        except:
            intdate = 0

    try:
        intsecond = int(seconddate)
    except:
        intsecond = 0

    if intsecond - intdate > 80 and intsecond < 2100:
        # A gap of more than eighty years is too much.
        # This is usually an estimated date that could be anywhere within
        # the nineteenth century.
        # note that we specify intsecond < 2100 because otherwise things
        # dated 9999 throw an error
        intdate = 0

    if datetype == 't' and intsecond > 0 and intsecond < intdate:
        intdate = intsecond
        # This is a case where we have both a publication date and
        # a copyright date. Accept the copyright date. We're going
        # for 'the earliest attested date for the item.'

    if intdate < 1000 and intsecond > 1700 and intsecond < 2100:
        intdate = intsecond

    return intdate

def date_row(row):
    datetype = row["datetype"]
    firstdate = row["startdate"]
    secondate = row["enddate"]
    if "imprintdate" in row:
        textdate = row["imprintdate"]
    else:
        textdate = row["textdate"]
    intdate = infer_date(datetype, firstdate, secondate, textdate)
    return intdate

##bio_df = pd.read_csv('./biographies/metadata/hathi_ic_biog.tsv', sep='\t')
##
### add infer_date to the df
##bio_dict = bio_df.to_dict(orient='records')
##for row in bio_dict:
##    row['inferreddate'] = date_row(row)
##
##new_bioindex = pd.DataFrame()
##new_bioindex = new_bioindex.from_records(bio_dict)
##
##new_bioindex.to_csv('hathi_ic_date.tsv', index=False, sep='\t')
##

def add_dicts_to_list(alistofdicts, alist, prefix):
    global variants

    for word in alistofdicts:
        wordval = word["w"].lower()
        if wordval in variants:
            wordval = variants[wordval]

        if len(prefix) > 1:
            wordval = prefix + '-' + wordval

        alist.append(wordval)

    return alist

outlist = list()
counter = 0

usedalready = set()

# GLOBAL VARIABLES below
# Python doesn't make us declare globals, but I wish it did.

unknowndate = 0     # GLOBAL counter for number of characters without dates
thingsunknown = set()

id2date = dict()    # GLOBAL dict translating docids to dates

# One of the main functions of this transformation is to pair each
# character with a publication date. That will allow us to easily
# select subsets of characters

with open('../metadata/pre23biometa.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        # there are two different forms of id volumes can have,
        # because 19c stories are often multi-volume
        # we're going to treat them all as valid
        
        #docid = row['docid']
        #recordid = row['recordid']
        htid = row['HTid']
        if row['inferreddate'] != '':
            inferreddate = int(row['inferreddate'].split('.')[0])
            id2date[htid] = inferreddate
        #id2date[docid] = inferreddate
        #id2date[recordid] = inferreddate

variants = dict()  # GLOBAL dictionary translating US -> UK spelling.

# We don't want classification accuracy to be thrown off by deviant American spellings;
# the VariantSpellings file will normalise them all to a standard centred on the UK.

with open('../lexicons/VariantSpellings.txt', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        if len(fields) < 2:
            continue
        else:
            variants[fields[0]] = fields[1]

stopwords = set()    # GLOBAL list of stopwords only used to filter dialogue
stoppath = '../lexicons/stopwords.txt'
with open(stoppath, encoding = 'utf-8') as f:
    for line in f:
        stopwords.add(line.lower().strip())

morestops = {'just', 'right', 'mr', 'mr.', "n't", "ca"}
for stop in morestops:
    stopwords.add(stop)

def append_characters(jsonstring, outfile, expectedid):
    ''' Given a single json string produced by BookNLP, this extracts the
    characters, and prints them in simpler format to outfile.

    jsonstring: what we will parse
    outfile: where it gets written
    expectedid: a docid implied by the filename where we got jsonstring
    '''

    global id2date, unknowndate, stopwords, thingsunknown

    jsonobject = ujson.loads(jsonstring)

    storyid = jsonobject["id"]

    if storyid in id2date:
        date = id2date[storyid]
        docid = storyid
    elif expectedid in id2date:
        date = id2date[expectedid]
        docid = expectedid
    else:
        unknowndate += 1
        thingsunknown.add(expectedid)
        date = -1
        return 0

        # I'm not writing books I can't date

    characterlist = jsonobject["characters"]

    usedalready = set()
    # just to confirm that there are no duplicate names
    # within a single book

    outlist = []        # gather lines to write to file
    writtenchars = 0    # num actually written may not == num in characterlist

    for character in characterlist:

        # what is this character's name?
        # take the most common name
        names = character["names"]
        maxcount = 0
        thename = "nobody"
        for name in names:
            if name["c"] > maxcount:
                maxcount = name["c"]
                thename = name["n"].replace(" ", "")

        namestring = thename

        while namestring in usedalready:
            namestring = namestring + "*"

        usedalready.add(namestring)

        gender = character["g"]
        if gender == 1:
            genderstring = "f"
        elif gender == 2:
            genderstring = "m"
        else:
            genderstring = 'u'

        thesewords = []       # gathering all words for this character

        thesewords = add_dicts_to_list(character["agent"], thesewords, '')
        thesewords = add_dicts_to_list(character["poss"], thesewords, '')
        thesewords = add_dicts_to_list(character["mod"], thesewords, '')
        thesewords = add_dicts_to_list(character["patient"], thesewords, 'was')

        for spoken in character["speaking"]:
            wlist = spoken['w'].lower().split()
            for w in wlist:
                if w in stopwords:
                    continue
                if len(w) > 0 and w[0].isalpha():
                    word = 'said-' + w
                    thesewords.append(word)

        if len(thesewords) > 10:
            # we only write characters that have more than ten
            # words associated

            writtenchars += 1
            textstring = ' '.join(thesewords)
            outline = '\t'.join([docid, namestring, docid + '|' + namestring, genderstring, str(date), textstring])
            outlist.append(outline)

    with open(outfile, mode="a", encoding="utf-8") as outfile:
        for line in outlist:
            outfile.write(line + '\n')

    return writtenchars


## MAIN EXECUTION BEGINS HERE

arguments = sys.argv
datasource = arguments[2]
outfile = arguments[3]
command = arguments[1]

# Whichever command / data source is being used,
# we need to create a header for the outfile if
# one does not yet exist.

if os.path.isfile(outfile):
    print('Hey, you know ' + outfile)
    print('already exists, right? Just confirming.')
    print('I will append to it.')
else:
    with open(outfile, mode = 'w', encoding = 'utf-8') as f:
        f.write('docid\tcharname\tcharid\tgender\tpubdate\twords\n')
        # tab-separated, five fields

ctr = 0
totalchars = 0

if command == '-folder':
    assert os.path.isdir(datasource)
    # otherwise we have an error

    sourcefiles = [x for x in os.listdir(datasource) if x.endswith('.book')]
    # the data files produced by BookNLP all end with '.book'
    for sf in sourcefiles:
        path = os.path.join(datasource, sf)
        with open(path, encoding = 'utf-8') as f:
            jsonstring = f.read()

        expectedid = sf.replace('.book', '')
        totalchars += append_characters(jsonstring, outfile, expectedid)

        ctr += 1
        if ctr % 100 == 1:
            print(ctr)

elif command == '-jsonl':
    assert os.path.isfile(datasource)
    # otherwise we have an error

    with open(datasource, encoding = 'utf-8') as f:
        for jsonstring in f:
            totalchars += append_characters(jsonstring, outfile, 'dummystring')

            ctr += 1
            if ctr % 100 == 1:
                print(ctr)

else:
    print("Usage for jsontotable5 is either:")
    print("python jsontotable5.py -folder infolder outfile")
    print("or")
    print("python jsontotable5.py -jsonl infile outfile")

## DONE.

print('Unknown dates: ' + str(unknowndate))












