import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def clean_data(df):
    ## parse minirating column to get avg_rating and num_ratings
    df['avg_rating'] = df['minirating'].apply(lambda x: (x.split('— ')[0]))
    df['avg_rating'] = df['avg_rating'].apply(lambda x: x.replace(' avg rating', ''))
    df['avg_rating'] = df['avg_rating'].apply(lambda x: x.replace(' ', '').replace('reallylikedit', '').strip())
    df['num_ratings'] = df['minirating'].apply(lambda x: (x.split('— ')[1]))
    df['num_ratings'] = df['num_ratings'].apply(lambda x: x.replace(' ratings', '').replace(',',''))

    ## get rid of obsolete columns
    df = df.replace('-', np.nan)
    df.drop('minirating', inplace=True, axis=1)
    df.drop(['Unnamed: 0', 'Number'], axis=1, inplace=True)
   
    ## create awards_count
    df['awards'] = df['awards'].astype(str)
    awa_split = df['awards'].apply(lambda x:x.split(","))
    awa_count = awa_split.apply(lambda x:len(x))
    df['awards_count'] = awa_count
    
    return df

def preprocessing(df):
    df = clean_data(df)
    df.avg_rating = pd.to_numeric(df.avg_rating, errors="coerce")
    df.num_ratings = pd.to_numeric(df.num_ratings, errors="coerce")
    df['num_pages'] = df['num_pages'].apply(lambda x: int(x) if x is not np.nan else np.nan) 
    
    # normalization 1 - 10
    scaler = MinMaxScaler((1, 10))
    df['minmax_norm_rating'] = scaler.fit_transform(df[['avg_rating']])
    df['mean_norm_ratings'] = 1 + (df['avg_rating'] - df['avg_rating'].mean()) / (df['avg_rating'].max() - df['avg_rating'].min()) * 9
    
    # rounding the values
    df['minmax_norm_rating'] = df['minmax_norm_rating'].apply(lambda x:round(x, 2))
    df['mean_norm_ratings'] = df['mean_norm_ratings'].apply(lambda x:round(x,2))
    
    return df

if __name__ == '__main__':
    preprocessing(pd.read_csv('Best_2000s.csv')).to_pickle("Best_2000s_df.pkl")
