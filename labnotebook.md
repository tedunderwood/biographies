lab notebook
============

The readme.md file is good as a central summary of what everything *is,* but one often also needs a more narrative account of what got done. That's what this is for. It doesn't need to get as detailed as git commits.

June 5, 2017
------------
Merged extract and slicer
Installed git on the DC
Edited extract.py so that it runs on the DC
But two outstanding issues:
1. it's designed to run in the secure volume and
2. it seems to always produce lists of ten files
3. we probably need to build in a stage where it wipes the holding folder and
4. extracting files is slow, probably because we're reopening the zip archive

#### Natalie
installed Vim and configured .vimrc for use with arrows, backspace, etc
installed pip for python3 and set up pip3 environment variables
+ use `pip3 install <package>` to use with python3
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
Wrote balance_data.py that subsets hathi_ic_biog.tsv with 50 Female, 50 Male, and 25 Unknown author genders for each year (1923-2000)
+ outputs to /media/secure_volume/balanced_hathi_ic_biog.tsv

June 15, 2017
-------------
#### Natalie
Wrote extract_balanced.py, which is a version of extract.py that takes an <infile> and <outfile> as arguments. The infile is the dataset of files that we want (output file from balance_data.py). It gets the volsplit locations from bioindex.tsv and writes the slice file with bio IDs and paths at the <outfile> location.
+ need to investigate why only 9413 files were moved to the holding_folder, of the 9725 rows in balanced_hathi_ic_biog.tsv. Probably an issue with how I am merging with bioindex.tsv
+ improve speed somehow? it took about 10 minutes to run. a way to open each volsplit only once when extracting?

June 16, 2017
-------------
#### Natalie
Changed balance_data.py to merge bioindex.tsv with hathi_ic_biog.tsv first, so that all IDs will match and we don't have any NaN volsplit file locations (filesuffix)
Now takes a command line argument of where to save the outfile (.tsv)
Prints out year and author gender if less than 50 rows are found
+ my test outfile is saved at /secure_volume/meta/balanced_hathi_ic_biog.tsv
+ 9712 rows total. 50 M, 50 F, 25 U for each imprintdate year, except:
  + 1923-F - 41 rows
  + 1925-F - 42 rows
  + 1926-F - 46 rows
  + 1940-F - 49 rows
  + 1941-F - 42 rows
  + 1944-F - 42 rows

Changed extract_balanced.py to iterate over each volsplit file and extract all the necessary files, so each volsplit is opened only once
Tested that it outputs correct number of lines (9712) to the given outfile
+ my test outfile is at /secure_volume/natalie/outfile.txt
+ much faster now, runs in 1:30

June 20, 2017
-------------
#### Ted
Rewrote the PagesToCharacters class that serves as a wrapper for David's BookNLP, letting it use zip files that contain a lot of page files.

To generate the new .jar I futzed around a bit. Finally edited the src in javaworkspace/book-nlp which is confusingly filed under the project "narrative" in Eclipse.

I produced a "Runnable JAR" for the whole narrative project.

This worked, but I'm not sure it was necessary. A much smaller non-runnable jar was probably what I had in place, and it had worked fine, given that the libraries are present and on the classpath.

#### Natalie
Updated the balance data script to include the date functions from previous work done at: https://github.com/tedunderwood/library/blob/master/SonicScrewdriver.py
Messed around with restructuring scripts and extracting everything to holding folder


June 22, 2017
-------------
#### Natalie
Changed the extractor (now extract.py) to extract all bio files into the holding folder, so we won't have to redo this step every time the data changes
+ this was done by merging hathi_ic_biog.tsv and bioindex.tsv
+ all shared hathitrust IDs with volsplit locations were extracted
Merged with Ryan's code so that slicer.py takes 3 command line args: <infile> <outfile> <number of slices>
Tested the three scripts (extract.py, balance_data.py, slicer.py) are working on the data capsule

June 26, 2017
-------------
#### Ted
Added several files to /code that I've used in the past to extract characters as strings from json files.
Also added 19andchicagoficmeta.csv to /metadata, and VariantSpellings.txt to /lexicons. These files are used in extracting characters.

December 28, 2018
-----------------
#### Ted
Completed [preregistration for generalized character model.](https://osf.io/my8r7/register/564d31db8c5e4a7c9694b2be)

Began preparing data for topic modeling.

December 31, 2018
-----------------
#### Ted
Generated eight initial fiction models (with and without dialogue), and tested evaluation scripts that compared raw topic vectors, or vectors adjusted relative to document centroids, author centroids, period centroids, and overall centroids.

The best-performing approach was to normalize relative to document centroids when comparing characters from the same book; otherwise, use raw vectors. This topped out at 81.5% accuracy. A naive approach that simply used raw vectors topped out at 76% accuracy. The fic200 model, with 200 topics and including dialogue, was the best-performing topic model.

Now to compare biographies.


