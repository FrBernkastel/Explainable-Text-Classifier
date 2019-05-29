#!/usr/bin/env python3

# %%
import rpyc
import classifier as cf
import interpreter as ip
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

    def __init__(self, interpreter):

        if not os.path.isfile('classifier.backup'):
            self.lr = cf.LogisRegression()
            with open('classifier.backup', 'wb') as backup_file:
                pickle.dump(self.lr, backup_file)
        else:
            with open('classifier.backup', 'rb') as backup_file:
                self.lr = pickle.load( backup_file)
            print("finished")
        self.ip = interpreter(self.lr)

    def exposed_predict_news(self, text):
        """

        :param text: the target text
        :return: (prediction, a list of important words)
        """
        try:
            assert type(text) == str, "not valid input"
        except:
            pass
        res = dict()
        res['topk_labels'] = ['SPORTS', 'FIFTY', 'HEALTHY LIVING', 'POLITICS', 'ENTERTAINMENT']
        res['topk_prob'] = [0.4, 0.3, 0.2, 0.05, 0.05]
        res['topk_labels_prob'] = [('SPORTS', 0.03528977019242901),\
                     ('FIFTY', 0.04950928969548888),\
                      ('HEALTHY LIVING', 0.0770822639575894),\
                       ('POLITICS', 0.09133677266006603),\
                        ('ENTERTAINMENT', 0.34307359857285236)]
        res['topk_labels__feature_coef'] =  {'SPORTS': [('curry', 0.5), ('james', 0.3), ('soccer', 0.3)],\
                                            'FIFTY': [('curry', 0.5), ('james', 0.3), ('soccer', 0.3)],\
                                            'HEALTHY LIVING': [('curry', 0.5), ('james', 0.3), ('soccer', 0.3)],\
                                            'POLITICS': [('curry', 0.5), ('james', 0.3), ('soccer', 0.3)],\
                                            'ENTERTAINMENT': [('curry', 0.5), ('james', 0.3), ('soccer', 0.3)],\
                                            }

        #  [
        #     ['SPORTS', ('curry', 0.5), ('james', 0.3), ('soccer', 0.3)]
        #     ['FIFTY', ('curry', 0.5), ('james', 0.3), ('soccer', 0.3)]
        #     ['HEALTHY LIVING', ('curry', 0.5), ('james', 0.3), ('soccer', 0.3)]
        #     ['POLITICS', ('curry', 0.5), ('james', 0.3), ('soccer', 0.3)]
        #     ['ENTERTAINMENT', ('curry', 0.5), ('james', 0.3), ('soccer', 0.3)]     
        # ]

        # res['label'] = [1,2,3]
        # res['probability'] = [2,3,4]
        # res['confidence'] = [222]
        # res['flag'] = flag

        return json.dump(res) 



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

    def exposed_test(self, t = None):
        if t is not None:
            return t
        else:
            return "good job"


if __name__ == '__main__':
    from rpyc.utils.server import ThreadPoolServer

    server = ThreadPoolServer(PredictServer(ip.explain), port = PORT)
    server.start()
