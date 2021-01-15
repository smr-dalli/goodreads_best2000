#!/usr/bin/env python
# coding: utf-8

# In[15]:


# Start writing code here...
import streamlit as st
from PIL import Image
import pandas as pd
import datetime

#Sidebar

#st.set_page_config(layout="wide")
image = Image.open('PromoHP1_Minerva_McGonagall_2.jpg')
st.sidebar.image(image, width = 300, height = 200)
st.sidebar.title('Team McGonagall')
st.sidebar.header("Build Week 1")
today = st.sidebar.date_input("Presentation day is", datetime.datetime.now())
st.sidebar.subheader("""Players:\n
Marcin Szleszynski [click](https://github.com/martinezpl)\n
Saurabh Satasia [click](https://github.com/saurabhsatasia)\n
Sai Mohan Reddy Dalli [click](https://github.com/smr-dalli)""")
st.sidebar.subheader('Our Sponsors:')
st.sidebar.markdown("""Jan Carbonell [click](https://github.com/jcllobet)\n
Antonnio Marsella [click](https://github.com/AntonioMarsella)""")

#Title
st.header('Welcome to our webpage, we are happy to see you:)')
image = Image.open('Goodreads-Logo-1024x576-7abf5bd8d98b9d10.jpg')
st.image(image,width = 900,height = 200)
st.subheader('Wonder!! what is Good reads is all about?, [click here](https://www.youtube.com/watch?v=SnjlL4St_W4) for '
             'a brief introduction.')
st.header('Tasks for the Build Week 1')
st.markdown("""1. From the [Good reads website](https://www.goodreads.com/), scrap the first 1000 [Best Books 
list of the Decade: 2000s](https://www.goodreads.com/list/show/5.Best_Books_of_the_Decade_2000s/). The dataframe 
looks like [this..](https://github.com/martinezpl/goodreads_best2000/blob/main/pngs/orginal_df.PNG).\n 2. Cleaning 
the dataset by dropping the NAN values to a readable pandas dataframe.\n 3. Calculating the Min max norm rating and 
Mean max norm rating for the data consistency. The dataframe looks like [this..]( 
https://github.com/martinezpl/goodreads_best2000/blob/main/pngs/Minmax_mean_norm_rating_df.PNG).\n 4. Analysing the 
data by grouping particular columns to find the relation among the other columns. The dataframe looks like [this..]( 
https://github.com/martinezpl/goodreads_best2000/blob/main/pngs/Analysis.PNG).\n 5. Visulaisation of the dataframe 
columns for the better interpretation of the data using plotly.""")
st.markdown("""This is the [README.md](https://github.com/martinezpl/goodreads_best2000/blob/main/README.md) file for the overview of the build week.""")

#dataset
df = pd.read_csv('Best_00s.csv')
st.header("Click on 'Display the data' below to look at the complete dataframe:")
if st.button("Display the data !!!"):
    st.dataframe(df)
st.markdown("""Large data to read?, you can filter to access individual columns here:""")
st.subheader("Filter by columns")
column = st.multiselect("Select the columns you want to display.",df.columns)

st.subheader("Filter out the books by number of awards and number of pages:")
threshold = st.slider('Number of awards:',5,40)
filtered = df[df.awards_count >=threshold]
st.dataframe(filtered[column])
threshold1 = st.slider('Number of pages:',200,1000)
filtered1 = df[df.num_pages >= threshold1]
st.dataframe(filtered1[column])

st.subheader("About Team McGonagall:")
"We are strives and we love to publish our articles to help developers with the useful data. Follow us on [Github](" \
"https://github.com/martinezpl/goodreads_best2000) for more exciting projects. All the best for your future endeavors! "

st.subheader(" Do you find this page interesting? ")
x = [1,2,3,4,5]
rate = st.multiselect('On a scale of 1 - 5, how informative is this website?',x)
st.subheader("Leave a comment:")
st.text_area('Thank you for your participation:)','Type here..')
st.button('Post comment')




