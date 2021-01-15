import pandas as pd
import numpy as np
import streamlit as sl
import scipy.stats as st
from tqdm import tqdm
import plotly.express as px
import plotly.figure_factory as ff


# plotly-themes->["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]

def authors_best(authorsName, df):
    authors_books = df[df['Author']==authorsName]
    authors_best_book = authors_books[authors_books.minmax_norm_rating == authors_books.minmax_norm_rating.max()]
    return (authors_best_book['Title'].to_string(header = False, index = False))

# Just to generate map
def place_title(bookName, df):
    authors_books = df[df['Title']==bookName]
    place = authors_books['places']
    return place.to_string(header = False, index = False)

# ---- Visualisations ---- 

# 1. Create a 2D scatterplot with pages on the x-axis and num_ratings on the y-axis.
def scatter_pages_num_rating(df):
    df=df.sample(n=200)
    # df['num_pages'] = df['num_pages'].sort_values()
    fig = px.scatter(df, x="num_pages", y="num_ratings",template='plotly_dark')  #  df['num_pages'].sort_values()
    fig.update_layout(title='pages vs num_ratings', paper_bgcolor="rgb(93,93,93)",
                      xaxis_range=[50,1400], yaxis_range=[0,1200000], showlegend=True)
    return fig

def plotly_line_vega(df):
    df['num_pages'] = df['num_pages'].sort_values()
    df= df.sample(n=200)
    fig = sl.vega_lite_chart(df, {"width": 600, "height": 500, 'mark': {'type': 'circle', 'tooltip': True},
                            'encoding': {'x': {'field': 'num_pages', 'type': 'quantitative'},
                                         'y': {'field': 'num_ratings', 'type': 'quantitative'}, }, })
    return fig

# 2. Can you compute numerically the correlation coefficient of these two columns (in this case whole dataframe)?
def plot_correlation(df):
    corr = df.corr()
    return corr.style.background_gradient(cmap='coolwarm')

# 3. Visualise the avg_rating distribution.
def avg_rating_dist(df):
    # marginal violin, rug
    fig = px.histogram(df, x="avg_rating", marginal="box", hover_data=df.columns, color_discrete_sequence=px.colors.qualitative.Dark24,
                       template='plotly_dark', opacity=1)
    fig.update_layout(title='avg_rating Distribution', margin=dict(l=40, r=40, t=40, b=40), paper_bgcolor="rgb(93,93,93)")
    return fig

# 4. Visualise the minmax_norm_rating distribution.
def minmax_norm_dist(df):
    # ['Alphabet','Antique','Bold','D3','Dark2','Dark24','G10']
    fig = px.histogram(df, x="minmax_norm_rating", marginal="box", hover_data=df.columns,
                       color_discrete_sequence=px.colors.qualitative.Antique, template='plotly_dark', opacity=0.7)
    fig.update_layout(title='minmax_norm_rating Distribution', margin=dict(l=40, r=40, t=40, b=40),
                      paper_bgcolor="rgb(93,93,93)")
    return fig

# 5. Visualise the `mean_norm_rating` distribution.
def mean_norm_dist(df):
    # ['Alphabet','Antique','Bold','D3','Dark2','Dark24','G10']
    fig = px.histogram(df, x="mean_norm_ratings", marginal="box", hover_data=df.columns,
                       color_discrete_sequence=px.colors.qualitative.Light24,template='plotly_dark', opacity=0.7)
    fig.update_layout(title='mean_norm_rating Distribution', margin=dict(l=40, r=40, t=40, b=40),
                      paper_bgcolor="rgb(93,93,93)")
    return fig

def all_three_dist(df):
    hist_data = [df['avg_rating'], df['minmax_norm_rating'], df['mean_norm_ratings']]
    group_labels = ['avg_rating', 'minmax_norm_rating', 'mean_norm_ratings']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels, bin_size=.3)
    fig.update_layout(title='All in one Distribution', margin=dict(l=40, r=40, t=40, b=40),
                      paper_bgcolor="rgb(93,93,93)")
    fig.layout.width=800
    fig.layout.height=500
    fig.layout.template='plotly_dark'
    return fig

# 6.
def norm_comparison(df):
    fig = px.scatter(df[['minmax_norm_rating','mean_norm_ratings']],labels=['minmax_norm_rating','mean_norm_ratings'], template='plotly_dark')

    fig.update_layout(title='minmax & mean norm rating', margin=dict(l=40, r=40, t=40, b=40),
                      paper_bgcolor="rgb(93,93,93)", showlegend=True)
    fig.layout.width = 800
    fig.layout.height = 500
    return fig

