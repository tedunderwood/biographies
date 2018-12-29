Generalized character models
============================

In Dec 2018 we restarted work on this project by framing some generalized models of character.

The pipeline we used to create them is basically

dataprep => MALLET => interpretation

Significant choices can be made at each stage.

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
A model using only fiction, prepared without any stopwording, and divided into 50 topics. This and other models described only as fic + integer are based on malletficchars.txt, which contained 18,987 volumes and 631,388 characters, and was imported into MALLET as basicficchars.mallet.

fic100
-------
A model using only fiction, prepared without any stopwording, and divided into 100 topics.
