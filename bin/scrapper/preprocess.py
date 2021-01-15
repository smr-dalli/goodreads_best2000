import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def clean_data(df):
    df['num_reviews'] = list(map(lambda x: int(x[0]) if len(x) > 1 else None, [x.replace(',','').replace('NONE', '0').split() for x in df['num_reviews']] ))
    df['num_pages'] = list(map(lambda x: int(x) if x[0].isnumeric() else None, [x[:x.find('p')] for x in df['num_pages']]))
    df['awards'] = [x.strip().split(',')[:x.find(')') + 1] for x in df['awards']]
    df['series'] = list(map(lambda x: True if len(x) > 1 else False, df['series']))
    df['year_published'] = list(map(lambda x: int(x[x.index('by') - 1]) if 'by' in x else None, [x.strip().split() for x in df['year_published']]))
    df['places'] = list(map(lambda x: x[x.index('Setting') + 1:] if 'Setting' in x else None, list(map(lambda x: x[:x.index('Other')] if 'Other' in x else x, list(map(lambda x: x[:x.index('Literary')] if 'Literary' in x else x, [x.strip().split() for x in df['places']]))))))
    return df
   
def preprocessing(df):
    df = clean_data(df)
    df['avg_rating'] = pd.to_numeric(df['minirating'].apply(lambda x: (x.split('— ')[0])).apply(lambda x: x.replace(' avg rating', '')).apply(lambda x: x.replace(' ', '').replace('reallylikedit', '').strip()), errors="coerce")
    df['num_ratings'] = pd.to_numeric(df['minirating'].apply(lambda x: (x.split('— ')[1])).apply(lambda x: x.replace(' ratings', '').replace(',','')), errors="coerce")
    df['awards_count'] =  df['awards'].apply(lambda x:len(x))
    df['minmax_norm_rating'] = np.around(MinMaxScaler((1, 10)).fit_transform(df[['avg_rating']]), 2)
    df['mean_norm_ratings'] = np.around((1 + (df['avg_rating'] - df['avg_rating'].mean()) / (df['avg_rating'].max() - df['avg_rating'].min()) * 9), 2)
    df.drop('minirating', inplace=True, axis=1)
    df.drop('Unnamed: 0', inplace=True, axis=1)
    return df
