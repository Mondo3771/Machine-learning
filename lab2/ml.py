import numpy as np
nono = np.array(["as","the","was","a","is","and","this","at"])

def add_dict(bag,review,dictN,dictP,countN,countP):

    reviewWords =np.array(review.split()[1:])
    reviewWords = np.unique(reviewWords) #gets rid of duplicates in the review bagecause we are checking if its in a neg rev not hoe many times its in the review
    reviewWords = np.setdiff1d(reviewWords,nono)
    bag=np.append(bag,reviewWords)

    if review[0]=='1':
        countP+=1
        for j in reviewWords:
            if j not in dictP:
                dictP.update({j:1})
            else:
                dictP.update({j:dictP[j]+1})   
            if j not in dictN:
                dictN.update({j:0}) #this adds to the table a 0 basically we havent seen it in the negative side but we have seen it in the positve
    else:
        for k in reviewWords:
            if k not in dictN:
                dictN.update({k:1})
            else:
                dictN.update({k:dictN[k]+1}) 
            if k not in dictP:
                dictP.update({k:0}) #this adds to the table a 0 basically we havent seen it in the positive side but we have seen it in the negative
        countN+=1
    return bag,dictN,dictP,countN,countP

file1 = open("simple-food-reviews.txt")
review = file1.readline()[:-1] 
reviews = np.array([])

while len(review) != 0:
    reviews = np.append(reviews,review)
    review = file1.readline()[:-1]

np.random.shuffle(reviews) #shuffle to choose random reviews

countPositiveReviews=0
countNegativeReviews=0

bag=np.array([]) # bag will hold the unique words gotten from training data (will be used to create vector)
dictPositiveWords={} #holds all words found in positive reviews and how many times
dictNegativeWords={} #holds all words found in negative reviews and how many times


# Training data uses first 12 reviews 
for i in range(12): 
    bag, dictNegativeWords, dictPositiveWords,countNegativeReviews, countPositiveReviews = add_dict(bag,reviews[i],dictNegativeWords,dictPositiveWords,countNegativeReviews,countPositiveReviews)
#this sets the probabilty of each word for out class conditional model

bag= np.unique(bag)

priorP=countPositiveReviews/(countPositiveReviews+countNegativeReviews)
priorN=countNegativeReviews/(countPositiveReviews+countNegativeReviews)

#now we are done creating the prior and the class conditional model


#we need to create the encoder
#Starting to test 
# print(bag)
correctP = 0
correctN = 0
wrongP = 0
wrongN = 0


for j in range(12, len(reviews)): #for each of the last 6 reviews
    review = reviews[j]
    reviewWords= review.split(" ")
    vec = np.zeros(len(bag))

    #this is where we are doing the encoding
    for i in range(1,len(reviewWords)):
        wordIndex = np.where(bag == reviewWords[i])[0] #this checks and finds the indexes where a word is in bag 
        if len(wordIndex) !=0: #if the word is in bag the add 1 to the vector of the string
            vec[wordIndex[0]]+=1
        else:# if its not , this is the word we will need to do laplace on
            pass
    
    # now we are trying to find the product of the probabilities    
    probn=1
    probp=1

#1) code for what happens for when input has more than one instance of the word
#2) code for zero probabilities 
#3) remind niggas that we need to use some data for testing and the other for training 
#4)Should training data change with new test data (no)       


    for i in range(0,len(vec)): ## This is without laplace smoothing we will do that out side the for loop
        if vec[i] == 0:
            probn = probn *(1- (dictNegativeWords[bag[i]]+1)/countNegativeReviews+2) 
            probp = probp*(1- (dictPositiveWords[bag[i]]+1)/countPositiveReviews+2)
        else:
            probn = probn *((dictNegativeWords[bag[i]]+1)/countNegativeReviews+2)
            probp = probp *((dictPositiveWords[bag[i]]+1)/countPositiveReviews+2)
    prob_negative = (probn * priorN)/(probn * priorN + probp * priorP)
    prob_positive = (probp * priorP)/(probn * priorN + probp * priorP)

    # print(reviewWords)
    # print(prob_negative, prob_positive)
    
    if reviewWords[0]=="-1":

        if prob_negative > prob_positive:
            correctN +=1
        elif prob_positive > prob_negative:
            wrongN +=1;  
    elif reviewWords[0]=="1": 

        if prob_positive > prob_negative:
            correctP += 1
        elif prob_negative > prob_positive:
            wrongP += 1     
    bag, dictNegativeWords,dictPositiveWords, countNegativeReviews, countPositiveReviews = add_dict(bag,review,dictNegativeWords,dictPositiveWords,countNegativeReviews,countPositiveReviews)
    priorP=countPositiveReviews/(countPositiveReviews+countNegativeReviews)
    priorN=countNegativeReviews/(countPositiveReviews+countNegativeReviews)
    bag= np.unique(bag)
confusionMatrix = np.array([[correctN, wrongP],[wrongN,correctP]])

print(confusionMatrix)
accuracy  = (correctN +correctP)/(correctP+ correctN +wrongN + wrongP)
print("Accuracy: " , accuracy)
    # check if the review is positive

    



