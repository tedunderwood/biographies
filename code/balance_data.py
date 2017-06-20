import pandas as pd
import numpy as np
import sys

outfile = sys.argv[1]

bio_df = pd.read_csv('~/biographies/metadata/hathi_ic_biog.tsv', sep='\t')

bioindex = pd.read_csv('/media/secure_volume/index/bioindex.tsv',sep='\t')

merge_bioindex = pd.merge(
    bio_df, bioindex,
    how='inner',
    left_on='docid',
    right_on='htid').loc[
    :,['infer_date','authgender','mainid','htid','filesuffix']
    ]

# date functions taken from https://github.com/tedunderwood/library/blob/master/SonicScrewdriver.py
def infer_date(datetype, firstdate, seconddate, textdate):
    '''Receives a date type and three dates, as strings, with no guarantee that any
    of the dates will be numeric. The logic of the data here is defined by
    MARC standards for controlfield 008:
    http://www.loc.gov/marc/bibliographic/concise/bd008a.html
    Returns a date that represents either a shaky consensus
    about the earliest attested date for this item, or 0, indicating no
    consensus.
    '''
    try:
        intdate = int(firstdate)
    except:
        # No readable date
        if firstdate.endswith('uu'):
            # Two missing places is too many.
            intdate = 0
        elif firstdate.endswith('u'):
            # but one is okay
            try:
                decade = int(firstdate[0:3])
                intdate = decade * 10
            except:
                # something's weird. fail.
                intdate = 0
        else:
            intdate = 0

    if intdate == 0:
        try:
            intdate = int(textdate)
        except:
            intdate = 0

    try:
        intsecond = int(seconddate)
    except:
        intsecond = 0

    if intsecond - intdate > 80 and intsecond < 2100:
        # A gap of more than eighty years is too much.
        # This is usually an estimated date that could be anywhere within
        # the nineteenth century.
        # note that we specify intsecond < 2100 because otherwise things
        # dated 9999 throw an error
        intdate = 0

    if datetype == 't' and intsecond > 0 and intsecond < intdate:
        intdate = intsecond
        # This is a case where we have both a publication date and
        # a copyright date. Accept the copyright date. We're going
        # for 'the earliest attested date for the item.'

    if intdate < 1000 and intsecond > 1700 and intsecond < 2100:
        intdate = intsecond

    return intdate

def date_row(row):
    datetype = row["datetype"]
    firstdate = row["startdate"]
    secondate = row["enddate"]
    if "imprintdate" in row:
        textdate = row["imprintdate"]
    else:
        textdate = row["textdate"]
    intdate = infer_date(datetype, firstdate, secondate, textdate)
    return intdate

def make_balanced(df):
    balanced_df = pd.DataFrame()
    for yr in np.arange(1923,2001):
        for gender in ['F','M','U']:
            subset_df = df.loc[(df.infer_date == str(yr)) & (df.authgender == gender),:]
            df_shape = subset_df.shape
            if gender == 'U':
                subset_df = subset_df.head(25)
            if df_shape[0] > 50:
                subset_df = subset_df.head(50)
            else:
                print('Only', df_shape[0], 'rows written for:')
                print(yr, '-->',gender)
            balanced_df = pd.concat([balanced_df, subset_df], axis=0)
    return balanced_df

# add infer_date to the df
merge_dict = merge_bioindex.to_dict(orient='records')
for row in merge_dict:
    row['infer_date'] = date_row(row)

new_bioindex = pd.DataFrame()
new_bioindex.from_records(df_dict)

# create gender-balanced subset df
balanced_df = make_balanced(new_bioindex)

# write to given outfile
balanced_df.to_csv(outfile, index=False, sep='\t')

print(balanced_df.shape[0], 'rows written to', outfile)
