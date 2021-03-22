

import pandas as pd
import os
import sys
import logging
import surprise
import random
import time




class recommender:

    def __init__(self):
        self.root_dir = os.path.dirname(__file__)
        self.dfs_path = os.path.join(self.root_dir, 'Data/datasets')
        self.model_path = os.path.join(self.root_dir, 'Data/model.pickle')
        self.items_df, self.ratings_df = self.load_dfs()
        self.pos, self.neg = ['y', 'yes', 'Y', 'Yes'], ['n', 'no', 'N', 'No']
        self.nof_user_ratings = self.ratings_df.user_id.value_counts()


        self.min_nof_ratings = 1
        self.ratings_changed = False
        self._algo_choise = 'SVD'  # Here select the training algorithm SVD Baseline NMF or KNNBasic
        # Check if there is a pre-trained model
        try:
            _, self.algorithm = surprise.dump.load(self.model_path)   # Load the pre-trained model
        except:
            logging.error(('\nInitialize...position %s no model found"model.pickle".\n请加入模型'), self.model_path)

    def transToList(self, items):
        Res = []
        name = items.columns.values.tolist()
        for i, item in enumerate(items.iterrows()):
            pass
            row = dict.fromkeys(name)
            for n in name:
                # print(item[n])
                row[n] = item[1][n]
                pass
            Res.append(row)
        return Res

    def build_trainset(self):  #Building training set
        reader = surprise.Reader(rating_scale=(1, 10))
        data = surprise.Dataset.load_from_df(self.ratings_df[['user_id', 'isbn', 'rating']], reader)
        self.trainset = data.build_full_trainset()

    def build_recset(self, trainset, fill=None):  #Building test set
        trainset = self.trainset
        fill = trainset.global_mean if fill is None else float(fill)
        recset = []

        u = trainset.to_inner_uid(self.user_Id)
        user_items = set([j for (j, _) in trainset.ur[u]])
        recset += [(trainset.to_raw_uid(u), trainset.to_raw_iid(i), fill) for
                   i in trainset.all_items() if
                   i not in user_items]
        return recset

    def recommend(self, user_Id, nof_rec=4, verbose=True):  # Check whether the user has already scored, if not, it will be randomly recommended by default
        self.user_Id = user_Id
        if (self.user_Id not in self.nof_user_ratings.index):
            list=self.nof_user_ratings.index.tolist()
            list.sort()
            # print(self.user_Id,list)
            print('The current user has not performed a scoring behavior, and will recommend books randomly.\n')
            items=self.rand_recommend()
            return items
        print('The user has performed a rating behavior, and recommends based on the rating.\n')
        try:
            recset = self.build_recset(self.trainset)
        except:
            self.build_trainset()
            recset = self.build_recset(self.trainset)
        try:
            predictions = self.algorithm.test(recset)
        except:
            logging.error(('%sposition no model found"model.pickle".\nplease confirm the model path'), self.model_path)

        # Build a list of recommended books
        top_n = []
        for _, iid, _, est, _ in predictions:
            top_n.append((iid, int(est)))
        top_n.sort(key=lambda x: x[1], reverse=True)
        isbn, rating = [], []
        for i, r in top_n[:nof_rec]:
            print(i)
            isbn.append(i)
            rating.append(int(r))
        items = self.items_df.loc[self.items_df.isbn.isin(isbn)]
        items = pd.concat([items.reset_index(drop=True), pd.DataFrame({'rating': rating})], axis=1)

        return self.transToList(items)

    def load_dfs(self):  #Load data files
        try:
            items_df = pd.read_csv(os.path.join(self.dfs_path, 'book2.csv'), sep=',', encoding='latin-1',
                                   low_memory=False)
            ratings_df = pd.read_csv(os.path.join(self.dfs_path, 'rating3.csv'), sep=',', encoding='latin-1',
                                     low_memory=False)
        except:
            logging.error(('One or more of the files was not found in %s.\n Please make sure you have run '
                           '"BookCrossing data cleansing.ipynb" first.'), self.dfs_path)
            sys.exit(1)
        return items_df, ratings_df

    def rand_recommend(self, nof_rec=4):  # Randomly return n recommended books
        top_n = self.ratings_df[['isbn', 'rating']][self.ratings_df['rating'] == 10]
        row_num = top_n.shape[0]
        rand = random.randint(0, max(row_num - nof_rec, 1))
        isbn, rating = [], []
        for i in zip(top_n['isbn'][rand:rand + nof_rec], top_n['rating'][rand:rand + nof_rec]):
            isbn.append(i[0])
            rating.append(int(i[1]))
        items = self.items_df.loc[self.items_df.isbn.isin(isbn)]
        items = pd.concat([items.reset_index(drop=True), pd.DataFrame({'rating': rating})], axis=1)
        top_n=[];
        for i in range(nof_rec):
            top_n.append((i,'*'))
        return self.transToList(items)

    def model_fit(self):  #Train model
        self.build_trainset()
        algo = self._algo_choise
        if algo == 'SVD':
            self.algorithm = surprise.SVD()
        elif algo == 'Baseline':
            self.algorithm = surprise.BaselineOnly()
        elif algo == 'NMF':
            self.algorithm = surprise.NMF()
        elif algo == 'CoClustering':
            self.algorithm = surprise.CoClustering()
        else:
            self.algorithm = surprise.KNNBasic()

        print('Use%salgorithm traning' % algo)

        self.algorithm.fit(self.trainset)
        self.ratings_changed = False
        self.save_model()
        print('Done')

    def save_model(self, verbose=True):  # Save model
        if verbose:
            print('Save...')
        verbose = 1 * verbose
        surprise.dump.dump(self.model_path, predictions=None, algo=self.algorithm, verbose=verbose)

if __name__ == '__main__':
    rec = recommender()
    # items = rec.recommend(user_Id=345525)   #Recommend randomly
    time_start = time.time()
    rec.model_fit()
    print('2')
    items = rec.recommend(user_Id=51172)
    time_end = time.time()
    print('运行耗时：', time_end - time_start)
    i=0
    for item in items:
        i=i+1
        # print('Book "',item[1], '" from "', item[2], '", (%f)'%item[5])
        print('{0}) "{1}({2})"  of {3}.\nThe url is: {4}'.format(i, item['book_title'], item['isbn'],
                                    item['book_author'] ,item['img_m']))
    # rec.model_fit()