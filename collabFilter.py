import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

class Collaborate:
    def standardize(self,row):
        new_row=(row-row.mean())/(row.max()-row.min())
        return new_row

    def get_similar_movies(self,movie_name,user_rating):
        similar_score=item_similarity_df[movie_name]*(user_rating-2.5)
        similar_score=similar_score.sort_values(ascending=False)

ratings=pd.read_csv("./toy_dataset.csv",index_col=0)
ratings=ratings.fillna(0)  #clean data
ratings_std=ratings.apply(Collaborate().standardize)
item_similarity=cosine_similarity(ratings_std.T)    #item to item collab filter

item_similarity_df=pd.DataFrame(item_similarity,index=ratings.columns,columns=ratings.columns)
print(ratings_std)
print(item_similarity)


