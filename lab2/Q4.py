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
    wordsTraining = words[:round(size*0.8)] #first 80% of a book are reserved for testing
    print()
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
# for word in bagOfWords:
#     for dict in bookDictionaries:
#         if word not in dict:
#             dict[word] = 0 

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

# vectors = []
# vectors.append(createVector(bagOfWords, pages[1], bookDictionaries[0]))
# vectors.append(createVector(bagOfWords, pages[1], bookDictionaries[1]))
# vectors.append(createVector(bagOfWords, pages[1], bookDictionaries[2]))
# vectors.append(createVector(bagOfWords, pages[1], bookDictionaries[3]))
# vectors.append(createVector(bagOfWords, pages[1], bookDictionaries[4]))
# vectors.append(createVector(bagOfWords, pages[1], bookDictionaries[5]))
# vectors.append(createVector(bagOfWords, pages[1], bookDictionaries[6]))

# now to calculate the probability given a message
def probabilitySentenceGivenBook(vector, bag ,  dict, totalWords):
    prob = 1
    for index in range(len(vector)):
        if vector[index] == 1:
            # print(prob)
            if bag[index] not in dict or dict[bag[index]] ==0 :
                prob +=   abs(math.log(1 / (totalWords + 2),10))
            else:  
                prob += abs(math.log(dict[bag[index]] / totalWords,10))
        else:
            # print(prob)
            if bag[index] not in dict or dict[bag[index]] ==0 :
                prob +=  abs(math.log( 1 - 1 / (totalWords + 2),10))
            else:    
                prob +=  abs( math.log(1 - dict[bag[index]] / totalWords,10))
    return prob

bookIndex = -1
maxProb = 0

# the following loop is to get the numerator of the Naive Bayes Classifier in logs
# whichever index has the maximum numerator will have the highest probability
# this is because all the numerator logs will be subtracted by the same logged denominator

# for i in range(7):
#     probConditional = probabilitySentenceGivenBook(vectors[i],bagOfWords, bookDictionaries[i], bookTotalWords[i])
#     probNumerator = probConditional + abs(math.log(bookPriors[i]))
#     if probNumerator > maxProb:
#         maxProb = probNumerator
#         bookIndex = i

# print("Predicted Book: ", bookIndex )

# Create a function that will take in the test-pages-array and loop through it counting how many times it gets the prediction right
def testFunction(bag,dictionaries,testBookPages, bookTotalWords,  bookPriors):
    correctPredicts = 0
    wrongPredicts = 0
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
                correctPredicts +=1
            else:
                wrongPredicts +=1
    return correctPredicts,wrongPredicts    




print(testFunction(bagOfWords,bookDictionaries,testPages,bookTotalWords,bookPriors))



# for b in bookDictionaries:
#     if "scuttled" in b:
#         print("True")
#     else:
#         print("False")
# t = True
# for dict in bookDictionaries:
#     for w in dict.keys():
#         if w not in bagOfWords:
#             bagOfWords.append(w)

# for dict in bookDictionaries:
#     for w in dict.keys():
#         if w not in bagOfWords:
#             t = False            
# print(t)            
