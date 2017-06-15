import pandas as pd
import numpy as np

df = pd.read_csv('../metadata/hathi_ic_biog.tsv', sep='\t')

def make_balanced_df(df):
    balanced_df = pd.DataFrame()
    for yr in np.arange(1923,2001):
        for gender in ['F','M','U']:
            subset_df = df.loc[(df.imprintdate == str(yr)) & (df.authgender == gender),:]
            df_shape = subset_df.shape
            if gender == 'U':
                subset_df = subset_df.head(25)
            if df_shape[0] > 50:
                subset_df = subset_df.head(50)
            balanced_df = pd.concat([balanced_df, subset_df], axis=0)
    return balanced_df

balanced_df = make_balanced(df)

balanced_df.to_csv('/media/secure_volume/balanced.tsv', index=False, sep='\t')
