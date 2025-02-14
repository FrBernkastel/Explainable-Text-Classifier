#!/usr/bin/env python3

# %%
import rpyc
import classifier as cf
import second_classifier as cf2
import interpreter as ip
import second_interpreter as ip2
import json
import os
import pickle

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8001        # Port to listen on (non-privileged ports are > 1023)


# %%
class PredictServer(rpyc.Service):
    """
        The server that makes predictions for text using a classifier
    """

    def __init__(self, interpreter, interpreter2):

        if not os.path.isfile('classifier.backup'):
            self.lr = cf.LogisRegression()
            with open('classifier.backup', 'wb') as backup_file:
                pickle.dump(self.lr, backup_file)
        else:
            with open('classifier.backup', 'rb') as backup_file:
                self.lr = pickle.load( backup_file)
        print("lr finished")

        if not os.path.isfile('second_classifier.backup'):
            self.lr2 = cf2.LogisRegression()
            with open('second_classifier.backup', 'wb') as backup_file:
                pickle.dump(self.lr2, backup_file)
        else:
            with open('second_classifier.backup', 'rb') as backup_file:
                self.lr2 = pickle.load( backup_file)
        print("lr2 finished")

        self.ip = interpreter(self.lr)
        print("ip finished")
        self.ip2 = interpreter2(self.lr2)
        print("ip2 finished")

    def exposed_predict(self, text):
        """
        :param text: the target text
        :return: (prediction, a list of important words)
        """
        try:
            assert type(text) == str, "not valid input"
        except:
            pass

        vec = self.lr.count_vect.transform([text])[0]
        pre = int(self.lr.cls.predict(vec))
        # probability of the label
        pro = self.lr.cls.predict_proba(vec)[0][pre]
        # confidence score
        con = self.lr.cls.decision_function(vec)
        ex, flag = self.ip.get_explanation(vec)


        res = dict()
        # 'label', 'probability', 'confidence', 'flag', 'explanation'
        res['label'] = pre
        res['probability'] = pro
        res['confidence'] = con[0]
        res['flag'] = flag

        # todo: sometimes contains duplicated words, e.g. "it's not good enough". return ['not', 'not good'].
        if pre == 1:
            res['explanation'] = ex['valued_pos']
        else:
            res['explanation'] = ex['valued_neg']
        return json.dumps(res)

    def exposed_predict_news(self, text):
        """
        :param text: the target text
        :return: (prediction, a list of important words)
        """
        try:
            assert type(text) == str, "not valid input"
        except:
            pass

        res = self.ip2.predict_topk(text, 5)

        # res['labels_prob'] = [0.03528977019242901 * 31] #acsending sort
        # res['topk_label_proba'] =  [('SPORTS', 0.03528977019242901) * 5] #acsending sort
        # res['label__feat_coef'] =  {'SPORTS': [('curry', 0.5), ('james', 0.3), ('soccer', 0.3)] * 31  } #order by label name

        return json.dumps(res)

    def exposed_test(self, t = None):
        if t is not None:
            return t
        else:
            return "good job"


if __name__ == '__main__':
    from rpyc.utils.server import ThreadPoolServer

    server = ThreadPoolServer(PredictServer(ip.explain, ip2.explain), port = PORT)
    server.start()
