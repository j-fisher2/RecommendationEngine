import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq

def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]

def combine_features(row):
	return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']

def getSimilar(cosine_sim,movie_idx):
	row=cosine_sim[movie_idx]
	row=[(-v,i) for i,v in enumerate(row)]
	heapq.heapify(row)
	res=[]
	for i in range(21):
		most_similar=heapq.heappop(row)
		if i==0:
			continue
		res.append(get_title_from_index(most_similar[1]))
	return res

movie_list=set()
		

df=pd.read_csv("movie_dataset.csv")

##Select Features
features=['keywords','cast','genres','director']
for feature in features:
	df[feature]=df[feature].fillna('')


df['target features']=df.apply(combine_features,axis=1)

#Create count matrix
cv=CountVectorizer()
count_matrix=cv.fit_transform(df['target features'])

#Compute the Cosine Similarity based on the count_matrix
cosine_sim=cosine_similarity(count_matrix)

movie_user_likes = "Transformers"

movie_idx=get_index_from_title(movie_user_likes)

similar_movies=getSimilar(cosine_sim,movie_idx)
print(similar_movies)
