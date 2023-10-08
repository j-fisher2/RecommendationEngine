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
        self.similar = pd.DataFrame()
        self.item_similarity_df = item_similarity_df  # Use self.item_similarity_df
        for movie, rating in self.ratings:
            self.similar = pd.concat([self.similar,Collaborate(self.item_similarity_df).get_similar_movies(movie, rating)], ignore_index=True)   
    def getSimilar(self):
        return self.similar

    

ratings = pd.read_csv("./toy_dataset.csv", index_col=0)
ratings = ratings.fillna(0)  # Clean data
ratings_std = ratings.apply(Collaborate(None).standardize)
item_similarity = cosine_similarity(ratings_std.T)  # Item-to-item collab filter

item_similarity_df = pd.DataFrame(item_similarity, index=ratings.columns, columns=ratings.columns)

user1 = User([("action1", 5), ("romantic2", 1), ("romantic3", 1)], item_similarity_df)
sim_movies = user1.getSimilar()
print(sim_movies)



