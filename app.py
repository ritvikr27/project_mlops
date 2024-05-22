from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

#Load the dataset and models
movie_data= pd.read_csv('E:/MLOps Plaksha/project_mlops/movie_metadata.csv')
with open('E:/MLOps Plaksha/project_mlops/updated_tfidf_vectorizer.pkl', 'rb') as f:
    tfidf_vectorizer = pickle.load(f)
with open('E:/MLOps Plaksha/project_mlops/updated_cosine_sim_matrix.pkl', 'rb') as f:
    cosine_sim_matrix = pickle.load(f)

#Strip whitespace from movie titles
movie_data['movie_title']= movie_data['movie_title'].str.strip().str.lower()

def get_movie_recommendations(title, movie_data, cosine_sim_matrix):
    title = title.strip().lower()
    if title not in movie_data['movie_title'].values:
        return []

    idx = movie_data[movie_data['movie_title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movie_data.iloc[movie_indices][['movie_title', 'director_name', 'genres', 'imdb_score']].to_dict(orient='records')

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    recommendations = get_movie_recommendations(title, movie_data, cosine_sim_matrix)
    if not recommendations:
        return jsonify({'error': 'Movie not in the database, sorry!'}), 404
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
