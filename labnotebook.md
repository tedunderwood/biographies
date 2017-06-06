lab notebook
============

The readme.md file is good as a central summary of what everything *is,* but one often also needs a more narrative account of what got done. That's what this is for. It doesn't need to get as detailed as git commits.

June 5, 2017
------------
Merged extract and slicer
Installed git on the DC
Edited extract.py so that it runs on the DC
But two outstanding issues:
(1) it's designed to run in the secure volume and
(2) it seems to always produce lists of ten files
(3) we probably need to build in a stage where it wipes the holding folder and
(4) extracting files is slow, probably because we're reopening the zip archive
