#!/bin/python

import tarfile
from scipy.sparse import vstack
import numpy as np
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn import metrics
from sklearn import preprocessing

class Data_Reader():
    """
    Provide some methods for reading dataset
    """

    def __init__(self, BagOfWords = False, TFIDF = True):
        self.Feature_BagOfWords = BagOfWords
        self.Feature_TFIDF = TFIDF

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
        tar = tarfile.open(tarfname, "r:gz")
        trainname = "train.tsv"
        devname = "dev.tsv"
        for member in tar.getmembers():
            if 'train.tsv' in member.name:
                trainname = member.name
            elif 'dev.tsv' in member.name:
                devname = member.name

        class Data: pass
        sentiment = Data()
        print("-- train data")
        sentiment.train_data, sentiment.train_labels = self.read_tsv(tar,trainname)
        print(len(sentiment.train_data))

        print("-- dev data")
        sentiment.dev_data, sentiment.dev_labels = self.read_tsv(tar, devname)
        print(len(sentiment.dev_data))
        print("-- transforming data and labels")

        if self.Feature_BagOfWords:
            from sklearn.feature_extraction.text import CountVectorizer
            sentiment.count_vect = CountVectorizer()
        if self.Feature_TFIDF:
            from sklearn.feature_extraction.text import TfidfVectorizer
            # sentiment.count_vect = TfidfVectorizer(ngram_range=(1,2), max_features=10000)
            sentiment.count_vect = TfidfVectorizer(ngram_range=(1,2))

        sentiment.trainX = sentiment.count_vect.fit_transform(sentiment.train_data)
        sentiment.devX = sentiment.count_vect.transform(sentiment.dev_data)

        sentiment.le = preprocessing.LabelEncoder()
        sentiment.le.fit(sentiment.train_labels)
        sentiment.target_labels = sentiment.le.classes_
        sentiment.trainy = sentiment.le.transform(sentiment.train_labels)
        sentiment.devy = sentiment.le.transform(sentiment.dev_labels)
        tar.close()
        return sentiment

    def read_unlabeled(self, tarfname, sentiment):
        """Reads the unlabeled data.

        The returned object contains three fields that represent the unlabeled data.

        data: documents, represented as sequence of words
        fnames: list of filenames, one for each document
        X: bag of word vector for each document, using the sentiment.vectorizer
        """
        tar = tarfile.open(tarfname, "r:gz")
        class Data: pass
        unlabeled = Data()
        unlabeled.data = []
        
        unlabeledname = "unlabeled.tsv"
        for member in tar.getmembers():
            if 'unlabeled.tsv' in member.name:
                unlabeledname = member.name
                
        print(unlabeledname)
        tf = tar.extractfile(unlabeledname)
        for line in tf:
            line = line.decode("utf-8")
            text = line.strip()
            unlabeled.data.append(text)

        unlabeled.X = sentiment.count_vect.transform(unlabeled.data)
        print(unlabeled.X.shape)
        tar.close()
        return unlabeled

    def read_tsv(self, tar, fname):
        member = tar.getmember(fname)
        print(member.name)
        tf = tar.extractfile(member)
        data = []
        labels = []
        for line in tf:
            line = line.decode("utf-8")
            (label,text) = line.strip().split("\t")
            labels.append(label)
            data.append(text)
        return data, labels


class LogisRegression(object):
    """docstring for LogisRege"""

    def __init__(self, tarfname = "data/sentiment.tar.gz"):
        self.tarfname = tarfname
        self.sentiment = None
        self.cls = self.get_cls(Data_Reader())
        
    def get_cls(self, dr):
        """
        Train a classifier and return it
        """

        print("Reading data")
        self.sentiment = dr.read_files(self.tarfname)
        unlabeled = dr.read_unlabeled(self.tarfname, self.sentiment)

        print("\nTraining classifier")   
        length = unlabeled.X.get_shape()[0]
        expand_step = int(self.sentiment.trainX.get_shape()[0]/30)
        
        # %%
        Dl_x = self.sentiment.trainX
        Dl_y = self.sentiment.trainy
        Du = unlabeled.X[:int(length*5/10),:]
        added = set()  # the index of what already been added to labeled data
        acc_devs = []
        clss = []
        preds = []
        itr = 0
        while itr < 1000:
            cls = self.train_classifier(Dl_x, Dl_y)
            clss.append(cls)
            acc_dev = self.evaluate(self.sentiment.devX, self.sentiment.devy, cls, 'dev')
            acc_devs.append(acc_dev)

            # predict
            Du_y = cls.predict(Du)

            # stop criterion
            preds.append(Du_y)
            if itr > 6:
                if itr%10==0: print(itr)
                diff = np.count_nonzero((preds[itr] - preds[itr-1]))
                if diff < 0.003 * len(Du_y):
                    print("done training")
                    break

            # expand
            conf = cls.decision_function(Du)
            conf_dict = [(abs(conf[i]), i) for i in range(0,conf.shape[0]) if i not in added]
            conf_dict.sort(key = lambda tup: tup[0], reverse=True)
            # take 10% every time
            taken = [conf_dict[i][1] for i in range(0, expand_step)]
            added.update(taken)
            Dl_x = vstack([Dl_x, Du[taken]])
            Dl_y = np.concatenate((Dl_y, Du_y[taken]))

            itr += 1

        idx = acc_devs.index(max(acc_devs)) 
        cls = clss[idx]
        return cls

    def train_classifier(self, X, y, c=1.0):
        """Train a classifier using the given training data.

        Trains logistic regression on the input data with default parameters.
        """
        # cls = LogisticRegression(C=c, random_state=0, solver='lbfgs', max_iter=10000)
        cls = LogisticRegressionCV(cv=3, random_state=0, solver='lbfgs', max_iter=10000)
        cls.fit(X, y)
        return cls

    def evaluate(self, X, yt, cls, name='data'):
        """Evaluated a classifier on the given labeled data using accuracy."""
        yp = cls.predict(X)
        acc = metrics.accuracy_score(yt, yp)
        print("  Accuracy on %s  is: %s" % (name, acc))
        return acc