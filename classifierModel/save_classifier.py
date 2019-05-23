#!/usr/bin/env python3

## run this file to get the classifier backup, so you don't have to train it everytime you start the sever

import classifier as cf
import pickle

lr = cf.LogisRegression()

with open('classifier.backup', 'wb') as backup_file:
    pickle.dump(lr, backup_file)
