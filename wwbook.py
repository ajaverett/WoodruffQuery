import streamlit as st

import pandas as pd
import altair as alt
import datetime as dt

st.title('WW Papers')
path = pd.read_csv("clean_final2.csv")
booksToShow = st.multiselect(label='Which Books?', options= path['book_title'].unique(),default=['Doctrine and Covenants','Alma'])

#path2 = path.query('internal_id in options').
prop_limit = st.slider('How Strict are the Matches?', 0, 100, 35)
    
displaydf = path.query('(book_title in @booksToShow) &( (probability *100) >= @prop_limit)')



st.dataframe(displaydf.filter(['date','text','verse_short_title','book_title','scripture_text'
]))

bardf = (displaydf.groupby('book_title')
         .verse_short_title.nunique().reset_index())

books = (alt.Chart(bardf)
         .mark_bar()
         .encode(
    y=alt.Y('book_title',axis=alt.Axis(title='Book Title')),
    x=alt.X('verse_short_title',axis=alt.Axis(title='Frequency of Book Reference'))
         )
)
st.altair_chart(books, use_container_width=True)

path['date'] = pd.to_datetime(path['date'])
path['year'] = path['date'].dt.year
cb = (path.query('book_title in @booksToShow')
      .groupby(['year','book_title'])
      .verse_short_title.nunique()
      .reset_index())    

st.text("Here\'s how these Books Compare Over the Years of Pres. Woodruff\'s Writing:")
        
# comparebooks = (alt.Chart(cb)
#                 .mark_line()
#                 .encode(
#     x=alt.X('year',axis=alt.Axis(title='Year of His Journal',format='d')),
#     y=alt.Y('verse_short_title',title='Number of Verses Referenced'),
#     color='book_title'
#                 )
# )

# st.altair_chart(comparebooks,use_container_width=True)

import plotly.express as px
# Create chart
comparebooks = px.line(cb, x='year', y='verse_short_title', color='book_title', 
                       title='Comparison of Number of Verses Referenced by Book and Year of His Journal',
                       labels={'year': 'Year of His Journal', 'verse_short_title': 'Number of Verses Referenced'})
comparebooks.update_layout(xaxis_tickformat = 'd')

# Display chart in Streamlit app
st.plotly_chart(comparebooks,use_container_width=True)


# streamlit run "C:/Users/spenc/Documents/GitHub/wasianwilford/White Guy/wwbook.py"