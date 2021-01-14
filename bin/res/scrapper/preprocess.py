import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sklearn.preprocessing import MinMaxScaler

def clean_data(df):
    df['num_reviews'] = list(map(lambda x: int(x[0]) if len(x) > 1 else 0, [x.replace(',','').replace('NONE', '0').split() for x in df['num_reviews']] ))
    df['num_pages'] = [int(x.replace('NONE', '0').replace('','0')[:x.find('p')]) for x in df['num_pages']]
    df['awards'] = [x.strip().split(',')[:x.find(')') + 1] for x in df['awards']]
    df['series'] = list(map(lambda x: True if len(x) > 1 else False, df['series']))
    yr = [x.strip().split() for x in df['year_published']]
    years = []
    for y in yr:
        if 'Published' in y:
            years.append([int(x) for x in y[y.index('Published'):y.index('Published') + 5] if x.isnumeric() and len(x) == 4][0])
        else:
            years.append(0)
    df['year_published'] = years
    to_parse = [x.split('\n') for x in df['places']]
    place_list = []
    for row in to_parse:
        f = False
        places = ''
        for line in row:
            if line == 'Literary Awards':
                break
            if f == True:
                if len(line) > 1:
                    places += line.strip() + ' | '
            if line == 'Setting':
                f = True
        place_list.append(places)
    df['places'] = place_list

    return df
   
def preprocessing(df):
    df = clean_data(df)
    
    ## parse minirating column to get avg_rating and num_ratings
    df['avg_rating'] = df['minirating'].apply(lambda x: (x.split('— ')[0]))
    df['avg_rating'] = df['avg_rating'].apply(lambda x: x.replace(' avg rating', ''))
    df['avg_rating'] = df['avg_rating'].apply(lambda x: x.replace(' ', '').replace('reallylikedit', '').strip())
    df['num_ratings'] = df['minirating'].apply(lambda x: (x.split('— ')[1]))
    df['num_ratings'] = df['num_ratings'].apply(lambda x: x.replace(' ratings', '').replace(',',''))

    df.drop('minirating', inplace=True, axis=1)
    df.drop('Unnamed: 0', inplace=True, axis=1)

    ## create awards_count
    df['awards'] = df['awards'].astype(str)
    awa_split = df['awards'].apply(lambda x:x.split(","))
    awa_count = awa_split.apply(lambda x:len(x))
    df['awards_count'] = awa_count
    
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
    df = preprocessing(pd.read_csv('raw_scrap.csv'))
    df.to_pickle("Best_00s.pkl")
    df.to_csv("Best_00s.csv")
