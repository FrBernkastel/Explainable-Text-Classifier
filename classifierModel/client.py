#!/usr/bin/env python3

import rpyc

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8001        # Port to listen on (non-privileged ports are > 1023)

def predict():
    text = "It's not good enough. "
    # text_news = "Hugh Grant Marries For The First Time At Age 57"
    text_news = "xx"
    try:
        with rpyc.connect(HOST, PORT) as conn:
            t = conn.root.predict(text)
            print(t)
            t = conn.root.predict_news(text_news)
            print(t)

    except Exception as e:
        raise e


predict()
