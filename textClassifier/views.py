from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
import rpyc
import os
import pickle
import random

review_list = []
news_list = []
review_init = 0
news_init = 0

# random return an review
def pick_review(request):
    global review_list, review_init
    if request.method == 'GET':
        if review_init == 0:
            print(os.getcwd())
            if not os.path.isfile('textClassifier/static/textClassifier/review_list.backup'):
                raise FileNotFoundError()
            else:
                with open('textClassifier/static/textClassifier/review_list.backup', 'rb') as backup_file:
                    review_list = pickle.load(backup_file)
            review_init = 1
        idx = random.randint(0, len(review_list)-1)
        return HttpResponse(review_list[idx])
    else:
        pass


# random return a news headline
def pick_news(request):
    global news_list, news_init
    if request.method == 'GET':
        if news_init == 0:
            if not os.path.isfile('textClassifier/static/textClassifier/news_list.backup'):
                raise FileNotFoundError()
            else:
                with open('textClassifier/static/textClassifier/news_list.backup', 'rb') as backup_file:
                    news_list = pickle.load(backup_file)
            news_init = 1
        idx = random.randint(0, len(news_list) - 1)
        return HttpResponse(news_list[idx])
    else:
        pass


# Create your views here.
def review(request):
    context = {"pos_flag":1,"neg_flag":0, "explanation": "This text is negative because of too many negative words."}
    return render(request,'classifier/review.html', context)


def news(request):
    context = {"pos_flag":1,"neg_flag":0, "explanation": "This text is negative because of too many negative words."}
    return render(request,'classifier/news.html', context)

def predict_news(request):
    if request.method == 'POST':
        input_text = request.POST.get("input_text")
        label_proba, prob, exp, flag = remote_predict_news(input_text)
        # exp = "" 
        # label_proba = [('SPORTS', 0.03528977019242901),('POLOTICS',0.02)]
        # prob = [0.3]*31
        context = {"explanation": exp, "input_text": input_text,
                   "labels": label_proba, "prob": prob, "flag":flag}
        return JsonResponse(context, safe=False)
    else:
        pass

def remote_predict_news(text):
    HOST = "localhost"  # Standard loopback interface address (localhost)
    PORT = 8001  # Port to listen on (non-privileged ports are > 1023)
    try:

        with rpyc.connect(HOST, PORT) as conn:
            # text = "I love the dog, and the world, and, everything"
            res_json = conn.root.predict_news(text)
            import json
            res = json.loads(res_json)
            print(res.keys())

            # 'label', 'probability', 'confidence', 'flag', 'explanation'
            prob = res['labels_prob']
            label = res['topk_label_proba']
            exp = res['label__feat_coef']
            flag =  res['flag']

            return label, prob, exp, flag

    except Exception as e:
        raise e



def predict(request):
    if request.method == 'POST':
        input_text = request.POST.get("input_text")
    
        label,prob,conf,flag,exp_words_list = remote_predict(input_text)
        
        #1.process the exp_words
        exp_words = set()
        for gram in exp_words_list:
            gram = gram.strip()
            words = gram.split(" ")
            for w in words:
                exp_words.add(w)
        exp_words = list(exp_words)
        print(exp_words)

        #2.determine the conclusion
        pos_flag = label
        neg_flag = 1-pos_flag

        if flag == False:
            pos_flag = 0
            neg_flag = 0
        print(flag,pos_flag,neg_flag)

        #!should remove the debug message
        message = "The label is {}, because it contains words like: {}, the probability is: {} \
        , the confidence is: {}, the flag is :{}".format("POS" if pos_flag == 1 else "NEG",exp_words, prob, conf, flag)
        print(message)

        #3. calculate the prob for each label
        pos_prob = 0.5
        neg_prob = 0.5
        if pos_flag == 1:
            pos_prob = (prob)*100
            neg_prob = (1-prob)*100 
        else:
            pos_prob = (1-prob)*100
            neg_prob = (prob)*100

        #4. construct the json response
        context = {"explanation": message,"pos_flag":pos_flag,"neg_flag":neg_flag,\
                   "input_text" : input_text,"pos_prob":pos_prob,"neg_prob":neg_prob, \
                   "exp_words":exp_words}
        return JsonResponse(context, safe=False)
    else:
        context = {"pos_flag":1,"neg_flag":0, "explanation": "This text is negative because of too many negative words."}
        return render(request,'classifier/index.html', context)


def remote_predict(text):
    HOST = "localhost"  # Standard loopback interface address (localhost)
    PORT =  8001        # Port to listen on (non-privileged ports are > 1023)
    try:
        
        with rpyc.connect(HOST, PORT) as conn:
            #text = "I love the dog, and the world, and, everything"
            res_json = conn.root.predict(text)
            import json
            res = json.loads(res_json)
            print(res)
            #'label', 'probability', 'confidence', 'flag', 'explanation'
            label = res['label']
            prob = res['probability']
            conf = res['confidence']
            flag = res['flag']
            exp = res['explanation']
            
            return label,prob,conf,flag,exp

    except Exception as e:
        raise e

