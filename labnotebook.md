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

#### Natalie
installed Vim and configured .vimrc for use with arrows, backspace, etc
installed pip for python3 and set up pip3 environment variables
+ use `pip3 install <package>' to use with python3
installed pandas, numpy, zipfile, ipython, matplotlib for python3 


June 6, 2017
------------
Added author genders to metadata/hathi_ic_biog.tsv,
using [Gender-ID.py, by Bridget Baird and Cameron Blevins](https://github.com/cblevins/Gender-ID-By-Time)


June 13, 2017
------------
#### Natalie
Added shutil step that wipes the holding_folder if it exists
Changed the script to locate the correct volsplit.zip file using the filesuffix column in bioindex (much faster now)
Added error handling try & except block when extracting files to holding_folder
Tested slicer is writing correct number of lines in the output file
Merged with master

June 14, 2017
-------------
#### Natalie
Figuring out how to push to remote under collaborator username
 
