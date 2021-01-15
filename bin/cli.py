import click
import pandas as pd
from scrapper.scrapper import scrap_goodreads_table
from scrapper.preprocess import preprocessing
from res.charts import *

@click.group()
def cli():
    pass    

@click.command()
@click.option('--pages', default=1, help='number of pages to scrap')
@click.option('--f', default='csv', help='destination format: csv/json/pkl')
@click.option('--name', default='scrapped_data', help='name of your destination file')
@click.argument('url')
def scrap_table(pages, f, name, url):
    fn = name + '.' + f
    df = preprocessing(scrap_goodreads_table(pages, url))
    if f == 'csv':
        df.to_csv(fn)
    elif f == 'json':
        df.to_json(fn)
    elif f == 'pkl':
        df.to_pickle(fn)

@click.command()
@click.option('--corr', default=False, help='shows correlations between columns')
@click.option('--ratdist', default=False, help='shows rating distributions')
@click.argument('data')
def analyze(corr, ratdist, data):
    f = data[data.find('.') + 1:]
    supported_formats = ['csv', 'json', 'pkl'] 
    if f not in supported_formats: 
        raise ValueError(f"File format not supported. Supported formats: {supported_formats}")
    else:
        if f == 'csv':
            df = pd.read_csv(data)
        elif f == 'json':
            df = pd.read_json(data)
        elif f == 'pkl':
            df = pd.read_pickle(data)

    if corr:
        print(plot_correlation(df))
    
    if ratdist:
        
cli.add_command(scrap_table)
cli.add_command(analyze)

if __name__ == "__main__":
    cli()
