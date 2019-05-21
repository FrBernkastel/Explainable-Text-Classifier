import rpyc

HOST = '100.64.2.75'  # Standard loopback interface address (localhost)
PORT = 8001        # Port to listen on (non-privileged ports are > 1023)

def predict():
    try:
        with rpyc.connect(HOST, PORT) as conn:
            t = conn.root.test()
            print(t)

    except Exception as e:
        raise e


predict()