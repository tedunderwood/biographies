Data preparation scripts
========================

Unfortunately, none of the data for this process fits in github. But I can at least share the scripts I used, and share data later on another platform.

Fiction jsons produced by BookNLP were initially transformed into tables by jsontotable5.py.

Then I ran scripts to select characters distributed (relatively) evenly across the timeline. Different scripts produced different editions of the data.

tabletomallet_firstfic.py
-------------------------

Produced malletficchars.txt, and thus the models filed as fic50, fic100, and so on.
