chars2get = set()

with open('biofic2take.tsv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        charid = fields[0]
        chars2get.add(charid)

outlines = []

with open('../biofic50/biofic50_doctopics.txt', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        charid = fields[1]
        if charid in chars2get:
            outlines.append(line)

with open('../biofic50/biofic50_viz.tsv', mode = 'w', encoding = 'utf-8') as f:
    for line in outlines:
        f.write(line)
