import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def try_request(url):
    try:
        return requests.get(url)
    except:
        try_request(url)

def scrap_goodreads_table(pages, url, pos):
    t1 = time.time()
    check = lambda x: x if x is not None else BeautifulSoup("<p>NONE</p>", features='lxml')
    dic = {'Title_URL': [], 'Title': [], 'Author': [], 'minirating': [], 'num_reviews': [], 'num_pages': [], 'awards': [], 'genres': [], 'series': [], 'year_published': [], 'places': []}
    for i in range(1, pages + 1): # number of pages to scrap (100 positions per page)
        print("Scrapping page #" + str(i))
        page = try_request(url + '?page=' + str(i))
        soup = BeautifulSoup(page.content, 'html.parser')
        contents = [soup.findAll('a', class_='bookTitle'), soup.findAll('a', class_='authorName'), soup.findAll('span', class_='minirating')]
        if pos == 0:
            pos = len(contents[0])
        dic['Title'] += [contents[0][j].get_text().strip() for j in range(pos)]
        dic['Title_URL'] += ["https://www.goodreads.com" + contents[0][j]['href'] for j in range(pos)]
        dic['Author'] += [contents[1][j].get_text() for j in range(pos)]
        dic['minirating'] += [contents[2][j].get_text() for j in range(pos)]
    for i in range(len(dic['Title_URL'])):
        print("Assembling data on book #" + str(i))
        page = try_request(dic['Title_URL'][i])
        soup = BeautifulSoup(page.content, 'html.parser')
        html_targets = {'num_reviews': soup.find('meta', itemprop = 'reviewCount'), 'num_pages': soup.find('span', itemprop = 'numberOfPages'), 'awards': soup.find('div', itemprop = 'awards'), 'genres': BeautifulSoup(str(soup.findAll('a', class_ = 'actionLinkLite bookPageGenreLink')[:3]), features="lxml"), 'series': soup.find('h2', id = 'bookSeries'), 'year_published': soup.find('div', id = 'details'), 'places': soup.find('div', id = 'bookDataBox')}
        for column in list(dic.keys())[4:]:
            dic[column].append(check(html_targets[column]).get_text())
    t2 = time.time() - t1
    print("Time taken:", int(t2 // 60), "minutes and", int(t2 % 60), "seconds")
    return pd.DataFrame(dic)
