from django.shortcuts import render
from django.http import JsonResponse
import nltk
import math
from stopwords import stops
import pickle 
import sys
from .models import AnalysisResults


def analyze(request):
    return render(request,'analyze.html')

def about_page(request):
    return render(request, 'about.html')

def view_results(request):
    # Submit prediction and show all
    data = {"dataset": AnalysisResults.objects.all()}
    return render(request, "results.html", data)


def smooth_naive_bayes(reviewwords):

    posscore = 0
    negscore = 0
    poswords = pickle.load(open('machine_learning_stuff/pickleData/poswords.pickle','rb'))
    negwords = pickle.load(open('machine_learning_stuff/pickleData/negwords.pickle','rb'))

    posdefaultprob = math.log(1/(len(poswords)+len(set(poswords))+ 1))
    negdefaultprob = math.log(1/(len(negwords)+len(set(negwords))+ 1))
    
    smooth_poswordprobs = pickle.load(open('machine_learning_stuff/pickleData/poswordprobs.pickle','rb'))
    smooth_negwordprobs = pickle.load(open('machine_learning_stuff/pickleData/negwordprobs.pickle','rb'))

    posscore = smooth_poswordprobs.get(reviewwords[0], posdefaultprob)
    for i in range(1, len(reviewwords)):
        posscore += smooth_poswordprobs.get(reviewwords[i], posdefaultprob)

    negscore = smooth_negwordprobs.get(reviewwords[0], negdefaultprob)
    for i in range(1, len(reviewwords)):
        negscore += smooth_negwordprobs.get(reviewwords[i], negdefaultprob)

    if (posscore - negscore) >  0:
        return "pos", (posscore-negscore)

    return "neg", (posscore-negscore)

def analyze_review(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        review = request.POST.get('review').rstrip()
        reviewwords = []
        token = set(nltk.word_tokenize(review))
        #words = set(review.split())
        #print(token)
        #print(words)
        for w in token:
            if w not in stops:
                reviewwords.append(w)
                
        judge, score = smooth_naive_bayes(reviewwords)
        #print(judge)

        AnalysisResults.objects.create(review=review, result=judge, score = score)
        

    
        return JsonResponse({'review': review, 'result': judge, 'score': score}, safe=False)