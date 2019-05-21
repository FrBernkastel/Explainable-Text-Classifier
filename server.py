#!/usr/bin/env python3

import rpyc
import classifier as cf

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8001        # Port to listen on (non-privileged ports are > 1023)


class PredictServer(rpyc.Service):
    """
        The server that makes predictions for text using a classifier
    """

    def __init__(self):
        self.lr = cf.LogisRegression()

    def exposed_predict(self, text):
        try:
            assert type(text) == str, "not valid input"
        except:
            pass

        vec = self.lr.sentiment.count_vect.transform([text])
        res = self.lr.cls.predict(vec)[0]
        return int(res)

    def exposed_test(self, t = None):
        if t is not None:
            return t
        else:
            return "good job"


if __name__ == '__main__':
    from rpyc.utils.server import ThreadPoolServer

    server = ThreadPoolServer(PredictServer(), port = PORT)
    server.start()