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
A model using only fiction, prepared without any stopwording, and divided into 50 topics.

fic100
-------
A model using only fiction, prepared without any stopwording, and divided into 100 topics.
