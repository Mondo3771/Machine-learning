import numpy as np 
import math as math

books = np.array([])
bookDictionaries = []

bookTotalWords = []
sum = 0
bagOfWords = []

testPages = []

for i in range(1,8):
    file = open("HP" + str(i) + ".txt")

    books = np.append(books,file.read())

    pages = books[i-1].split("\n") # get the pages of the ith book
    testPages.append(pages[round(len(pages)*0.8):]) #last 20% of a book are reserved for testing.

    words = books[i-1].split(" ")
    
    size = len(words)
    wordsTraining = words[:round(size*1)] #first 80% of a book are reserved for testing
    dictionary = {} # initialise dictionary for each book
    numWords = 0

    for word in wordsTraining:
        if word == "":  
            pass
        else:
            numWords += 1
            bagOfWords.append(word)
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary[word] = 1    
    bookDictionaries.append(dictionary)
    bookTotalWords.append(numWords)
    sum += numWords


bagOfWords = list(set(bagOfWords))  # List of all the unique words in the books to make vectors
bagOfWords = bagOfWords[1:]


# some words may not appear in each dictionary therefore must be given zeros for the sake of creating vectors
for dict in bookDictionaries:
    for w in dict.keys():
        if w not in bagOfWords:
            bagOfWords.append(w)

# make an array of priors for each book
bookPriors = []
for i in range(7):
    bookPriors.append(bookTotalWords[i] / sum)

# Create a vector based on bag   
#given a page create a vector based on the book    
def createVector (bag , page, dict):
    words = page.split(" ") # individual words in a page
    words = words[1:]
    vector = np.zeros(len(bag)) 
    x = 0
    for word in words:
        if word in dict:
            x += 1
            vector[bag.index(word)] = 1        
    # print(x , " words found in book")
    return vector           

# now to calculate the probability given a message
def probabilitySentenceGivenBook(vector, bag ,  dict, totalWords):
    prob = 1
    for index in range(len(vector)):
        if vector[index] == 1:
            # print(prob)
            if bag[index] not in dict or dict[bag[index]] ==0 :
                prob +=   abs(math.log(285/ (totalWords+570),10))
            else:  
                prob += abs(math.log(dict[bag[index]] / totalWords,10))
        else:
            # print(prob)
            if bag[index] not in dict or dict[bag[index]] ==0 :
                prob +=  abs(math.log( 1 - 285 / (totalWords + 570),10))
            else:    
                prob +=  abs( math.log(1 - dict[bag[index]] / totalWords,10))
    return prob


# the following loop is to get the numerator of the Naive Bayes Classifier in logs
# whichever index has the maximum numerator will have the highest probability
# this is because all the numerator logs will be subtracted by the same logged denominator


# Create a function that will take in the test-pages-array and loop through it counting how many times it gets the prediction right
def testFunction(bag,dictionaries,testBookPages, bookTotalWords,  bookPriors):
    correctPredicts = 0
    wrongPredicts = 0
    confusionMatrix = np.zeros((7,7))
    for k in range(len(testBookPages)):
        for j in range(len(testBookPages[k])):

            vectors = []
            vectors.append(createVector(bag, testBookPages[k][j], dictionaries[0]))
            vectors.append(createVector(bag, testBookPages[k][j], dictionaries[1]))
            vectors.append(createVector(bag, testBookPages[k][j], dictionaries[2]))
            vectors.append(createVector(bag, testBookPages[k][j], dictionaries[3]))
            vectors.append(createVector(bag, testBookPages[k][j], dictionaries[4]))
            vectors.append(createVector(bag, testBookPages[k][j], dictionaries[5]))
            vectors.append(createVector(bag, testBookPages[k][j], dictionaries[6]))

            maxP = 0
            predictedBook = -1
            for i in range(len(vectors)):
                p = probabilitySentenceGivenBook(vectors[i],bag,dictionaries[i],bookTotalWords[i]) + abs(math.log(bookPriors[i])) 
                # p is the probability (in logs) that the page is in book i
                if p > maxP:
                    maxP = p
                    predictedBook = i
            if predictedBook == k:
                confusionMatrix[k][k] += 1
                correctPredicts +=1
            else:
                confusionMatrix[k][predictedBook] += 1
                wrongPredicts +=1
    print(confusionMatrix)            
    return correctPredicts,wrongPredicts    




right,wrong = testFunction(bagOfWords,bookDictionaries,testPages,bookTotalWords,bookPriors)
print(right,wrong)
print("Accuracy: ", right / (right+wrong))
