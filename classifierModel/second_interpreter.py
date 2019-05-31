#!/usr/bin/env python3


# Import libararies
import re
import pandas as pd # CSV file I/O (pd.read_csv)
from nltk.corpus import stopwords
import numpy as np
import sklearn
import nltk
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score ,confusion_matrix

from nltk.stem import PorterStemmer, WordNetLemmatizer

import warnings
warnings.filterwarnings('ignore')


import operator

from nltk.corpus import stopwords

class explain():
    def __init__(self, classifier):

        self.lr = classifier #liu
        # feature names len()=30000
        feature_names = self.lr._vectorize.get_feature_names() #liu
        # coef (31, 30000)
        self.coefs = self.lr.cls.coef_
        self.pos_num = 1000

        self.thresholds = []
        for i in range(len(self.coefs)):
            coefs_sorted = sorted(self.coefs[i], reverse = True)
            th = coefs_sorted[self.pos_num]
            self.thresholds.append(th)

        # self.pos_threshold, self.neg_threshold = self.get_threshold() #wq
        # self.stopwords = set(stopwords.words('english')) #wq


        # def get_threshold(self):
        #     """

        #     :return: return the threshold of mater coefficient
        #     """
        #     # l = [(features[i], coefs[i]) for i in range(len(features))]
        #     # l.sort(key=lambda tp: tp[1])
        #     l = self.coefs.copy()
        #     l.sort()
        #     pos_thre = l[-self.pos_num]
        #     neg_thre = l[self.neg_num]
        #     # print(pos_thre)
        #     # print(neg_thre)
        #     return (pos_thre, neg_thre)

        # def get_explanation(self, vec):
        #     """

        #     :param vec: the vector of target text
        #     :return: res: a dictionary of import words; flag: false for no valued words
        #     """
        #     # get feature to coefficient mapping
        #     mapping = [(self.features[i], self.coefs[i]) for i in vec.indices]
        #     mapping.sort(key=lambda tp: tp[1])
        #     print(mapping)
        #     valued_pos = [x[0] for x in mapping if x[1] >= self.pos_threshold and x[0] not in self.stopwords]
        #     valued_neg = [x[0] for x in mapping if x[1] <= self.neg_threshold and x[0] not in self.stopwords]
        #     if len(valued_neg) == 0 and len(valued_pos) == 0:
        #         flag = False
        #     else:
        #         flag = True
        #     res = dict()
        #     res['valued_pos'] = valued_pos
        #     res['valued_neg'] = valued_neg
        #     return res, flag



    def predict_topk(self, input_text, k):
        self.lr.topk = k

        # print('convert data')
        # Convert pandas series into numpy array
        X_test = np.array([input_text, "Will Smith Joins Diplo And Nicky Jam For The 2018 World Cup Official Song"])
        cleanHeadlines_test = [] #To append processed headlines
        number_reviews_test = len(X_test) #Calculating the number of reviews

        # print('clean headline')
        # from nltk.stem import PorterStemmer, WordNetLemmatizer
        lemmetizer = WordNetLemmatizer()
        stemmer = PorterStemmer()
        def get_words(headlines_list):
            headlines = headlines_list   
            headlines_only_letters = re.sub('[^a-zA-Z]', ' ', headlines)
            words = nltk.word_tokenize(headlines_only_letters.lower())
            stops = set(stopwords.words('english'))
            meaningful_words = [lemmetizer.lemmatize(w) for w in words if w not in stops]
            return ' '.join(meaningful_words )


        for i in range(0,number_reviews_test):
            cleanHeadline = get_words(X_test[i]) #Processing the data and getting words with no special characters, numbers or html tags
            cleanHeadlines_test.append( cleanHeadline )

        tfidwords_test = self.lr._vectorize.transform(cleanHeadlines_test)
        X_test = tfidwords_test.toarray()

        
        def tag_proba_func(tag, proba):
            res = []
            for i in range(len(tag)):
                res.append( (tag[i], float(proba[i])) )
            return res
        proba_list = self.lr.cls.predict_proba(X_test)
        tag_proba_list = tag_proba_func(self.lr.cls.classes_, proba_list[0])
        tag_proba_list.sort(key = operator.itemgetter(1), reverse = True )


        # labels (31,)
        labels = self.lr.cls.classes_
        # coef (31, 30000)
        coef = self.lr.cls.coef_
        # feature names len()=30000
        feature_names = self.lr._vectorize.get_feature_names()
        # transform (1, 30000)
        input_transform = tfidwords_test[0]
        input_transform_indices = list()
        for e in input_transform.indices:
            input_transform_indices.append(int(e))


        res = dict()        
        res['input_transform_indices'] = input_transform_indices
        res['flag'] = len(input_transform_indices) > 0
        res['labels_prob'] = list(proba_list[0])
        res['topk_label_proba'] = tag_proba_list[:self.lr.topk]     
        res['label__feat_coef'] = dict()
        for i in range(labels.shape[0]) :
            feat_coef = list()
            for j in input_transform.indices:
                if (coef[i][j] >= self.thresholds[i]):
                    feat_coef.append( (feature_names[j], coef[i][j]) )
            feat_coef.sort( key = operator.itemgetter(1),reverse=True)
            res['label__feat_coef'][labels[i]] = feat_coef

        return res





