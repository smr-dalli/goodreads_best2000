import streamlit as st
from PIL import Image
import pandas as pd
import datetime
from geopy.geocoders import Nominatim
from res.charts import *
from res.bg import set_png_as_page_bg
from style import *
def st_app():
    #Sidebar
    st.balloons()
    set_png_as_page_bg('res/hog-1.png')
    image = Image.open('PromoHP1_Minerva_McGonagall_2.jpg')
    st.sidebar.image(image, width=300, height=200)
    st.sidebar.markdown(html_temp_1.format("Team: McGonagall"), unsafe_allow_html=True)
    st.sidebar.header("Build Week 1")
    today = st.sidebar.date_input("Presentation day: ", datetime.datetime.now())
    st.sidebar.subheader("Players:")
    st.sidebar.markdown("""
    * [Marcin Szleszynski](https://github.com/martinezpl)
    * [Saurabh Satasia](https://github.com/saurabhsatasia)
    * [Sai Mohan Reddy Dalli](https://github.com/smr-dalli)""")
    st.sidebar.subheader('Our Sponsors:')
    st.sidebar.markdown("""* [Jan Carbonell](https://github.com/jcllobet)
* [Antonnio Marsella](https://github.com/AntonioMarsella)""")

    # Title
    st.header('Welcome to our webpage, make yourself at home :)')
    image = Image.open('Goodreads-Logo-1024x576-7abf5bd8d98b9d10.jpg')
    st.image(image, width=900, height=200)
    st.header("""Like what you see? \n For CLI goodreads scrapper, analyzing tools and more fun stuff check out the [source code](https://github.com/martinezpl/goodreads_best2000).""")

    # dataset
    df = pd.read_csv('Best_00s.csv', index_col=[0])
    st.markdown(html_temp_2.format("Best books of the decade: 2000"), unsafe_allow_html=True)
    st.header("Click on 'Display the data' below to look at the complete dataframe:")
    if st.button("Display the data."):
        st.dataframe(df.style.set_properties(**{'background-color': 'gray', 'color': 'white', 'border-color': 'blue'}))
    st.markdown("""Use filters to access individual columns here:""")
    st.subheader("Filter by columns")
    column = st.multiselect("Select the columns you want to display.", df.columns)