# 7. just show pngs on streamlit but not working
## 7. 
def fit_scipy_distributions(array, bins, xlabel='x label', ylabel='y label', plot_hist = True, plot_best_fit = True, plot_all_fits = False):
    
    if plot_best_fit or plot_all_fits:
        assert plot_hist, "plot_hist must be True if setting plot_best_fit or plot_all_fits to True"
    
    # Returns un-normalised (i.e. counts) histogram
    y, x = np.histogram(np.array(array), bins=bins)
    
    # Some details about the histogram
    bin_width = x[1]-x[0]
    N = len(array)
    x_mid = (x + np.roll(x, -1))[:-1] / 2.0 # go from bin edges to bin middles
    
    # selection of available distributions
    # CHANGE THIS IF REQUIRED
    DISTRIBUTIONS = [st.alpha,st.cauchy,st.cosine,st.laplace,st.levy,st.levy_l,st.norm, st.chi2]   #stats.chi2

    if plot_hist:
        fig = plt.figure(figsize=(15,12), facecolor='w')
        fig, ax = plt.subplots(facecolor = 'w')
        h = ax.hist(np.array(array), bins = bins, color = 'tab:olive')

    # loop through the distributions and store the sum of squared errors
    # so we know which one eventually will have the best fit
    sses = []
    for dist in tqdm(DISTRIBUTIONS):
        name = dist.__class__.__name__[:-4]

        params = dist.fit(np.array(array))
        arg = params[:-2]
        loc = params[-2]
        scale = params[-1]

        pdf = dist.pdf(x_mid, loc=loc, scale=scale, *arg)
        pdf_scaled = pdf * bin_width * N # to go from pdf back to counts need to un-normalise the pdf

        sse = np.sum((y - pdf_scaled)**2)
        sses.append([sse, name])

        # Not strictly necessary to plot, but pretty patterns
        if plot_all_fits:
            ax.plot(x_mid, pdf_scaled, label = name)
    
    if plot_all_fits:
        plt.legend(loc=1)

    # CHANGE THIS IF REQUIRED
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Things to return - df of SSE and distribution name, the best distribution and its parameters
    results = pd.DataFrame(sses, columns = ['SSE','distribution']).sort_values(by='SSE') 
    best_name = results.iloc[0]['distribution']
    best_dist = getattr(st, best_name)
    best_params = best_dist.fit(np.array(array))
    
    if plot_best_fit:
        new_x = np.linspace(x_mid[0] - (bin_width * 2), x_mid[-1] + (bin_width * 2), 1000)
        best_pdf = best_dist.pdf(new_x, *best_params[:-2], loc=best_params[-2], scale=best_params[-1])
        best_pdf_scaled = best_pdf * bin_width * N
        ax.plot(new_x, best_pdf_scaled, label = best_name)
        plt.legend(loc=1)
    
    if plot_hist:
        plt.show()
    
    return results, best_name, best_params
# 8. Visualize the awards distribution in a boxplot and aggregtated bars. (in this case just boxplot)
def awards_boxplot(df):
    fig = px.violin(df, y="awards_count", box=True,  # draw box plot inside the violin
                    points='all',template='plotly_dark')
    fig.update_layout(title='Awards Count', margin=dict(l=40, r=40, t=40, b=40),
                      paper_bgcolor="rgb(93,93,93)", yaxis_range=[0,25],showlegend=True)

    fig.layout.width = 800
    fig.layout.height = 500
    return fig

# 9. "Group the books by original_publish_year and get the mean of the minmax_norm_ratings of the groups."
def yearly_minmax_mean(df):
    groupby_year = df.groupby(['year_published']).agg({'minmax_norm_rating': 'mean','Title':'max'}).reset_index()
    groupby_book = df.groupby(['Title']).agg({'minmax_norm_rating': 'mean'}).reset_index()

    fig = px.bar(groupby_year, x='year_published', y='minmax_norm_rating', color='Title', hover_data=['Title'], template='plotly_dark', opacity=0.7)
    fig.update_layout(title='Books, Publish year vs minmax_norm', margin=dict(l=40, r=40, t=40, b=40),
                      paper_bgcolor="rgb(93,93,93)", showlegend=False)
    fig.layout.width = 800
    fig.layout.height = 500
    return fig

# 10.
def minmax_awards(df):
    df = df[df['minmax_norm_rating'].notna()]
    fig = px.scatter(data_frame=df, x="minmax_norm_rating", y="awards_count",    # size="Title", color="awards_count"
                     trendline='ols', hover_name='Title', opacity=0.9, template='plotly_dark', )
    #  marginal_x='histogram',
    #                      marginal_y='box'
    fig.update_layout(title='Y = (0.1218*minmax_norm_rating)-(2.6884*awards_count)-->R^2=0.0026', margin=dict(l=40, r=40, t=40, b=40),
                      paper_bgcolor="rgb(93,93,93)", showlegend=True)
    fig.layout.width = 800
    fig.layout.height = 500
    return fig


from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def minmax_awards_2(df, fig_size):
    df = df[df['minmax_norm_rating'].notna()]
    X = df['minmax_norm_rating'].values.reshape(-1, 1)
    y = df['awards_count'].values
    print(f"X.shape = {X.shape}")
    print(f"y.shape = {y.shape}\n=========================")

    # Train and Predict using linear regression
    lin_reg = LinearRegression()
    model_linreg = lin_reg.fit(X, y)
    print("The linear regression coefficient can be accessed in a form of class attribute with model.coef_")
    print("model coefficient = ", model_linreg.coef_, "\n==================================")
    print("The y-intercept can be accessed in a form of class attribute with model.intercept_")
    print(f"y-intercept = {model_linreg.intercept_}\n================================")
    y_prediction = model_linreg.predict(X)

    # Evaluate
    r2 = model_linreg.score(X, y)
    print(f"R-squared = {r2}")

    # Plot
    fig = plt.figure(10, fig_size)
    ax = plt.subplot()
    ax.plot(X, y_prediction, color='k', label='Bivariate Linear Regression')
    ax.scatter(X, y, edgecolor='k', color='c', label='Sample Data')
    ax.set_ylabel('awards_count', fontsize=14)
    ax.set_xlabel('minmax_norm_rating', fontsize=14)
    ax.text(0.8, 0.1, '', fontsize=13, ha='center', va='center',
            transform=ax.transAxes, color='gray')
    ax.legend(facecolor='white', fontsize=11)
    ax.set_title('$R^2= %.4f$' % r2, fontsize=18)
    ax.text(0.55, 0.15, '$y = %.4f x_1 - %.4f $' % (model_linreg.coef_[0], abs(model_linreg.intercept_)), fontsize=22,
            transform=ax.transAxes)

    return fig
