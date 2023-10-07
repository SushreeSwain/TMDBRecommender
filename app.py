import streamlit as st
import pickle
import pandas as pd

# Load movie data and similarity matrix
movies_list = pickle.load(open("movies.pkl", 'rb'))
movies_list = movies_list['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Page title and subtitle
st.title("FILM RECOMMENDER SYSTEM")
st.markdown("<p class='center-align' style='font-size: 30px; font-weight: bold;'>Explore the world of cinema</p>",
            unsafe_allow_html=True)

# Create a search box with a dropdown menu
selected_movie = st.selectbox("Search for a movie:", movies_list)

# Display the selected movie
if selected_movie:
    st.write("You selected:", selected_movie)


# Function to recommend similar films
def recommend(movie, num_recommendations=5):
    movie_index = list(movies_list).index(movie)
    distances = similarity[movie_index]
    movie_scores = [(i, score) for i, score in enumerate(distances) if i != movie_index]
    movie_scores.sort(key=lambda x: x[1], reverse=True)
    recommended_films = [movies_list[i[0]] for i in movie_scores[:num_recommendations]]
    return recommended_films

if selected_movie:
    num_recommendations = 5  # Number of initial recommendations
    recommended_films = recommend(selected_movie, num_recommendations)

    if recommended_films:
        st.markdown(f"<p class='center-align uppercase-title'>{num_recommendations} RECOMMENDED FILMS</p>",
                    unsafe_allow_html=True)
        for film in recommended_films:
            st.write(film)

# Create a centered button to show more recommendations
show_more_button = st.button("Show 10 more recommendations")
# Display additional recommendations when the button is clicked
if show_more_button and selected_movie:
    num_recommendations += 10  # Increase the number of recommendations
    additional_recommendations = recommend(selected_movie, num_recommendations)

    # Add a faded line after the initial recommendations
    st.markdown("<hr class='faded-line'>", unsafe_allow_html=True)

    st.markdown(f"<p class='center-align uppercase-title'>10 MORE RECOMMENDATIONS</p>", unsafe_allow_html=True)
    for film in additional_recommendations[num_recommendations - 10:]:
        st.write(film)

st.markdown("<hr class='faded-line'>", unsafe_allow_html=True)

movies_df = pickle.load(open("movies.pkl", 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown("<hr class='faded-line'>", unsafe_allow_html=True)

# Create a text input box for entering the name of a crew member
selected_crew = st.text_input("Enter the name of an actor, director, or crew member:")


# Function to recommend movies by crew member
def recommend_by_crew(name, num_recommendations=4):
    relevant_movies = movies_df[movies_df['tags'].str.contains(name, case=False)]

    if relevant_movies.empty:
        st.write(f"No movies found for {name}.")
        return

    movie_indices = relevant_movies.index
    similarity_scores = similarity[movie_indices].sum(axis=0)
    movie_scores = [(i, score) for i, score in enumerate(similarity_scores)]
    movie_scores.sort(key=lambda x: x[1], reverse=True)
    top_recommendations = [movies_df.iloc[i[0]]['title'] for i in movie_scores[:num_recommendations]]

    return top_recommendations


# Display recommendations when a crew member's name is entered
if selected_crew:
    recommended_movies = recommend_by_crew(selected_crew)

    if recommended_movies:
        st.markdown(f"<p class='center-align uppercase-title'>RECOMMENDED FILMS FOR {selected_crew.upper()}</p>",
                    unsafe_allow_html=True)
        for film in recommended_movies:
            st.write(film)

st.markdown("<hr class='faded-line'>", unsafe_allow_html=True)
