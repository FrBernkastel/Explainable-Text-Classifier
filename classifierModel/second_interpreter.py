#!/usr/bin/env python3


# Import libararies
import re
import pandas as pd 
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
        self.pos_num = 800

        self.thresholds = []
        for i in range(len(self.coefs)):
            coefs_sorted = sorted(self.coefs[i], reverse = True)
            th = coefs_sorted[self.pos_num]
            self.thresholds.append(th)


    def predict_topk(self, input_text, k):
        self.lr.topk = k

        # print('convert data')
        # Convert pandas series into numpy array
        X_test = np.array([input_text, "Will Smith Joins Diplo And Nicky Jam For The 2018 World Cup Official Song"])

        # from nltk.stem import WordNetLemmatizer
        lemmetizer = WordNetLemmatizer()
        def fetch_words(headline):
            line = headline
            line_only_alpha = re.sub('[^a-zA-Z]', ' ', line)
            words = nltk.word_tokenize(line_only_alpha.lower())
            stops = set(stopwords.words('english'))
            meaningful = [lemmetizer.lemmatize(w) for w in words if w not in stops]
            return ' '.join(meaningful )

        X_test_clean = [fetch_words(elem) for elem in X_test]
        test_tfidf = self.lr._vectorize.transform(X_test_clean)
        X_test = test_tfidf.toarray()

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
        input_transform = test_tfidf[0]
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
