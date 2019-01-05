import csv, random

specialids = set()

with open('../../evaluation/hypotheses.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        ids = [row['firstsim'], row['secondsim'], row['distractor']]
        for anid in ids:
            specialids.add(anid)

taken = dict()
takenlabels = dict()
bio = set()
fic = set()

with open('../data/bioficchars.txt', encoding = 'utf-8') as f:
    for row in f:
        fields = row.strip().split()
        label = fields[1]
        if fields[0] in specialids:
            continue
        elif len(fields) < 20:
            continue

        if label.startswith('bio'):
            bio.add(fields[0])
        else:
            fic.add(fields[0])

sample = []
sample.extend(random.sample(fic, 2000))
sample.extend(random.sample(bio, 2000))
sample = set(sample)

with open('../data/bioficchars.txt', encoding = 'utf-8') as f:
    for row in f:
        fields = row.strip().split()
        if fields[0] in specialids or fields[0] in sample:
            label = fields[1]
            takenlabels[fields[0]] = label

with open('biofic2take.tsv', mode = 'w', encoding = 'utf-8') as f:
    for charid, label in takenlabels.items():
        f.write(charid + '\t' + label + '\n')

