#!/usr/bin/env python3

from nltk.corpus import stopwords

class explain():
    def __init__(self, classifier):
        # the threshold that means import
        self.pos_num = 200
        self.neg_num = 300
        print(classifier)

        self.lr = classifier
        self.features = self.feature_arr()
        self.coefs = self.coef_arr()

        self.pos_threshold, self.neg_threshold = self.get_threshold()
        self.stopwords = set(stopwords.words('english'))

    def feature_arr(self):
        """

        :return: the feature array
        """
        features = self.lr.count_vect.get_feature_names()
        return features

    def coef_arr(self):
        """

        :return: the coefficient array
        """
        coefs = self.lr.cls.coef_[0]
        return coefs

    def get_threshold(self):
        """

        :return: return the threshold of mater coefficient
        """
        # l = [(features[i], coefs[i]) for i in range(len(features))]
        # l.sort(key=lambda tp: tp[1])
        l = self.coefs.copy()
        l.sort()
        pos_thre = l[-self.pos_num]
        neg_thre = l[self.neg_num]
        # print(pos_thre)
        # print(neg_thre)
        return (pos_thre, neg_thre)

    def get_explanation(self, vec):
        """

        :param vec: the vector of target text
        :return: res: a dictionary of import words; flag: false for no valued words
        """
        # get feature to coefficient mapping
        mapping = [(self.features[i], self.coefs[i]) for i in vec.indices]
        mapping.sort(key=lambda tp: tp[1])
        # print(mapping)
        valued_pos = [x[0] for x in mapping if x[1] >= self.pos_threshold and x[0] not in self.stopwords]
        valued_neg = [x[0] for x in mapping if x[1] <= self.neg_threshold and x[0] not in self.stopwords]
        if len(valued_neg) == 0 and len(valued_pos) == 0:
            flag = False
        else:
            flag = True
        res = dict()
        res['valued_pos'] = valued_pos
        res['valued_neg'] = valued_neg
        return res, flag





