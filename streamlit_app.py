import streamlit as st
import requests


#Custom CSS for styling
#st.markdown("""
#    <style>
#    .main {
#        background-color: #f5f5f5;
#        color: #333;
#    }
#    h1 {
#        color: #ff6347;
#    }
#    .stButton>button {
#        background-color: #4CAF50;
#        color: white;
#    }
#    .stTextInput>div>div>input {
#        background-color: #e0f7fa;
#        color: #000;
#    }
#    </style>
#    """, unsafe_allow_html=True)


#Streamlit app content
st.title('Movie Recommendation System')

movie_title = st.text_input('Enter a movie title:')

if st.button('Get Movie Recommendations'):
    response = requests.get('http://localhost:5000/recommend', params={'title': movie_title})
    if response.status_code == 200:
        recommendations = response.json()['recommendations']
        st.write(f"Recommended movies based on '{movie_title}':")
        
        for movie in recommendations:
            st.markdown(f"""
            <div style="border: 2px solid #4CAF50; padding: 10px; margin: 10px 0; border-radius: 10px;">
                <strong>Title:</strong> {movie['movie_title'].title()}<br>
                <strong>Director:</strong> {movie['director_name']}<br>
                <strong>Genres:</strong> {movie['genres']}<br>
                <strong>IMDb Score:</strong> {movie['imdb_score']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write('Movie not in the database, sorry!')