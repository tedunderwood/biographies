# jsontotable3.py

# Written December, 2015. It translates the jsons produced by
# David Bamman's BookNLP pipeline into a simpler text file.

# This is based on jsontotable2, located in some booknlp directory or
# other. It differs above all in appending suffixes to the words
# that indicate their grammatical relationship to the character.
# ~n for nouns that are possessed; i.e., "her mind"
# ~m for things that modify the character; "she was glad"
# ~p for verbs that the character has a passive relation to
# the default, verbs where the character is the subject,
# are not specifically marked.

import ujson, csv

def add_dicts_to_list(alistofdicts, alist, category):
    global variants

    for word in alistofdicts:
        wordval = word["w"].lower()
        if wordval in variants:
            wordval = variants[wordval]

        if category != 'a':
            wordval = wordval + '~' + category

        alist.append(wordval)

    return alist

outlist = list()
counter = 0

usedalready = set()

htid2story = dict()
htid2date = dict()

with open('/Users/tunder/Dropbox/character/meta/charmeta.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        story = row['storyID']
        htid = row['htid']
        htid2story[htid] = story
        htid2date[htid] = int(row['date'])

missingstory = 0
unknowndate = 0

variants = dict()
# We're about to process Chicago volumes, which will have deviant American
# spellings of many words

with open('/Users/tunder/Dropbox/DataMunging/rulesets/VariantSpellings.txt', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        if len(fields) < 2:
            continue
        else:
            variants[fields[0]] = fields[1]

with open("/Volumes/TARDIS/work/characterdata/originaljsons/chicago.json", encoding = "utf-8") as f:
    for line in f:
        jsonobject = ujson.loads(line)

        storyid = jsonobject["id"]
        if storyid in htid2date:
            date = htid2date[storyid]
            if date < 1920:
                continue
                # for present purposes we're only using chicago beyond 1920
        else:
            unknowndate += 1

        # we used htids as storyids in processing the 20c, but
        # in the long run it's better to have the 19c and 20c
        # unified by a single set of story ids, for which purpose
        # we use a handy 20c translation table

        if storyid in htid2story:
            storyid = htid2story[storyid]
        else:
            missingstory += 1

        characterlist = jsonobject["characters"]

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

            namestring = storyid + "_" + thename

            while namestring in usedalready:
                namestring = namestring + "*"

            usedalready.add(namestring)
            print(namestring)

            gender = character["g"]
            if gender == 1:
                genderstring = "female"
            elif gender == 2:
                genderstring = "male"
            else:
                genderstring = 'unknown'

            thesewords = []
            thesewords = add_dicts_to_list(character["agent"], thesewords, 'a')
            thesewords = add_dicts_to_list(character["poss"], thesewords, 'n')
            thesewords = add_dicts_to_list(character["mod"], thesewords, 'm')
            thesewords = add_dicts_to_list(character["patient"], thesewords, 'p')

            textstring = ' '.join(thesewords)

            outline = namestring + "\t" + genderstring + "\t" + textstring + "\n"
            outlist.append(outline)

            counter += 1

            if counter % 1000 == 999:

                with open("/Volumes/TARDIS/work/characterdata/19and20chars.txt", mode="a", encoding="utf-8") as outfile:
                    for line in outlist:
                        outfile.write(line)

                outlist = list()

print(counter)

with open("/Volumes/TARDIS/work/characterdata/19and20chars.txt", mode="a", encoding="utf-8") as outfile:
    for line in outlist:
        outfile.write(line)

print('Missing stories: ' + str(missingstory))
print('Unknown dates: ' + str(unknowndate))








