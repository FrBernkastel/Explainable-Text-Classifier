#!/usr/bin/env python3

# readme
# >>> import second_classifier as cl2
# >>> lr = cl2.LogisRegression()
# >>> lr.predict_topk("Hugh Grant Marries For The First Time At Age 57",5)
#
# returns:
# [('SPORTS', 0.030512064441369068),
#  ('FIFTY', 0.050181183875010804),
#  ('HEALTHY LIVING', 0.05387805876430925),
#  ('POLITICS', 0.09585761922835287),
#  ('ENTERTAINMENT', 0.41487000587815787)]



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

import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline 
import warnings
warnings.filterwarnings('ignore')

import zipfile


import operator

class Data_Reader():
    """
    Provide some methods for reading dataset
    """

    def __init__(self, BagOfWords = False, TFIDF = True):
        self.Feature_BagOfWords = BagOfWords
        self.Feature_TFIDF = TFIDF
        self._vectorize = None

    def read_files(self, tarfname):
        """Read the training and development data from the sentiment tar file.
        The returned object contains various fields that store sentiment data, such as:
        train_data,dev_data: array of documents (array of words)
        train_fnames,dev_fnames: list of filenames of the doccuments (same length as data)
        train_labels,dev_labels: the true string label for each document (same length as data)
        The data is also preprocessed for use with scikit-learn, as:
        count_vec: CountVectorizer used to process the data (for reapplication on new data)
        trainX,devX: array of vectors representing Bags of Words, i.e. documents processed through the vectorizer
        le: LabelEncoder, i.e. a mapper from string labels to ints (stored for reapplication)
        target_labels: List of labels (same order as used in le)
        trainy,devy: array of int labels, one for each document
        """
        # tar = tarfile.open(tarfname, "r:gz")
        # trainname = "train.tsv"
        # devname = "dev.tsv"
        # for member in tar.getmembers():
        #     if 'train.tsv' in member.name:
        #         trainname = member.name
        #     elif 'dev.tsv' in member.name:
        #         devname = member.name

        print('read file')
        news = pd.read_json(tarfname, lines=True)
        #remove_columns_list = ['authors', 'date', 'link', 'short_description', 'headline']
        news['information'] = news[['headline', 'short_description']].apply(lambda x: ' '.join(x), axis=1)
        news.drop(news[(news['authors'] == '') & (news['short_description'] == '' )].index, inplace=True)
        print('news complete')

        class Data: pass
        sentiment = Data()

        print('split data')
        # Split the data into train and test.
        X_train, X_test, Y_train, Y_test =\
                sklearn.model_selection.train_test_split(news[['information', 'authors']], news['category'], test_size=0.33)

        print('convert data')
        # Convert pandas series into numpy array
        X_train = np.array(X_train);
        X_test = np.array(X_test);
        sentiment.Y_train = np.array(Y_train);
        sentiment.Y_test = np.array(Y_test);
        cleanHeadlines_train = [] #To append processed headlines
        cleanHeadlines_test = [] #To append processed headlines
        number_reviews_train = len(X_train) #Calculating the number of reviews
        number_reviews_test = len(X_test) #Calculating the number of reviews

        print('clean headline')
        # from nltk.stem import PorterStemmer, WordNetLemmatizer
        lemmetizer = WordNetLemmatizer()
        stemmer = PorterStemmer()
        def get_words(headlines_list):
            headlines = headlines_list[0]   
            author_names = [x for x in headlines_list[1].lower().replace('and',',').replace(' ', '').split(',') if x != '']
            headlines_only_letters = re.sub('[^a-zA-Z]', ' ', headlines)
            words = nltk.word_tokenize(headlines_only_letters.lower())
            stops = set(stopwords.words('english'))
            meaningful_words = [lemmetizer.lemmatize(w) for w in words if w not in stops]
            return ' '.join(meaningful_words + author_names)

        for i in range(0,number_reviews_train):
            cleanHeadline = get_words(X_train[i]) #Processing the data and getting words with no special characters, numbers or html tags
            cleanHeadlines_train.append( cleanHeadline )

        for i in range(0,number_reviews_test):
            cleanHeadline = get_words(X_test[i]) #Processing the data and getting words with no special characters, numbers or html tags
            cleanHeadlines_test.append( cleanHeadline )

        print('vectorize')
        vectorize = sklearn.feature_extraction.text.TfidfVectorizer(analyzer = "word", max_features=30000)
        tfidwords_train = vectorize.fit_transform(cleanHeadlines_train)
        sentiment.X_train = tfidwords_train.toarray()

        tfidwords_test = vectorize.transform(cleanHeadlines_test)
        sentiment.X_test = tfidwords_test.toarray()

        self._vectorize = vectorize


        # print("-- train data")
        # sentiment.train_data, sentiment.train_labels = self.read_tsv(tar,trainname)
        # print(len(sentiment.train_data))

        # print("-- dev data")
        # sentiment.dev_data, sentiment.dev_labels = self.read_tsv(tar, devname)
        # print(len(sentiment.dev_data))
        # print("-- transforming data and labels")

        # if self.Feature_BagOfWords:
        #     from sklearn.feature_extraction.text import CountVectorizer
        #     sentiment.count_vect = CountVectorizer()
        # if self.Feature_TFIDF:
        #     from sklearn.feature_extraction.text import TfidfVectorizer
        #     # sentiment.count_vect = TfidfVectorizer(ngram_range=(1,2), max_features=10000)
        #     sentiment.count_vect = TfidfVectorizer(ngram_range=(1,2))

        # sentiment.trainX = sentiment.count_vect.fit_transform(sentiment.train_data)
        # sentiment.devX = sentiment.count_vect.transform(sentiment.dev_data)

        # sentiment.le = preprocessing.LabelEncoder()
        # sentiment.le.fit(sentiment.train_labels)
        # sentiment.target_labels = sentiment.le.classes_
        # sentiment.trainy = sentiment.le.transform(sentiment.train_labels)
        # sentiment.devy = sentiment.le.transform(sentiment.dev_labels)
        # tar.close()
        print('return sentiment')
        return sentiment

    # def read_unlabeled(self, tarfname, sentiment):
    #     """Reads the unlabeled data.
    #     The returned object contains three fields that represent the unlabeled data.
    #     data: documents, represented as sequence of words
    #     fnames: list of filenames, one for each document
    #     X: bag of word vector for each document, using the sentiment.vectorizer
    #     """
    #     tar = tarfile.open(tarfname, "r:gz")
    #     class Data: pass
    #     unlabeled = Data()
    #     unlabeled.data = []
        
    #     unlabeledname = "unlabeled.tsv"
    #     for member in tar.getmembers():
    #         if 'unlabeled.tsv' in member.name:
    #             unlabeledname = member.name
                
    #     print(unlabeledname)
    #     tf = tar.extractfile(unlabeledname)
    #     for line in tf:
    #         line = line.decode("utf-8")
    #         text = line.strip()
    #         unlabeled.data.append(text)

    #     unlabeled.X = sentiment.count_vect.transform(unlabeled.data)
    #     print(unlabeled.X.shape)
    #     tar.close()
    #     return unlabeled

    # def read_tsv(self, tar, fname):
    #     member = tar.getmember(fname)
    #     print(member.name)
    #     tf = tar.extractfile(member)
    #     data = []
    #     labels = []
    #     for line in tf:
    #         line = line.decode("utf-8")
    #         (label,text) = line.strip().split("\t")
    #         labels.append(label)
    #         data.append(text)
    #     return data, labels


