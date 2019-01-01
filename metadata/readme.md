biographies/metadata
====================

Metadata about biographies held by HathiTrust, including a subsample we are using.

**hathi_ic_biog.tsv** is a tab-separated file with metadata about 106,655 biographies contained in HathiTrust and characterized as in-copyright. It was created in 2017 by subsetting metadata extracted in 2016 for works that were in-copyright, not serials, in English (language == 'eng') and that contain 'Biography' or 'Autobiography' in the genre field.

This was produced by scrape_json.py in [the DataMunging/HathiMetadata repo,](https://github.com/tedunderwood/DataMunging/tree/master/HathiMetadata) if you want to understand how particular colums are related to MARC format.

**20cbiographyHTids.txt** is a stripped-down list of just the HT volume ids from the same file.

**pre23biometa.tsv** is analogous metadata for biographies in the public-domain part of Hathi.

**alreadyhavebio.txt** is a list of the volumes actually present on the cluster in /chardata.

**balanced_character_subset.csv** lists volumes used for modeling, contained on the cluster in character_subset.

returning to update in Jan 2019
-------------------------------

**merged_bio_meta.tsv** seems to be the most complete and integrated biography metadata I have

**allparsedbio.tsv** is a subset of the above file, created by first scraping all the docids from ```../data/all_post23bio_Sep11.tsv``` and ```../data/all_pre23bio_new.tsv```. Then we used those docids to subset merged_bio:

    havemeta = meta.loc[havebio, : ]
    meta = havemeta[~havemeta.index.duplicated(keep = 'first')]
    meta.to_csv('/Users/tunder/Dropbox/python/biographies/metadata/allparsedbio.tsv', sep = '\t', index_label = 'docid')

Not sure why it was necessary to drop duplicates. Deserves investigation.
