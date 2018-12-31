Generalized character models
============================

In Dec 2018 we restarted work on this project by framing some generalized models of character.

The pipeline we used to create them is basically

dataprep => MALLET => interpretation

Significant choices can be made at each stage.

**Data:** The raw data for this project is too big for a github repo and will have to be added later; even the full doc-topic matrices are too big. But we can run most of the interpretation and evaluation for the project using a reduced subset of the doc-topic matrix that contains only characters in volumes mentioned in [```hypotheses.tsv```](https://github.com/tedunderwood/biographies/tree/master/evaluation).

We do that reduction using ```interpret/condense_doctopics.py```. This script converts the full doctopics file produced by MALLET, into a reduced form that ends "_vols.tsv." These reduced subsets are what you will find in the data directories described below.

dataprep
--------

Contains scripts we used to convert the output of BookNLP into a format suitable for MALLET.

mallet
------

Contains batch scripts that were used to direct MALLET on the Illinois campus cluster.

interpret
---------

Scripts that translate the output of MALLET into meaningful results.

fic50
------
A model using only fiction, prepared without any stopwording, and divided into 50 topics. This and other models described only as fic + integer are based on ```malletficchars.txt```, which contained 18,987 volumes and 631,388 characters, and was imported into MALLET as ```basicficchars.mallet.```

fic100
-------
A model using only fiction, prepared without any stopwording, and divided into 100 topics.

fic200
-------
A model using only fiction, prepared without any stopwording, and divided into 200 topics. *This is at present the best-performing model.*

fic300
-------
A model using only fiction, prepared without any stopwording, and divided into 100 topics.

ficnospeech50
-------------
A model using only fiction *without dialogue* (just words governed by characters) and divided into 50 topics. This and other ficnospeech models were based on ```malletficnospeech.txt```, which was imported into MALLET as ```ficnospeech.mallet.```

ficnospeech100
--------------
A model using only fiction *without dialogue* and divided into 100 topics.

ficnospeech200
--------------
A model using only fiction *without dialogue* and divided into 200 topics.

ficnospeech300
--------------
A model using only fiction *without dialogue* and divided into 300 topics.
