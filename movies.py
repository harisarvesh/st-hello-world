import streamlit as st
import pandas as pd
import textwrap
import difflib
import pickle

# Load data and similarity model
data=pd.read_csv('C:/Users/haris/Downloads/autismdiagnosis/Autism_Prediction/New folder (2)/movies.csv')
loaded_model=pickle.load(open('C:/Users/haris/Downloads/autismdiagnosis/Autism_Prediction/New folder/similarity.sav','rb'))

st.title('🎬 Movie Recommendation Web App')
movie_name = st.text_input("Enter the movie name")

if movie_name:
    list_titles = data['title'].tolist()
    close_match = difflib.get_close_matches(movie_name, list_titles)

    if not close_match:
        st.warning("⚠️ No close match found.")
    else:
        close = close_match[0]
        index_movie = data[data.title == close]['index'].values[0]
        movie_info = data.iloc[index_movie]

        st.subheader("🎥 Movie Details")
        st.write("**Title:**", movie_info['title'])
        st.write("**Description:**")
        st.text(textwrap.fill(str(movie_info['overview']), width=100))
        st.write("**Cast:**", movie_info['cast'])
        st.write("**Director:**", movie_info['director'])

        st.markdown("---")
        st.subheader("📺 More Like This:")

        similarity_score = list(enumerate(loaded_model[index_movie]))
        sorted_movie = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        

i = 1
for movie in sorted_movie:
    index = movie[0]
    
    if index != index_movie and i <=6:
        movie_row = data.iloc[index]
        st.markdown(f"**{i}. {movie_row['title']}**")
        st.text(textwrap.fill(str(movie_row['overview']), width=100))
        st.markdown("---")
        i += 1

