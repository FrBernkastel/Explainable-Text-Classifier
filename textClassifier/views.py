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
    
        label = remote_predict(input_text)
        
        pos_flag = label
        neg_flag = 1-pos_flag

        context = {"explanation": input_text,"pos_flag":pos_flag,"neg_flag":neg_flag}
    
    return render(request, 'classifier/index.html', context)


def remote_predict(text):
    HOST = '100.81.51.71'  # Standard loopback interface address (localhost)
    PORT =  8001        # Port to listen on (non-privileged ports are > 1023)
    try:
        
        with rpyc.connect(HOST, PORT) as conn:
            
            #text = "I love the dog, and the world, and, everything"
            t = conn.root.predict(text)
        
            return t

    except Exception as e:
        raise e
