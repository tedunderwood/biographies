import pandas as pd
import numpy as np

bio_df = pd.read_csv('~/biographies/metadata/hathi_ic_biog.tsv', sep='\t')

bioindex = pd.read_csv('/media/secure_volume/index/bioindex.tsv',sep='\t')

merge_bioindex = pd.merge(
    bio_df, bioindex,
    how='inner',
    left_on='docid',
    right_on='htid').loc[
    :,['imprintdate','authgender','mainid','htid','docid','filesuffix']
    ]

def make_balanced(df):
    balanced_df = pd.DataFrame()
    for yr in np.arange(1923,2001):
        for gender in ['F','M','U']:
            subset_df = df.loc[(df.imprintdate == str(yr)) & (df.authgender == gender),:]
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

balanced_df = make_balanced(merge_bioindex)

balanced_df.to_csv('/media/secure_volume/meta/2balanced_hathi_ic_biog.tsv', index=False, sep='\t')
