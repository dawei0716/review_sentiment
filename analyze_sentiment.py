import math
from stopwords import stops
import pickle 

def smooth_naive_bayes(reviewwords):

    posscore = 0
    negscore = 0
    poswords = pickle.load(open('pickleData/poswords.pickle','rb'))
    negwords = pickle.load(open('pickleData/negwords.pickle','rb'))

    posdefaultprob = math.log(1/(len(poswords)+len(set(poswords))+ 1))
    negdefaultprob = math.log(1/(len(negwords)+len(set(negwords))+ 1))
    
    smooth_poswordprobs = pickle.load(open('pickleData/poswordprobs.pickle','rb'))
    smooth_negwordprobs = pickle.load(open('pickleData/negwordprobs.pickle','rb'))

    posscore = smooth_poswordprobs.get(reviewwords[0], posdefaultprob)
    for i in range(1, len(reviewwords)):
        posscore += smooth_poswordprobs.get(reviewwords[i], posdefaultprob)

    negscore = smooth_negwordprobs.get(reviewwords[0], negdefaultprob)
    for i in range(1, len(reviewwords)):
        negscore += smooth_negwordprobs.get(reviewwords[i], negdefaultprob)

    print(posscore-negscore)
    if (posscore - negscore) >  0:
        return "pos"

    return "neg"






def calculate_accuracy():
    
    wholereview = ""
    reviewwords = []
       
    wholereview = "great amazing wonderful fantastic wow truly great" #rstrip() it rstrip() it
    
    words = set(wholereview.split())
    
    for w in words:
        if w not in stops:
            reviewwords.append(w)
            
    judge = smooth_naive_bayes(reviewwords)
    print(judge)
            


calculate_accuracy()

