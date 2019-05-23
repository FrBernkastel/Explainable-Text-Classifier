#!/usr/bin/env python3

import rpyc

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8001        # Port to listen on (non-privileged ports are > 1023)

def predict():
    text = "It's not good enough. "
    try:
        with rpyc.connect(HOST, PORT) as conn:
            t = conn.root.predict(text)
            print(t)

    except Exception as e:
        raise e


predict()