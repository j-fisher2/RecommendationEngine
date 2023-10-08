import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

class Collaborate:
    def __init__(self, item_similarity_df):
        self.item_similarity_df = item_similarity_df
    
    def standardize(self, row):
        new_row = (row - row.mean()) / (row.max() - row.min())
        return new_row

    def get_similar_movies(self, movie_name, user_rating):
        similar_scores = self.item_similarity_df[movie_name]  # Use self.item_similarity_df
        
        # Calculate the adjusted similar scores
        similar_scores = similar_scores * (user_rating - 2.5)
        
        # Sort the similar scores in descending order
        similar_scores = similar_scores.sort_values(ascending=False)
        
        return similar_scores
        

class User:
    def __init__(self, movie_ratings, item_similarity_df):
        self.ratings = movie_ratings
        self.similar = pd.DataFrame()  # Initialize an empty DataFrame to store similar movies and scores
        self.item_similarity_df = item_similarity_df
        for movie, rating in self.ratings:
            similar_movies = Collaborate(self.item_similarity_df).get_similar_movies(movie, rating)
            similar_movies = pd.DataFrame(similar_movies, columns=[movie])  # Create a DataFrame for each movie and its scores
            self.similar = pd.concat([self.similar, similar_movies], axis=1)  # Concatenate the DataFrames along columns

    def getTopRecommendations(self, num_recommendations=5):
        # Sum the similarity scores for all movies
        total_scores = self.similar.sum(axis=1)
        # Sort movies by total_scores in descending order and return the top recommendations
        top_recommendations = total_scores.sort_values(ascending=False).head(num_recommendations)
        return top_recommendations

    

ratings = pd.read_csv("./toy_dataset.csv", index_col=0)
ratings = ratings.fillna(0)  # Clean data
ratings_std = ratings.apply(Collaborate(None).standardize)
item_similarity = cosine_similarity(ratings_std.T)  # Item-to-item collab filter


item_similarity_df = pd.DataFrame(item_similarity, index=ratings.columns, columns=ratings.columns)

user1 = User([("action1", 5),("action2",3)], item_similarity_df)
recommendations=user1.getTopRecommendations(3)
print(recommendations)



