import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import requests
from bs4 import BeautifulSoup
import time

def scrapper(urls):
    t1 = time.time()
    dic = {'num_reviews': [], 'num_pages': [], 'awards': [], 'genres': [], 'series': [], 'year_published': [], 'places': []}
    for i in range(1000):
        print('Processing position:', i)
        page = requests.get(urls[i])
        soup = BeautifulSoup(page.content, 'html.parser')

        try:
            reviews = soup.find('meta', itemprop = 'reviewCount').get_text().replace(',', '').strip()
            num_reviews = int(reviews[:reviews.find('\n')])
        except:
            reviews = '.'
        dic['num_reviews'].append(num_reviews)

        try:
            num_pages = soup.find('span', itemprop = 'numberOfPages').get_text()
            num_pages = int(num_pages[:num_pages.find(' ')])
        except:
            num_pages = '-'
        dic['num_pages'].append(num_pages)

        try:
            awards = soup.find('div', itemprop = 'awards').get_text().strip()
            awards = awards.split(',')
            awards_parsed = []
            for x in awards:
                awards_parsed.append(x[:x.find(')') + 1])
        except:
            awards = '-'
        dic['awards'].append(awards_parsed)

        try:
            genres = soup.findAll('a', class_ = 'actionLinkLite bookPageGenreLink')
            genres = [x.get_text() for x in genres][:3]
        except:
            genres = '-'
        dic['genres'].append(genres)

        try:
            series = soup.find('h2', id = 'bookSeries').get_text()
            if len(series) > 1:
                series = True
            else:
                series = False
        except:
            series = '-'
        dic['series'].append(series)

        try:
            year = soup.find('div', id = 'details').get_text().strip().split()
            year = [int(x) for x in year[year.index('Published'):year.index('Published') + 5] if x.isnumeric() and len(x) == 4]
        except:
            year = '-'
        dic['year_published'].append(year[0])

        try:
            pl = soup.find('div', id = 'bookDataBox').get_text().split('\n')
            places = ''
            f = False
            for x in pl:
                if x == 'Literary Awards':
                    break

                if f == True:
                    if len(x) > 1:
                        places += x + ' '

                if x == 'Setting':
                    f = True
        except:
            places = '-'
        dic['places'].append(places)

    df2 = pd.DataFrame(dic)
    result = pd.concat([df, df2], axis=1).to_csv('Best_2000s.csv')
    t2 = time.time()
    time_total = t2 - t1
    print("Time taken: ", int(time_total), " seconds.")
    return df2

def clean_data(df):
    ## parse minirating column to get avg_rating and num_ratings
    df['avg_rating'] = df['minirating'].apply(lambda x: (x.split('— ')[0]))
    df['avg_rating'] = df['avg_rating'].apply(lambda x: x.replace(' avg rating', ''))
    df['avg_rating'] = df['avg_rating'].apply(lambda x: x.replace(' ', '').replace('reallylikedit', '').strip())
    df['num_ratings'] = df['minirating'].apply(lambda x: (x.split('— ')[1]))
    df['num_ratings'] = df['num_ratings'].apply(lambda x: x.replace(' ratings', '').replace(',',''))

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

    # normalization 1 - 10
    scaler = MinMaxScaler((1, 10))
    df['minmax_norm_rating'] = scaler.fit_transform(df[['avg_rating']])
    df['mean_norm_ratings'] = 1 + (df['avg_rating'] - df['avg_rating'].mean()) / (df['avg_rating'].max() - df['avg_rating'].min()) * 9
    
    # rounding the values
    df['minmax_norm_rating'] = df['minmax_norm_rating'].apply(lambda x:round(x, 2))
    df['mean_norm_ratings'] = df['mean_norm_ratings'].apply(lambda x:round(x,2))
    
    return df

def authors_best(authorName, df):
    authors_books = df[df['Author']==authorName]
    authors_best_book = authors_books[authors_books.minmax_norm_rating == authors_books.minmax_norm_rating.max()]
    return authors_best_book

def analyse(df):
    groupby_minmax = df.groupby('year_published')['minmax_norm_rating'].agg('mean')
    return groupby_minmax    

if __name__ == '__main__':
    # Scrap 1000 books to csv.
    '''
    octoparse = pd.read_csv('Best_Books_of_the_Decade__2000s__6922_books_.csv')
    octoparse = octoparse[:1000]
    urls = octoparse['Title_URL']
    scrapper(urls)
    ''' 
    df = pd.read_csv('Best_2000s.csv')
    books = preprocessing(df)
    group_by_year = analyse(books)
    print(group_by_year)
