import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=e383c937ee1f2b20f566898de79c89af&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch posters from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


pickle_off = open(r"movies.pkl", "rb")
movies = pd.read_pickle(pickle_off)

pickle_off1 = open(r"similarity.pkl", "rb")
similarity = pd.read_pickle(pickle_off1)

st.title('Movies Recommender System')

selected_movie_name = st.selectbox(
    'what movie you like?',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Movie-1", "Movie-2", "Movie-3", "Movie-4", "Movie-5"])
    with tab1:
        st.header(names[0])
        st.image(posters[0])

    with tab2:
        st.header(names[1])
        st.image(posters[1])

    with tab3:
        st.header(names[2])
        st.image(posters[2])

    with tab4:
        st.header(names[3])
        st.image(posters[3])

    with tab5:
        st.header(names[4])
        st.image(posters[4])

