import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

#scrap data from title page
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

if __name__ == '__main__':
    octoparse = pd.read_csv('Best_Books_of_the_Decade__2000s__6922_books_.csv')
    octoparse = octoparse[:1000]
    urls = octoparse['Title_URL']
    scrapper(urls)
 
