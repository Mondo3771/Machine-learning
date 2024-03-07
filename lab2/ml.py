import numpy as np
def add_dict(b,w,dN,dP,cn,cp):
    a=np.array(w.split()[1:])
    a= np.unique(a) #gets rid of fuplicates in the review because we are checking if its in a neg rev not hoe many times its in the review
    b=np.append(b,a)
    if w[0]=='1':
        cp+=1
        for j in a:
            if j not in dP:
                dP.update({j:1})
            else:
                dP.update({j:dP[j]+1})   
            if j not in dN:
                dN.update({j:0}) #this adds to the table a 0 basically we havent seen it in the negative side but we have seen it in the positve
    else:
        for k in a:
            if k not in dN:
                dN.update({k:1})
            else:
                dN.update({k:dN[k]+1}) 
            if k not in dP:
                dP.update({k:0}) #this adds to the table a 0 basically we havent seen it in the positive side but we have seen it in the negative
        cn+=1
    return cn, cp, dN,dP,b
file1 = open("simple-food-reviews.txt")
words = file1.readline()[:-1] 
reviews = np.array([])
while len(words) != 0:
    reviews = np.append(reviews,words)
    words = file1.readline()[:-1]
np.random.shuffle(reviews)
countp=0
countn=0

bags=np.array([])
dictP={}
dictN={}

for i in range(18): #gets the first 12 
    countn, countp, dictN,dictP ,bags= add_dict(bags,reviews[i],dictN,dictP,countn,countp)
#this sets the probabilty of each word for out class conditional model
bags= np.unique(bags)
print(len(reviews))
priorP=countp/(countp+countn)
priorN=countn/(countp+countn)
#now we are done creating the prior and the class conditional model
#we need to create the encoder 
ce=0
for j in range(18,len(reviews)-1):
    ce+=1
    words = reviews[j]
    rev= words.split(" ")
    vec = np.zeros(len(bags))
    lap = {}
    #this is where we are doing the encoding
    for i in range(1,len(rev)):
        an = np.where(bags == rev[i])[0] #thischecks and finds the index where a word is in bag 
        if len(an) !=0: #if the word is in bags the add 1 to the the vector of the string
            vec[an[0]]+=1
        else:# if its not , this is the word we will need to do laplace on
            pass
    # print(lap)
    # now we are trying to find the product of the probabilities
    probn=1
    probp=1
    for i in range(0,len(vec)): ## This is without laplace smoothing we will do that out side the for loop
        if vec[i] == 0:
            probn = probn *(1- (dictN[bags[i]]+1 )/countn+2)
            probp = probp*(1- (dictP[bags[i]]+1)/countp+2)
        else:
            probn = probn *((dictN[bags[i]]+1 )/countn+2)
            probp = probp *((dictP[bags[i]]+1)/countp+2)
    prob_negative = (probn*priorN)/(probn*priorN + probp*priorP )
    prob_positive = (probp*priorP)/(probn*priorN + probp*priorP )
    
    # print(dictN)
    print(words)
    print("This is the probability that the review is negative ",prob_negative)
    print("This is the probability that the review is positive ",prob_positive)
    countn, countp, dictN,dictP ,bags= add_dict(bags,words,dictN,dictP,countn,countp)
    priorP=countp/(countp+countn)
    priorN=countn/(countp+countn)
    bags= np.unique(bags)
print(ce)