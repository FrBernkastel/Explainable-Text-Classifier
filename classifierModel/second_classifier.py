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
from sklearn.metrics import accuracy_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

from nltk.stem import PorterStemmer, WordNetLemmatizer
import zipfile
import operator


class Data_Reader():
    """
    Provide some methods for reading dataset
    """

    def __init__(self, BagOfWords=False, TFIDF=True):
        self.Feature_BagOfWords = BagOfWords
        self.Feature_TFIDF = TFIDF
        self._vectorize = None

    def read_files(self, tarfname):

        print('read file')
        news = pd.read_json(tarfname, lines=True)
        # remove_columns_list = ['authors', 'date', 'link', 'short_description', 'headline']
        news['information'] = news[['headline', 'short_description']].apply(lambda x: ' '.join(x), axis=1)
        news.drop(news[(news['authors'] == '') & (news['short_description'] == '')].index, inplace=True)
        print('news complete')

        class Data:
            pass

        sentiment = Data()

        print('split data')
        # Split the data into train and test.
        X_train, X_test, Y_train, Y_test = \
            sklearn.model_selection.train_test_split(news[['information', 'authors']], news['category'], test_size=0.33)

        print('convert data')
        # Convert pandas series into numpy array
        X_train = np.array(X_train) 
        X_test  = np.array(X_test) 
        sentiment.Y_train = np.array(Y_train)
        sentiment.Y_test = np.array(Y_test)        

        print('clean headline')
        # from nltk.stem import PorterStemmer, WordNetLemmatizer
        lemmetizer = WordNetLemmatizer()
        stemmer = PorterStemmer()

        def fetch_words(headlines_list):
            head = headlines_list[0]
            author = [x for x in headlines_list[1].lower().replace('and', ',').replace(' ', '').split(',') if x != '']
            head_only_alpha = re.sub('[^a-zA-Z]', ' ', head)
            words = nltk.word_tokenize(head_only_alpha.lower())
            stops = set(stopwords.words('english'))
            meaningful = [lemmetizer.lemmatize(w) for w in words if w not in stops]
            return ' '.join(meaningful + author)

        X_train_clean = [ fetch_words(elem) for elem in X_train ]
        X_test_clean  = [ fetch_words(elem) for elem in X_test ]

        print('vectorize')
        vectorize = sklearn.feature_extraction.text.TfidfVectorizer(analyzer="word", max_features=30000)
        X_train = vectorize.fit_transform(X_train_clean)
        sentiment.X_train = X_train.toarray()
        X_test = vectorize.transform(X_test_clean)
        sentiment.X_test  = X_test.toarray()
        self._vectorize = vectorize

        print('return sentiment')
        return sentiment


class LogisRegression(object):
    """docstring for LogisRege"""

    # def __init__(self, tarfname = "data/sentiment.tar.gz"):
    def __init__(self, tarfname="data/News_Category_Dataset.json.zip"):
        zip_ref = zipfile.ZipFile(tarfname, 'r')
        zip_ref.extractall('data/')
        zip_ref.close()

        self.tarfname = 'data/News_Category_Dataset.json'
        self.count_vect = None
        self._vectorize = None
        self.cls = self.get_cls(Data_Reader())
        self.topk = None

    def get_cls(self, dr):
        """
        Train a classifier and return it
        """
        print("Reading data")
        sentiment = dr.read_files(self.tarfname)
        print('train classifier')
        cls = self.train_classifier(sentiment.X_train, sentiment.Y_train)
        self._vectorize = dr._vectorize

        print('return cls')
        return cls

    def train_classifier(self, X, y, c=1.0):
        """Train a classifier using the given training data.
        Trains logistic regression on the input data with default parameters.
        """
        cls = LogisticRegression()
        cls.fit(X, y)
        return cls