#########################################

    threshold = st.slider('Number of awards:',5,40)
    filtered = df[df.awards_count >=threshold]
    st.dataframe(filtered[column].style.set_properties(**{'background-color': 'gray', 'color': 'white', 'border-color': 'blue'}))

    threshold1 = st.slider('Number of pages:',200,1000)
    filtered1 = df[df.num_pages >= threshold1]
    st.dataframe(filtered1[column].style.set_properties(**{'background-color': 'gray', 'color': 'white', 'border-color': 'blue'}))

    # threshold = st.slider('Number of awards:', 5, 40)
    # filtered = df[df.awards_count >= threshold]
    # st.dataframe(filtered[column].style.set_properties(**{'background-color': 'gray', 'color': 'white', 'border-color': 'blue'}))

    str2= 'Find out what is the best book of an author.'
    st.subheader(str2)
    # st.markdown(html_temp_4.format(str2),unsafe_allow_html=True)
    col3,col4 = st.beta_columns(2)
    with col3: auth = st.selectbox("Select Author", df['Author'].unique().tolist())
    with col4: st.success(authors_best(auth, df))

    str_m = "Books and Places."
    st.subheader(str_m)
    # st.markdown(html_temp_3.format(str_m), unsafe_allow_html=True)
    book = st.selectbox("Select Book", df['Title'].unique())
    df_res = (place_title(book, df))
    place = st.success(df_res)
    """### *Type the Location you received above*"""
    where = st.text_area("\n", " Type here...")
    if st.button("Submit"):
        geolocator = Nominatim(user_agent="a")
        location = geolocator.geocode(where)
        lat = location.latitude
        lon = location.longitude
        map_df = pd.DataFrame.from_dict({"lat": [lat], "lon": [lon]})
        st.map(map_df)



    st.markdown("""\n\n""")
    st.markdown("""**------------------------------------------------------------------------------------------------------------**""")

    # ANALYSIS
    ## EX-1
    st.markdown(html_temp_3.format("ANALYSIS"), unsafe_allow_html=True)
    st.markdown("""\n\n\n""")
    str1= "1. Group the books by `original_publish_year` and get the mean of the `minmax_norm_ratings` of the groups."
    st.markdown(html_temp_4.format(str1),unsafe_allow_html=True)
    # st.info("""### *1. Group the books by `original_publish_year` and get the mean of the `minmax_norm_ratings` of the groups.*""")
    groupby_minmax = df.groupby('year_published').agg({'minmax_norm_rating':'mean'})
    col1,col2 = st.beta_columns([2,4])
    groupby_minmax = groupby_minmax.style.set_properties(**{'background-color': 'gray', 'color': 'white', 'border-color': 'blue'})
    with col1: st.dataframe(groupby_minmax)
    with col2: st.area_chart(groupby_minmax)


    st.markdown("""**------------------------------------------------------------------------------------------------------------**""")

    st.markdown(html_temp_3.format("VISUALIZATION"),unsafe_allow_html=True)
    st.markdown("""\n\n\n""")

    # EX-1
    str3='1. Create a 2D scatterplot with `pages` on the x-axis and `num_ratings` on the y-axis.'
    st.markdown(html_temp_4.format(str3),unsafe_allow_html=True)
    ex_1 = scatter_pages_num_rating(df)
    st.plotly_chart(ex_1)
    # st.subheader("Same plot using Streamlit-line_vega_chart")
    # plotly_line_vega(df)
    st.markdown("""\n\n\n\n""")
    # EX-2
    str4='2. Can you compute numerically the correlation coefficient of these two columns?'
    st.markdown(html_temp_4.format(str4),unsafe_allow_html=True)
    st.write(plot_correlation(df))
    st.markdown("""\n\n\n\n""")

    # EX-3
    str5 = '3. Visualise the `avg_rating` distribution.'
    st.markdown(html_temp_4.format(str5),unsafe_allow_html=True)
    ex_3 = avg_rating_dist(df)
    st.plotly_chart(ex_3)
    st.markdown("""\n\n\n\n""")

    # EX-4
    str6 = '4. Visualise the `minmax_norm_rating` distribution.'
    st.markdown(html_temp_4.format(str6),unsafe_allow_html=True)
    st.plotly_chart(minmax_norm_dist(df))
    st.markdown("""\n\n\n\n""")

    # EX-5
    str7 = '5. Visualise the `mean_norm_rating` distribution.'
    st.markdown(html_temp_4.format(str7),unsafe_allow_html=True)
    st.plotly_chart(mean_norm_dist(df))
    st.plotly_chart(all_three_dist(df))
    st.markdown("""\n\n\n\n""")

    # EX-6
    str8 = '6. Create one graph that represents in the same figure both `minmax_norm_rating` and `mean_norm_rating` distributions.'
    st.markdown(html_temp_4.format(str8),unsafe_allow_html=True)
    st.plotly_chart(norm_comparison(df))
    st.markdown("""\n\n\n\n""")

    # EX-8
    str9 = '8. Visualize the awards distribution in a boxplot and aggregtated bars.'
    st.markdown(html_temp_4.format(str9),unsafe_allow_html=True)
    st.plotly_chart(awards_boxplot(df))
    st.markdown("""\n\n\n\n""")

    # EX-9
    str10 = 'Group the `books` by `original_publish_year` and get the mean of the `minmax_norm_ratings` of the groups.'
    st.markdown(html_temp_4.format(str10),unsafe_allow_html=True)
    st.plotly_chart(yearly_minmax_mean(df))
    st.markdown("""\n\n\n\n""")

    # EX-10
    str11 = 'Make a scatterplot to represent minmax_norm_ratings in function of the number of awards won by the book.'
    st.markdown(html_temp_4.format(str11),unsafe_allow_html=True)
    st.plotly_chart(minmax_awards(df))  #
    # st.pyplot(minmax_awards_2(df,fig_size=(10,10))) ## Old matplotlib plot
    st.markdown("""\n\n\n\n""")

    # EX-7 Not working
    # str12='What is the best fit in terms of a distribution (normal, chi-squared...) to represent each of those graphs?'
    # st.markdown(html_temp_2.format(str12), unsafe_allow_html=True)
    # st.image("D:/Strive/st/goodreads_best2000-main/pngs/distribution_fit.png")

    st.markdown("""**------------------------------------------------------------------------------------------------------------**""")

    # Explore maps in streamlit

    st.markdown("""**------------------------------------------------------------------------------------------------------------**""")

    # st.markdown(html_temp_2.format("About Team McGonagall:"), unsafe_allow_html=True)
    st.subheader("About Team McGonagall:")
    "We are strives and we love to publish our articles to help developers with the useful data. Follow us on [Github](" \
    "https://github.com/martinezpl/goodreads_best2000) for more exciting projects. All the best for your future endeavors! "

    st.subheader(" Do you find this page interesting? ")
    x = [1, 2, 3, 4, 5]
    rate = st.multiselect('On a scale of 1 - 5, how informative is this website?', x)
    st.subheader("Leave a comment:")
    st.text_area('Thank you for your participation:)', 'Type here..')
    st.button('Post comment')

if __name__ == "__main__":
    st_app()

