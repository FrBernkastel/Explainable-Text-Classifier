#!/usr/bin/env python3

# %%
import rpyc
import classifier as cf
import interpreter as ip

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8001        # Port to listen on (non-privileged ports are > 1023)


# %%
class PredictServer(rpyc.Service):
    """
        The server that makes predictions for text using a classifier
    """

    def __init__(self, interpreter):
        self.lr = cf.LogisRegression()
        self.ip = interpreter(self.lr)

    def exposed_predict(self, text):
        """

        :param text: the target text
        :return: (prediction, a list of important words)
        """
        try:
            assert type(text) == str, "not valid input"
        except:
            pass

        vec = self.lr.sentiment.count_vect.transform([text])
        res = self.lr.cls.predict(vec)[0]
        ex = self.ip.get_explanation(vec[0])
        pre = int(res)
        # todo: sometimes contains duplicated words, e.g. "it's not good enough". return ['not', 'not good'].
        if pre == 1:
            return (pre, ex['valued_pos'])
        else:
            return (pre, ex['valued_neg'])

    def exposed_test(self, t = None):
        if t is not None:
            return t
        else:
            return "good job"


if __name__ == '__main__':
    from rpyc.utils.server import ThreadPoolServer

    server = ThreadPoolServer(PredictServer(ip.explain), port = PORT)
    server.start()