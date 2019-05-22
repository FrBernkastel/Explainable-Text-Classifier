from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import rpyc



#from textClassifier1 import model

# Create your views here.
# Create your views here.
def index(request):
    context = {"pos_flag":1,"neg_flag":0, "explanation": "This text is negative because of too many negative words."}
    return render(request,'classifier/index.html', context)



def predict(request):
    if request.method == 'POST':
        input_text = request.POST.get("input_text")
    
        label,ex = remote_predict(input_text)
        
        pos_flag = label
        neg_flag = 1-pos_flag

        message = "The label is {}, because it contains words like: {}".format("POS" if pos_flag == 1 else "NEG",ex)

        context = {"explanation": message,"pos_flag":pos_flag,"neg_flag":neg_flag}
    
    return render(request, 'classifier/index.html', context)


def remote_predict(text):
    HOST = "localhost"  # Standard loopback interface address (localhost)
    PORT =  8001        # Port to listen on (non-privileged ports are > 1023)
    try:
        
        with rpyc.connect(HOST, PORT) as conn:
            #text = "I love the dog, and the world, and, everything"
            t,ex = conn.root.predict(text)
            ex = list(ex)
            print(type(t),type(ex))
            print(t,ex)
        
            return t,ex

    except Exception as e:
        raise e
