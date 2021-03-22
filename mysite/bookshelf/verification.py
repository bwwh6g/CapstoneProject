import pandas as pd
import os
import sys
import logging
import surprise
import random
from surprise.model_selection import cross_validate

root_dir = os.path.dirname(__file__)
dfs_path = os.path.join(root_dir, 'Data/datasets')
ratings_df = pd.read_csv(os.path.join(dfs_path, 'rating3.csv'), sep=',', encoding='latin-1',low_memory=False)
reader = surprise.Reader(rating_scale=(1, 10))
data = surprise.Dataset.load_from_df(ratings_df[['user_id', 'isbn', 'rating']], reader)
print("SVD:")
algo1 = surprise.SVD()
cross_validate(algo1, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
print("BaseLine:")
bsl_options = {'method': 'sgd',
               'n_epochs': 450,
               'learning_rate': 0.0015,
               }
algo2 = surprise.BaselineOnly(bsl_options=bsl_options)
cross_validate(algo2, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
print("NMF:")
algo3 = surprise.NMF()
cross_validate(algo3, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
print("CoClustering:")
algo4 = surprise.CoClustering()
cross_validate(algo4, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)