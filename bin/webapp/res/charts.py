import streamlit as st
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
    return place

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
    fig = st.vega_lite_chart(df, {"width": 600, "height": 500, 'mark': {'type': 'circle', 'tooltip': True},
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

# 8. Visualize the awards distribution in a boxplot and aggregtated bars. (in this case just boxplot)
def awards_boxplot(df):
    fig = px.violin(df, y="awards_count", box=True,  # draw box plot inside the violin
                    points='all',template='plotly_dark')
    fig.update_layout(title='Awards Count', margin=dict(l=40, r=40, t=40, b=40),
                      paper_bgcolor="rgb(93,93,93)", yaxis_range=[0,25],showlegend=True)

    fig.layout.width = 800
    fig.layout.height = 800
    return fig

# 9. "Group the books by original_publish_year and get the mean of the minmax_norm_ratings of the groups."
def yearly_minmax_mean(df):
    groupby_year = df.groupby(['year_published']).agg({'minmax_norm_rating': 'mean','Title':'max'}).reset_index()
    groupby_book = df.groupby(['Title']).agg({'minmax_norm_rating': 'mean'}).reset_index()

    fig = px.bar(groupby_year, x='year_published', y='minmax_norm_rating', color='Title', hover_data=['Title'], template='plotly_dark', opacity=0.7)
    fig.update_layout(title='Books, Publish year vs minmax_norm', margin=dict(l=40, r=40, t=40, b=40),
                      paper_bgcolor="rgb(93,93,93)", showlegend=False)
    fig.layout.width = 1200
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
