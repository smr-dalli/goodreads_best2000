import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def authors_best(authorsName, df):
    authors_books = df[df['Author']==authorsName]
    authors_best_book = authors_books[authors_books.minmax_norm_rating == authors_books.minmax_norm_rating.max()]
    return authors_best_book

def minmax_year(df):
    groupby_minmax = df.groupby('year_published')['minmax_norm_rating'].agg('mean')
    return groupby_minmax    

## Visualisations.
def plot_correlations(df):
    table = df.corr()
    x.style.background_gradient(cmap = 'coolwarm')
    return table

def scatter_pages_num_ratings(df, fig_size, sample):
    df = df.sample(n = sample)
    fig = plt.figure(1, fig_size) 
    plt.scatter(df.num_pages.sort_values(), df.num_ratings)
    plt.xlabel('Number of Pages')
    plt.ylabel('Number of Ratings')
    plt.title('2D Scatter plot for pages and ratings')
    print("Correlation:", df['avg_rating'].corr(df['num_ratings']))
    return fig

def avg_rating_dist(df, fig_size):
    fig = plt.figure(3, fig_size)
    sns.distplot(df.avg_rating)
    plt.xlabel('Average rating of the Books')
    plt.title('Average rating Distribution')
    return fig

def minmax_norm_dist(df, fig_size):
    fig = plt.figure(4, fig_size)
    sns.distplot(df.minmax_norm_rating, bins = 25,color='green')
    plt.xlabel('Minmax_norm rating of the Books')
    plt.title('Minmax_norm rating distribution')
    return fig

def mean_norm_dist(df, fig_size):
    fig = plt.figure(5, fig_size)
    sns.distplot(df.mean_norm_ratings, bins=25,color='orange')
    plt.xlabel('Mean_norm rating of the Books')
    plt.title('Mean_norm rating distribution')
    return fig

def norm_comparison(df, fig_size):
    fig = plt.figure(6, fig_size)
    ax = fig.add_subplot(111)
    df.minmax_norm_rating.plot(kind='kde', ax=ax, color='red')
    df.mean_norm_ratings.plot(kind='kde', ax=ax, color='green')
    ax.title.set_text('minmax_norm_rating and mean_norm_rating distributions')
    plt.xticks(np.arange(-4, 11))
    ax.legend()
    return fig

def awards_boxplot(df, fig_size):
    fig = plt.figure(8, fig_size)
    plt.boxplot(df.awards_count)
    plt.ylabel('number of awards')
    plt.title('Awards distribution')
    return fig

def yearly_minmax_mean(df, fig_size):
    df = minmax_year(df)
    fig = plt.figure(9, fig_size)
    plt.bar(x=df.index, height=df['minmax_norm_rating'])
    plt.xlabel('year of publishing')
    plt.ylabel('minmax_norm_rating mean')
    plt.title('Means of normalized ratings over the years.')
    return fig

from sklearn.linear_model import LinearRegression
def minmax_awards(df, fig_size):
    df = df[df['minmax_norm_rating'].notna()]
    X = df['minmax_norm_rating'].values.reshape(-1,1)
    y = df['awards_count'].values
    print(f"X.shape = {X.shape}")
    print(f"y.shape = {y.shape}\n=========================")

    # Train and Predict using linear regression
    lin_reg = LinearRegression()
    model_linreg = lin_reg.fit(X,y)
    print("The linear regression coefficient can be accessed in a form of class attribute with model.coef_")
    print("model coefficient = ", model_linreg.coef_,"\n==================================")
    print("The y-intercept can be accessed in a form of class attribute with model.intercept_")
    print(f"y-intercept = {model_linreg.intercept_}\n================================" )
    y_prediction = model_linreg.predict(X)

    # Evaluate
    r2 = model_linreg.score(X,y)
    print(f"R-squared = {r2}")
   
    # Plot
    fig = plt.figure(10, fig_size)
    ax = plt.subplot()
    ax.plot(X, y_prediction, color='k', label='Bivariate Linear Regression')
    ax.scatter(X,y, edgecolor='k', color='c', label='Sample Data')
    ax.set_ylabel('awards_count', fontsize=14)
    ax.set_xlabel('minmax_norm_rating', fontsize=14)
    ax.text(0.8,0.1,'', fontsize=13, ha='center', va='center',
    transform=ax.transAxes, color='gray')
    ax.legend(facecolor='white', fontsize=11)
    ax.set_title('$R^2= %.4f$' % r2, fontsize=18)
    ax.text(0.55, 0.15, '$y = %.4f x_1 - %.4f $' % (model_linreg.coef_[0], abs(model_linreg.intercept_)), fontsize=22, transform=ax.transAxes)
    
    return fig

if __name__ == '__main__':
    df = pd.read_pickle("Best_2000s_df.pkl")
    fig_size = (10, 10)
    fig = minmax_awards(df, fig_size)
    fig.show()
