## measure_variation.py

# This script is designed to automate the process of condensing multiple models
# and testing them against pre-registered hypotheses.

# We start with a modelname (arg1). We expect to find 12 doctopics files
# associated with that model. Each of those files will be
# condensed into a roletheme file and stored in a folder associated
# with the modelname. In doing this, we will also need to know
# the number of themes (as versus roles) associated with this model.

# Then we run smart-evaluate and regular-evaluation processes for all
# of the roletheme files.

import sys, csv, os
import numpy as np
import pandas as pd

import autocondense_rolethemes as autocondense
import autoevaluate_hypotheses as evaluate
import autosmartevaluate_rolethemes as smartevaluate

args = sys.argv

modelname = args[1]
themecount = int(args[2])

inroot = '/projects/ischoolichass/ichass/usesofscale/code/roles/'
outroot = '../' + modelname + '_mcmc/'

if not os.path.isdir(outroot):
	os.mkdir(outroot)

# CONDENSE DOCTOPIC FILES

for i in range(12):
	inpath = inroot + modelname + '_mcmc' + str(i) + '_doctopics.tsv'
	outpath = outroot + modelname + '_mcmc' + str(i) + '_rolethemes.tsv'

	if os.path.isfile(outpath):
		continue
	elif not os.path.isfile(inpath):
		break
	else:
		print("Condense: " + str(i))
		autocondense.condense_a_file(inpath, outpath, themecount)

ceiling = i + 1

# That's the number of files we found

for i in range(ceiling):
	inpath = outroot + modelname + '_mcmc' + str(i) + '_rolethemes.tsv'
	evaluate.evaluate_a_model(inpath)

print()

for i in range(ceiling):
	inpath = outroot + modelname + '_mcmc' + str(i) + '_rolethemes.tsv'
	smartevaluate.smarteval_a_model(inpath, themecount)