class LogisRegression(object):
    """docstring for LogisRege"""

    # def __init__(self, tarfname = "data/sentiment.tar.gz"):
    def __init__(self, tarfname = "data/News_Category_Dataset.json.zip"):     
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


        # self.count_vect = sentiment.count_vect
        # unlabeled = dr.read_unlabeled(self.tarfname, sentiment)

        # print("\nTraining classifier")   
        # length = unlabeled.X.get_shape()[0]
        # expand_step = int(sentiment.trainX.get_shape()[0]/30)
        
        # # %%
        # Dl_x = sentiment.trainX
        # Dl_y = sentiment.trainy
        # Du = unlabeled.X[:int(length*5/10),:]
        # added = set()  # the index of what already been added to labeled data
        # acc_devs = []
        # clss = []
        # preds = []
        # itr = 0
        # while itr < 1000:
        #     cls = self.train_classifier(Dl_x, Dl_y)
        #     clss.append(cls)
        #     acc_dev = self.evaluate(sentiment.devX, sentiment.devy, cls, 'dev')
        #     acc_devs.append(acc_dev)

        #     # predict
        #     Du_y = cls.predict(Du)

        #     # stop criterion
        #     preds.append(Du_y)
        #     if itr > 6:
        #         if itr%10==0: print(itr)
        #         diff = np.count_nonzero((preds[itr] - preds[itr-1]))
        #         if diff < 0.003 * len(Du_y):
        #             print("done training")
        #             break

        #     # expand
        #     conf = cls.decision_function(Du)
        #     conf_dict = [(abs(conf[i]), i) for i in range(0,conf.shape[0]) if i not in added]
        #     conf_dict.sort(key = lambda tup: tup[0], reverse=True)
        #     # take 10% every time
        #     taken = [conf_dict[i][1] for i in range(0, expand_step)]
        #     added.update(taken)
        #     Dl_x = vstack([Dl_x, Du[taken]])
        #     Dl_y = np.concatenate((Dl_y, Du_y[taken]))

        #     itr += 1

        # idx = acc_devs.index(max(acc_devs)) 
        # cls = clss[idx]
        print('return cls')
        return cls

    def train_classifier(self, X, y, c=1.0):
        """Train a classifier using the given training data.
        Trains logistic regression on the input data with default parameters.
        """
        # cls = LogisticRegression(C=c, random_state=0, solver='lbfgs', max_iter=10000)
        # cls = LogisticRegressionCV(cv=3, random_state=0, solver='lbfgs', max_iter=10000)
        # cls.fit(X, y)

        cls = LogisticRegression()
        cls.fit(X,y)
        return cls

    def predict_topk(self, input_text, k):
        self.topk = k

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

        tfidwords_test = self._vectorize.transform(cleanHeadlines_test)
        X_test = tfidwords_test.toarray()

        
        def tag_proba_func(tag, proba):
            res = []
            for i in range(len(tag)):
                res.append( (tag[i], float(proba[i])) )
            return res
        proba_list = self.cls.predict_proba(X_test)
        tag_proba_list = tag_proba_func(self.cls.classes_, proba_list[0])
        tag_proba_list.sort(key = operator.itemgetter(1) )

        # labels (31,)
        labels = self.cls.classes_
        # coef (31, 30000)
        coef = self.cls.coef_
        # feature names len()=30000
        feature_names = self._vectorize.get_feature_names()
        # transform (1, 30000)
        text = "Hugh Grant Marries For The First Time At Age 57"
        transform = self._vectorize.transform([text])[0]


        res = dict()
        res['labels_prob'] = tag_proba_list
        res['topk_label_proba'] = tag_proba_list[-self.topk:]        
        res['label__feat_coef'] = dict()
        for i in range(labels.shape[0]) :
            feat_coef = list()
            for j in transform.indices:
                feat_coef.append( (feature_names[j], coef[i][j]) )
            feat_coef.sort( key = operator.itemgetter(1) )
            res['label__feat_coef'][labels[i]] = feat_coef

        return res


    # def evaluate(self, X, yt, cls, name='data'):
    #     """Evaluated a classifier on the given labeled data using accuracy."""
    #     yp = cls.predict(X)
    #     acc = metrics.accuracy_score(yt, yp)
    #     print("  Accuracy on %s  is: %s" % (name, acc))
    #     return acc
